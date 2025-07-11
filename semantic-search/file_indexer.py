import os
import hashlib
import sys
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from tqdm import tqdm
except ImportError:
    # Simple fallback if tqdm is not available
    def tqdm(iterable, desc="Processing", **kwargs):
        print(f"{desc}...")
        return iterable

try:
    import openai
except ImportError:
    print("错误: openai 模块未安装")
    print("请运行: pip install openai")
    sys.exit(1)

try:
    from config import Config
except ImportError:
    print("错误: 无法导入 config 模块")
    sys.exit(1)

class FileIndexer:
    def __init__(self, openai_client):
        self.client = openai_client
        self.config = Config()
    
    def discover_files(self, root_path: str) -> List[Dict]:
        """
        Discover all files in the given directory and subdirectories
        Returns list of file info dictionaries
        """
        files_info = []
        
        try:
            root_path_obj = Path(root_path)
            
            print(f"正在扫描目录: {root_path_obj}")
            
            # Walk through all files and subdirectories
            for file_path in root_path_obj.rglob('*'):
                if file_path.is_file():
                    # Check if file extension should be indexed
                    file_ext = file_path.suffix.lower()
                    if not self.config.INDEXED_EXTENSIONS or file_ext in self.config.INDEXED_EXTENSIONS:
                        try:
                            file_info = {
                                'path': str(file_path.absolute()),
                                'name': file_path.name,
                                'stem': file_path.stem,  # filename without extension
                                'extension': file_ext,
                                'parent': str(file_path.parent),
                                'size': file_path.stat().st_size,
                                'modified_time': file_path.stat().st_mtime
                            }
                            
                            # Generate unique ID for the file
                            file_info['id'] = self._generate_file_id(file_info['path'])
                            files_info.append(file_info)
                        except (OSError, PermissionError) as e:
                            print(f"跳过文件 {file_path}: {e}")
                            continue
            
            print(f"发现 {len(files_info)} 个文件")
            return files_info
            
        except Exception as e:
            print(f"扫描目录时出错: {e}")
            return []
    
    def _generate_file_id(self, file_path: str) -> str:
        """Generate unique ID for a file based on its path"""
        return hashlib.md5(file_path.encode()).hexdigest()
    
    def create_searchable_text(self, file_info: Dict) -> str:
        """
        Create searchable text from file information
        This combines filename, path components, and extension for better semantic matching
        """
        # Extract meaningful components
        name_parts = []
        
        # Add filename without extension
        name_parts.append(file_info['stem'])
        
        # Add individual words from filename (split by common separators)
        stem_words = self._split_filename(file_info['stem'])
        name_parts.extend(stem_words)
        
        # Add parent directory names for context
        parent_parts = Path(file_info['parent']).parts
        name_parts.extend(parent_parts[-2:])  # Last 2 directory levels
        
        # Add file extension description
        ext_description = self._get_extension_description(file_info['extension'])
        if ext_description:
            name_parts.append(ext_description)
        
        # Combine all parts
        searchable_text = ' '.join(filter(None, name_parts))
        return searchable_text.lower()
    
    def _split_filename(self, filename: str) -> List[str]:
        """Split filename by common separators and camelCase"""
        import re
        # Split by common separators
        parts = re.split(r'[-_\s.]+', filename)
        
        # Further split camelCase
        result = []
        for part in parts:
            # Split camelCase: insertSpaces -> insert Spaces
            camel_split = re.sub(r'(?<!^)(?=[A-Z])', ' ', part).split()
            result.extend(camel_split)
        
        return [p.strip() for p in result if p.strip()]
    
    def _get_extension_description(self, extension: str) -> str:
        """Get human-readable description for file extensions"""
        ext_descriptions = {
            '.txt': 'text document',
            '.docx': 'word document',
            '.pdf': 'pdf document',
            '.py': 'python script',
            '.js': 'javascript file',
            '.html': 'web page',
            '.css': 'stylesheet',
            '.md': 'markdown document',
            '.json': 'data file',
            '.xml': 'data file',
            '.csv': 'spreadsheet data',
            '.xlsx': 'excel spreadsheet',
            '.pptx': 'presentation',
            '.zip': 'archive file',
            '.jpg': 'image photo',
            '.jpeg': 'image photo',
            '.png': 'image graphic',
            '.gif': 'animated image',
            '.svg': 'vector graphic',
            '.mp4': 'video file',
            '.avi': 'video file',
            '.mov': 'video file',
            '.mp3': 'audio music',
            '.wav': 'audio file',
            '.flac': 'audio music'
        }
        return ext_descriptions.get(extension.lower(), '')
    
    def generate_embeddings(self, files_info: List[Dict]) -> List[Tuple[str, List[float], Dict]]:
        """
        Generate embeddings for all files
        Returns list of (id, embedding, metadata) tuples
        """
        print("正在生成文件嵌入向量...")
        embeddings_data = []
        
        if not files_info:
            print("没有文件需要处理")
            return embeddings_data
        
        # Prepare texts for embedding
        texts = []
        for file_info in files_info:
            searchable_text = self.create_searchable_text(file_info)
            texts.append(searchable_text)
        
        # Generate embeddings in batches for efficiency
        batch_size = 100
        for i in tqdm(range(0, len(texts), batch_size), desc="生成嵌入向量"):
            batch_texts = texts[i:i + batch_size]
            batch_files = files_info[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    input=batch_texts,
                    model=self.config.EMBEDDING_MODEL
                )
                
                for j, embedding_obj in enumerate(response.data):
                    file_info = batch_files[j]
                    embedding = embedding_obj.embedding
                    
                    metadata = {
                        'file_path': file_info['path'],
                        'file_name': file_info['name'],
                        'file_stem': file_info['stem'],
                        'file_extension': file_info['extension'],
                        'file_parent': file_info['parent'],
                        'searchable_text': texts[i + j],
                        'file_size': file_info['size']
                    }
                    
                    embeddings_data.append((file_info['id'], embedding, metadata))
                    
            except Exception as e:
                print(f"生成嵌入向量时出错: {e}")
                # 继续处理其他批次
                continue
        
        print(f"成功生成 {len(embeddings_data)} 个文件的嵌入向量")
        return embeddings_data 