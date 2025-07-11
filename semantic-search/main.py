#!/usr/bin/env python3
"""
语义文件搜索工具
使用 OpenAI 嵌入模型和 ChromaDB 向量数据库实现文件名的语义搜索
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, List
try:
    import openai
    from colorama import init, Fore, Style
    from config import Config
    from file_indexer import FileIndexer
    from semantic_search import SemanticSearchEngine
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装所有依赖包：pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama for Windows
init()

class SemanticFileSearchApp:
    def __init__(self):
        self.config = Config()
        self.openai_client: Optional[openai.OpenAI] = None
        self.indexer: Optional[FileIndexer] = None
        self.search_engine: Optional[SemanticSearchEngine] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the application"""
        try:
            # Validate configuration
            self.config.validate_config()
            
            # Initialize OpenAI client
            self.openai_client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            
            # Initialize components
            self.indexer = FileIndexer(self.openai_client)
            self.search_engine = SemanticSearchEngine(self.openai_client)
            
            print(f"{Fore.GREEN}✓ 语义搜索引擎初始化成功{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}✗ 初始化失败: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def print_welcome(self):
        """Print welcome message"""
        print(f"{Fore.CYAN}")
        print("=" * 60)
        print("           语义文件搜索工具")
        print("    使用 AI 技术进行智能文件名搜索")
        print("=" * 60)
        print(f"{Style.RESET_ALL}")
        print("功能说明:")
        print("• 输入目录路径进行文件索引")
        print("• 使用自然语言搜索文件")
        print("• 支持语义相似性匹配")
        print("• 直接在文件管理器中定位文件")
        print()
    
    def get_directory_input(self) -> Optional[str]:
        """Get directory path from user"""
        while True:
            print(f"{Fore.YELLOW}请输入要索引的目录路径 (或输入 'quit' 退出):{Style.RESET_ALL}")
            directory = input("目录路径: ").strip()
            
            if directory.lower() == 'quit':
                return None
            
            if not directory:
                print(f"{Fore.RED}请输入有效的目录路径{Style.RESET_ALL}")
                continue
            
            # Expand user path and resolve
            directory = os.path.expanduser(directory)
            directory = os.path.abspath(directory)
            
            if not os.path.exists(directory):
                print(f"{Fore.RED}目录不存在: {directory}{Style.RESET_ALL}")
                continue
            
            if not os.path.isdir(directory):
                print(f"{Fore.RED}路径不是目录: {directory}{Style.RESET_ALL}")
                continue
            
            return directory
    
    def index_directory(self, directory: str) -> bool:
        """Index all files in the directory"""
        if not self.indexer or not self.search_engine:
            print(f"{Fore.RED}系统未正确初始化{Style.RESET_ALL}")
            return False
            
        try:
            print(f"\n{Fore.CYAN}开始索引目录: {directory}{Style.RESET_ALL}")
            
            # Discover files
            files_info = self.indexer.discover_files(directory)
            
            if not files_info:
                print(f"{Fore.YELLOW}目录中没有找到可索引的文件{Style.RESET_ALL}")
                return False
            
            # Generate embeddings
            embeddings_data = self.indexer.generate_embeddings(files_info)
            
            if not embeddings_data:
                print(f"{Fore.RED}生成嵌入向量失败{Style.RESET_ALL}")
                return False
            
            # Index files
            self.search_engine.index_files(embeddings_data)
            
            print(f"{Fore.GREEN}✓ 索引完成! 共索引 {len(embeddings_data)} 个文件{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}索引过程中出错: {e}{Style.RESET_ALL}")
            return False
    
    def search_files(self):
        """Interactive file search"""
        if not self.search_engine:
            print(f"{Fore.RED}搜索引擎未初始化{Style.RESET_ALL}")
            return
            
        stats = self.search_engine.get_collection_stats()
        if stats["count"] == 0:
            print(f"{Fore.YELLOW}还没有索引任何文件，请先索引一个目录{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}开始搜索 (当前已索引 {stats['count']} 个文件){Style.RESET_ALL}")
        print("输入搜索关键词，支持自然语言描述")
        print("例如: '石头', '岩石', '图片', 'python代码', '音乐文件' 等")
        print("输入 'back' 返回主菜单")
        
        while True:
            print(f"\n{Fore.YELLOW}请输入搜索词:{Style.RESET_ALL}")
            query = input("搜索: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'back':
                break
            
            # Perform search
            results = self.search_engine.search(query)
            
            if not results:
                print(f"{Fore.YELLOW}没有找到相关文件，请尝试其他关键词{Style.RESET_ALL}")
                continue
            
            # Display results
            self.search_engine.display_search_results(results)
            
            # Ask user to select a file
            self.handle_file_selection(results)
    
    def handle_file_selection(self, results: List[Dict]):
        """Handle user selection of search results"""
        if not self.search_engine:
            print(f"{Fore.RED}搜索引擎未初始化{Style.RESET_ALL}")
            return
            
        while True:
            print(f"\n{Fore.YELLOW}请选择文件序号 (1-{len(results)}) 在文件管理器中打开，或输入 'new' 进行新搜索:{Style.RESET_ALL}")
            selection = input("选择: ").strip()
            
            if selection.lower() == 'new':
                break
            
            if not selection.isdigit():
                print(f"{Fore.RED}请输入有效的数字{Style.RESET_ALL}")
                continue
            
            index = int(selection) - 1
            if index < 0 or index >= len(results):
                print(f"{Fore.RED}选择超出范围，请输入 1-{len(results)} 之间的数字{Style.RESET_ALL}")
                continue
            
            # Open file location
            selected_file = results[index]
            self.search_engine.open_file_location(selected_file['file_path'])
            break
    
    def show_main_menu(self):
        """Show main menu and handle user choices"""
        while True:
            print(f"\n{Fore.CYAN}主菜单:{Style.RESET_ALL}")
            print("1. 索引新目录")
            print("2. 搜索文件")
            print("3. 查看统计信息")
            print("4. 退出")
            
            choice = input("\n请选择 (1-4): ").strip()
            
            if choice == '1':
                directory = self.get_directory_input()
                if directory:
                    self.index_directory(directory)
                else:
                    break
            
            elif choice == '2':
                self.search_files()
            
            elif choice == '3':
                self.show_stats()
            
            elif choice == '4':
                print(f"{Fore.GREEN}再见！{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}无效选择，请输入 1-4{Style.RESET_ALL}")
    
    def show_stats(self):
        """Show collection statistics"""
        if not self.search_engine:
            print(f"{Fore.RED}搜索引擎未初始化{Style.RESET_ALL}")
            return
            
        stats = self.search_engine.get_collection_stats()
        print(f"\n{Fore.CYAN}统计信息:{Style.RESET_ALL}")
        print(f"已索引文件数量: {stats['count']}")
        print(f"向量数据库路径: {self.config.CHROMA_DB_PATH}")
        print(f"使用的嵌入模型: {self.config.EMBEDDING_MODEL}")
    
    def run(self):
        """Run the main application"""
        self.print_welcome()
        
        # Check if there are existing indexed files
        if self.search_engine:
            stats = self.search_engine.get_collection_stats()
            if stats["count"] > 0:
                print(f"{Fore.GREEN}发现已索引的文件: {stats['count']} 个{Style.RESET_ALL}")
                print("您可以直接进行搜索，或索引新的目录")
        
        self.show_main_menu()

def main():
    """Main entry point"""
    try:
        app = SemanticFileSearchApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}程序被用户中断{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}程序运行出错: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main() 