#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境配置测试脚本
用于测试.env文件配置是否正确
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def test_env_config():
    """测试环境配置"""
    print("🧪 测试环境配置...")
    print("=" * 50)
    
    # 检查.env文件是否存在
    env_file = project_root / '.env'
    if env_file.exists():
        print("✅ .env文件存在")
    else:
        print("⚠️  .env文件不存在，请创建.env文件")
        print("   可以复制env.example文件并重命名为.env")
        return False
    
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
        print(f"   默认消息数量: {config_summary['default_message_count']}")
        print(f"   默认时长: {config_summary['default_duration_hours']}小时")
        print(f"   默认角色数量: {config_summary['default_character_count']}")
        print(f"   保存间隔: {config_summary['save_interval']}条消息")
        print(f"   实时保存: {config_summary['realtime_save']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入配置模块失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def create_env_file():
    """创建.env文件"""
    print("\n🔧 创建.env文件...")
    
    env_file = project_root / '.env'
    env_example = project_root / 'env.example'
    
    if env_file.exists():
        print("⚠️  .env文件已存在")
        return True
    
    if env_example.exists():
        # 复制env.example到.env
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ 已从env.example创建.env文件")
        print("   请编辑.env文件，设置您的API密钥")
        return True
    else:
        print("❌ env.example文件不存在")
        return False

def main():
    """主函数"""
    print("🚀 环境配置测试工具")
    print("=" * 50)
    
    # 检查.env文件
    env_file = project_root / '.env'
    if not env_file.exists():
        print("📝 未找到.env文件，正在创建...")
        if create_env_file():
            print("\n💡 请编辑.env文件，设置您的API密钥后重新运行此脚本")
        return
    
    # 测试配置
    if test_env_config():
        print("\n🎉 环境配置测试通过！")
    else:
        print("\n❌ 环境配置测试失败，请检查配置")

if __name__ == "__main__":
    main()
