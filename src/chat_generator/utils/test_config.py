#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI配置测试工具
用于测试Google AI API配置是否正确
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / 'src'))

def test_ai_config():
    """测试AI配置"""
    print("🧪 测试AI配置...")
    print("=" * 50)
    
    try:
        # 导入配置模块
        from chat_generator.config.settings import (
            GOOGLE_AI_API_KEY, 
            DEFAULT_MODEL, 
            validate_config,
            get_config_summary
        )
        
        print("✅ 配置模块导入成功")
        
        # 验证配置
        errors = validate_config()
        if errors:
            print("❌ 配置验证失败:")
            for error in errors:
                print(f"   - {error}")
            return False
        else:
            print("✅ 配置验证通过")
        
        # 显示配置摘要
        config_summary = get_config_summary()
        print("\n📋 配置摘要:")
        print(f"   API密钥已设置: {config_summary['api_key_set']}")
        print(f"   默认模型: {config_summary['model']}")
        print(f"   调试模式: {config_summary['debug']}")
        print(f"   日志级别: {config_summary['log_level']}")
        
        # 测试Google AI API
        if GOOGLE_AI_API_KEY:
            print("\n🔗 测试Google AI API连接...")
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_AI_API_KEY)
                
                # 测试模型列表
                models = list(genai.list_models())
                if models:
                    print("✅ Google AI API连接成功")
                    print(f"   可用模型数量: {len(models)}")
                    return True
                else:
                    print("⚠️  API连接成功，但未找到可用模型")
                    return False
                    
            except Exception as e:
                print(f"❌ Google AI API连接失败: {e}")
                return False
        else:
            print("⚠️  未设置API密钥，跳过API测试")
            return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所需依赖包")
        return False
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 AI配置测试工具")
    print("=" * 50)
    
    if test_ai_config():
        print("\n🎉 AI配置测试通过！")
        print("   您现在可以使用AI聊天生成功能了")
    else:
        print("\n❌ AI配置测试失败")
        print("   请检查配置并重试")

if __name__ == "__main__":
    main()
