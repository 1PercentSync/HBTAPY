import os
import subprocess
import platform
import sys
from typing import List, Dict, Tuple, Optional

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("错误: chromadb 模块未安装")
    print("请运行: pip install chromadb")
    sys.exit(1)

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

class SemanticSearchEngine:
    def __init__(self, openai_client):
        self.client = openai_client
        self.config = Config()
        self.chroma_client = None
        self.collection = None
        self._initialize_chroma()
    
    def _initialize_chroma(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create ChromaDB client with persistent storage
            self.chroma_client = chromadb.PersistentClient(
                path=self.config.CHROMA_DB_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
            
            print(f"ChromaDB 已初始化，集合中有 {self.collection.count()} 个文档")
            
        except Exception as e:
            print(f"初始化 ChromaDB 失败: {e}")
            raise
    
    def index_files(self, embeddings_data: List[Tuple[str, List[float], Dict]]):
        """
        Index files into ChromaDB
        embeddings_data: List of (id, embedding, metadata) tuples
        """
        if not self.chroma_client:
            raise RuntimeError("ChromaDB 客户端未初始化")
            
        if not embeddings_data:
            print("没有文件需要索引")
            return
        
        print(f"正在索引 {len(embeddings_data)} 个文件到向量数据库...")
        
        # Clear existing collection
        try:
            self.chroma_client.delete_collection(self.config.COLLECTION_NAME)
        except Exception:
            # Collection might not exist, which is fine
            pass
        
        self.collection = self.chroma_client.create_collection(
            name=self.config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Prepare data for ChromaDB
        ids = []
        embeddings = []
        metadatas = []
        documents = []
        
        for file_id, embedding, metadata in embeddings_data:
            ids.append(file_id)
            embeddings.append(embedding)
            metadatas.append(metadata)
            documents.append(metadata['searchable_text'])
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            print(f"成功索引 {len(embeddings_data)} 个文件")
        except Exception as e:
            print(f"索引文件时出错: {e}")
            raise
    
    def search(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        """
        Search for files similar to the query
        Returns list of search results with metadata and scores
        """
        if not self.collection:
            print("错误: 还没有索引任何文件")
            return []
            
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS
        
        print(f"正在搜索: '{query}'")
        
        try:
            # Generate embedding for the query
            response = self.client.embeddings.create(
                input=[query],
                model=self.config.EMBEDDING_MODEL
            )
            query_embedding = response.data[0].embedding
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['metadatas', 'documents', 'distances']  # type: ignore
            )
            
            # Format results
            search_results = []
            if results and 'metadatas' in results and results['metadatas'] and results['metadatas'][0]:
                metadatas = results['metadatas'][0]  # type: ignore
                distances = results['distances'][0] if 'distances' in results and results['distances'] else []  # type: ignore
                
                for i, metadata in enumerate(metadatas):
                    similarity_score = 1 - distances[i] if distances and i < len(distances) else 0.5
                    result = {
                        'file_path': metadata['file_path'],
                        'file_name': metadata['file_name'],
                        'file_stem': metadata['file_stem'],
                        'file_extension': metadata['file_extension'],
                        'file_parent': metadata['file_parent'],
                        'searchable_text': metadata['searchable_text'],
                        'similarity_score': similarity_score,
                        'rank': i + 1
                    }
                    search_results.append(result)
            
            print(f"找到 {len(search_results)} 个相关结果")
            return search_results
            
        except Exception as e:
            print(f"搜索时出错: {e}")
            return []
    
    def open_file_location(self, file_path: str):
        """
        Open Windows Explorer and select the specified file
        """
        try:
            # Verify file still exists
            if not os.path.exists(file_path):
                print(f"警告: 文件不存在 {file_path}")
                return
                
            if platform.system() == 'Windows':
                # Use Windows Explorer to select the file
                subprocess.run(['explorer', '/select,', file_path], check=True)
                print(f"已在文件管理器中定位到: {file_path}")
            else:
                # For non-Windows systems, just open the parent directory
                parent_dir = os.path.dirname(file_path)
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', parent_dir], check=True)
                else:  # Linux
                    subprocess.run(['xdg-open', parent_dir], check=True)
                print(f"已打开目录: {parent_dir}")
                
        except subprocess.CalledProcessError as e:
            print(f"打开文件位置失败: {e}")
        except Exception as e:
            print(f"意外错误: {e}")
    
    def display_search_results(self, results: List[Dict]):
        """
        Display search results in a formatted way
        """
        if not results:
            print("没有找到相关文件")
            return
        
        print("\n" + "="*80)
        print("搜索结果:")
        print("="*80)
        
        for result in results:
            similarity_percentage = result['similarity_score'] * 100
            print(f"\n[{result['rank']}] {result['file_name']}")
            print(f"    路径: {result['file_path']}")
            print(f"    目录: {result['file_parent']}")
            print(f"    相似度: {similarity_percentage:.1f}%")
            print(f"    搜索文本: {result['searchable_text']}")
        
        print("\n" + "="*80)
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the indexed collection"""
        if not self.collection:
            return {"count": 0}
        
        try:
            count = self.collection.count()
            return {
                "count": count,
                "collection_name": self.config.COLLECTION_NAME
            }
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {"count": 0} 