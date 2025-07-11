#!/usr/bin/env python3
"""
测试脚本 - 验证语义搜索工具的依赖是否正确安装
"""

import sys

def test_imports():
    """测试所有必需的模块导入"""
    print("🔍 检测依赖模块...")
    
    # Test basic modules
    try:
        import os, sys, hashlib, subprocess, platform
        from pathlib import Path
        from typing import List, Dict, Tuple, Optional
        print("✅ 基础模块: OK")
    except ImportError as e:
        print(f"❌ 基础模块导入失败: {e}")
        return False
    
    # Test OpenAI
    try:
        import openai
        print("✅ OpenAI: OK")
    except ImportError:
        print("❌ OpenAI 模块未安装 - 请运行: pip install openai")
        return False
    
    # Test ChromaDB
    try:
        import chromadb
        print("✅ ChromaDB: OK")
    except ImportError:
        print("❌ ChromaDB 模块未安装 - 请运行: pip install chromadb")
        return False
    
    # Test Colorama
    try:
        from colorama import init, Fore, Style
        print("✅ Colorama: OK")
    except ImportError:
        print("❌ Colorama 模块未安装 - 请运行: pip install colorama")
        return False
    
    # Test tqdm (optional)
    try:
        from tqdm import tqdm
        print("✅ tqdm: OK")
    except ImportError:
        print("⚠️  tqdm 模块未安装 (可选) - 进度条将使用简化版本")
    
    # Test python-dotenv (optional)
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv: OK")
    except ImportError:
        print("⚠️  python-dotenv 模块未安装 (可选) - 将使用系统环境变量")
    
    return True

def test_config():
    """测试配置模块"""
    print("\n🔧 测试配置模块...")
    try:
        from config import Config
        config = Config()
        print("✅ 配置模块加载成功")
        
        # Check API key (don't print it for security)
        if config.OPENAI_API_KEY:
            print("✅ OpenAI API Key 已设置")
        else:
            print("⚠️  OpenAI API Key 未设置 - 请在 .env 文件中配置")
            
        return True
    except Exception as e:
        print(f"❌ 配置模块测试失败: {e}")
        return False

def test_modules():
    """测试主要功能模块"""
    print("\n📦 测试功能模块...")
    
    try:
        from file_indexer import FileIndexer
        print("✅ 文件索引器模块: OK")
    except Exception as e:
        print(f"❌ 文件索引器模块失败: {e}")
        return False
    
    try:
        from semantic_search import SemanticSearchEngine
        print("✅ 语义搜索引擎模块: OK")
    except Exception as e:
        print(f"❌ 语义搜索引擎模块失败: {e}")
        return False
    
    try:
        from main import SemanticFileSearchApp
        print("✅ 主程序模块: OK")
    except Exception as e:
        print(f"❌ 主程序模块失败: {e}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("        语义文件搜索工具 - 安装测试")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    if not test_imports():
        all_tests_passed = False
    
    if not test_config():
        all_tests_passed = False
    
    if not test_modules():
        all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 所有测试通过！程序准备就绪")
        print("\n下一步：")
        print("1. 确保在 .env 文件中设置了 OPENAI_API_KEY")
        print("2. 运行: python main.py")
    else:
        print("❌ 部分测试失败，请检查上述错误信息")
        print("\n建议：")
        print("1. 运行: pip install -r requirements.txt")
        print("2. 确保所有依赖都正确安装")
    print("=" * 60)

if __name__ == "__main__":
    main() 