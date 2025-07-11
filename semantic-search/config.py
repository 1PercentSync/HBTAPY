import os
import sys

try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    print("警告: python-dotenv 未安装，将使用系统环境变量")
    print("如需从 .env 文件加载配置，请安装: pip install python-dotenv")

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    EMBEDDING_MODEL = 'text-embedding-3-small'  # Cost-effective model
    
    # Chroma Configuration
    CHROMA_DB_PATH = './chroma_db'
    COLLECTION_NAME = 'file_embeddings'
    
    # Search Configuration
    TOP_K_RESULTS = 10
    
    # File Extensions to Index (can be extended)
    INDEXED_EXTENSIONS = {
        # 文档类型
        '.txt', '.docx', '.pdf', '.md', '.json', '.xml', '.csv', '.xlsx', '.pptx',
        # 代码类型  
        '.py', '.js', '.html', '.css', '.zip',
        # 图像类型
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tga', '.psd',
        # 音频类型
        '.mp3', '.wav', '.flac', '.mp4', '.avi', '.mov',
        # Unreal Engine 资产类型
        '.uasset', '.umap', '.upk',
        # 其他游戏开发文件
        '.fbx', '.obj', '.3ds', '.dae', '.blend'
    }
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required. 请在 .env 文件中设置或作为系统环境变量")
        return True 