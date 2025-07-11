# 语义文件搜索工具

一个基于 AI 的智能文件搜索工具，使用 OpenAI 嵌入模型和 ChromaDB 向量数据库实现文件名的语义搜索。

## 功能特点

- 🔍 **语义搜索**: 使用自然语言搜索文件，如输入"岩石"可以找到"石头"、"花岗岩"等相关文件
- 📁 **递归索引**: 自动索引指定目录及其所有子目录中的文件
- 🚀 **快速响应**: 基于向量相似度的快速搜索
- 💰 **成本优化**: 使用 OpenAI 的 text-embedding-3-small 模型，成本较低
- 🖥️ **文件定位**: 直接在 Windows 文件管理器中定位到选中的文件
- 💾 **持久化存储**: 使用 ChromaDB 本地存储，无需重复索引

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd semantic-search
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/macOS
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 复制环境变量模板
copy config_template.txt .env  # Windows
# 或
cp config_template.txt .env    # Linux/macOS

# 编辑 .env 文件，填入你的 OpenAI API Key
OPENAI_API_KEY=your_actual_api_key_here
```

### 5. 获取 OpenAI API Key
1. 访问 [OpenAI API Keys](https://platform.openai.com/api-keys)
2. 登录或注册账户
3. 创建新的 API Key
4. 将 API Key 复制到 `.env` 文件中

## 使用方法

### 启动程序
```bash
python main.py
```

### 基本流程
1. **索引目录**: 首次使用时，输入要搜索的目录路径，程序会扫描并索引所有文件
2. **语义搜索**: 输入搜索关键词，支持自然语言描述
3. **选择文件**: 从搜索结果中选择文件序号，程序会在文件管理器中定位该文件

### 搜索示例
- 输入 "石头" → 找到包含 "石头"、"岩石"、"花岗岩" 等的文件
- 输入 "图片" → 找到 .jpg、.png、.gif 等图像文件
- 输入 "音乐" → 找到 .mp3、.wav、.flac 等音频文件
- 输入 "代码" → 找到 .py、.js、.html 等代码文件

## 技术架构

### 核心组件
- **OpenAI Embeddings**: 使用 `text-embedding-3-small` 模型生成文本向量
- **ChromaDB**: 开源向量数据库，支持本地持久化存储
- **文件索引器**: 扫描文件系统并生成可搜索的文本描述
- **语义搜索引擎**: 基于余弦相似度的向量搜索

### 文件处理
程序会为每个文件生成搜索文本，包括：
- 文件名（去除扩展名）
- 文件名中的单词分割
- 父目录名称
- 文件类型描述

支持的文件类型包括：
- 文档: .txt, .docx, .pdf, .md
- 代码: .py, .js, .html, .css, .json
- 媒体: .jpg, .png, .mp4, .mp3
- 办公: .xlsx, .pptx, .csv
- 其他: .zip, .xml 等

## 配置选项

### config.py 中的主要配置
```python
# 嵌入模型（成本优化）
EMBEDDING_MODEL = 'text-embedding-3-small'

# 搜索结果数量
TOP_K_RESULTS = 10

# 支持的文件扩展名
INDEXED_EXTENSIONS = {'.txt', '.py', '.jpg', ...}
```

## 成本说明

使用 OpenAI `text-embedding-3-small` 模型：
- 成本: $0.00002 / 1K tokens
- 示例: 索引 1000 个文件大约花费 $0.01-0.02
- 搜索操作成本极低（每次搜索 < $0.001）

## 故障排除

### 常见问题
1. **API Key 错误**: 确保 `.env` 文件中的 OpenAI API Key 正确
2. **权限问题**: 确保程序有读取目标目录的权限
3. **依赖问题**: 确保所有依赖包都已正确安装

### 日志信息
程序会显示详细的处理进度：
- 文件扫描进度
- 嵌入向量生成进度
- 搜索结果和相似度分数

## 开发相关

### 项目结构
```
semantic-search/
├── main.py              # 主程序入口
├── config.py            # 配置管理
├── file_indexer.py      # 文件索引器
├── semantic_search.py   # 搜索引擎
├── requirements.txt     # 依赖列表
├── config_template.txt  # 环境变量模板
└── chroma_db/          # ChromaDB 数据存储目录（自动创建）
```

### 扩展功能
- 添加更多文件类型支持
- 实现增量索引更新
- 添加文件内容搜索
- 支持更多操作系统的文件打开方式

## 许可证

本项目使用 MIT 许可证。 