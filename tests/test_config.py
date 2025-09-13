#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件
验证API密钥配置是否正确
"""

import os
from config import GOOGLE_AI_API_KEY

def test_config():
    """测试配置"""
    print("🔧 测试配置文件")
    print("=" * 30)
    
    # 检查API密钥
    if GOOGLE_AI_API_KEY == "YOUR_GOOGLE_AI_API_KEY_HERE":
        print("❌ API密钥未设置")
        print("请修改 config.py 文件中的 GOOGLE_AI_API_KEY 变量")
        print("获取API密钥：https://makersuite.google.com/app/apikey")
        return False
    else:
        print("✅ API密钥已设置")
        print(f"密钥长度: {len(GOOGLE_AI_API_KEY)} 字符")
        print(f"密钥前缀: {GOOGLE_AI_API_KEY[:10]}...")
        return True

def test_imports():
    """测试导入"""
    print("\n📦 测试模块导入")
    print("=" * 30)
    
    try:
        from main import ChatGenerator, Character
        print("✅ 基础模块导入成功")
    except ImportError as e:
        print(f"❌ 基础模块导入失败: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google AI模块导入成功")
    except ImportError as e:
        print(f"❌ Google AI模块导入失败: {e}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    try:
        from ai_chat_generator import AIChatGenerator
        print("✅ AI聊天生成器导入成功")
    except ImportError as e:
        print(f"❌ AI聊天生成器导入失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🧪 聊天记录生成器配置测试")
    print("=" * 50)
    
    # 测试配置
    config_ok = test_config()
    
    # 测试导入
    import_ok = test_imports()
    
    print("\n" + "=" * 50)
    if config_ok and import_ok:
        print("🎉 所有测试通过！可以正常使用AI功能")
    else:
        print("❌ 部分测试失败，请检查配置")
        if not config_ok:
            print("   - 需要设置API密钥")
        if not import_ok:
            print("   - 需要安装依赖包")

if __name__ == "__main__":
    main()
