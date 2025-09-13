#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天记录生成器快速启动脚本
提供简单的菜单选择不同的运行模式
"""



def show_menu():
    """显示主菜单"""
    print("=" * 60)
    print("🎭 聊天记录生成器")
    print("=" * 60)
    print()
    print("请选择运行模式:")
    print()
    print("1. 🎯 交互式配置 (推荐新手)")
    print("   - 逐步引导设置角色、主题和参数")
    print("   - 适合第一次使用")
    print()
    print("2. ⚡ 快速示例生成")
    print("   - 使用预设角色和主题快速生成")
    print("   - 适合快速体验功能")
    print()
    print("3. 📚 查看使用示例")
    print("   - 运行多个场景的示例")
    print("   - 生成工作、朋友、家庭等不同场景的聊天记录")
    print()
    print("4. 🤖 AI智能聊天生成器")
    print("   - 使用Google AI生成更真实的对话")
    print("   - 基于事件自动生成相关角色")
    print("   - 需要Google AI API密钥")
    print()
    print("5. 📋 策划组织聊天生成器 (NEW!)")
    print("   - 专门用于策划与组织过程的聊天记录")
    print("   - 支持大量消息、完整逻辑链条")
    print("   - 包含多个小事情穿插")
    print()
    print("6. 🔧 测试AI配置")
    print("   - 检查API密钥和依赖包")
    print("   - 验证AI功能是否可用")
    print()
    print("7. 📖 查看帮助文档")
    print("   - 显示详细的使用说明")
    print()
    print("8. 🚪 退出")
    print()


def run_interactive():
    """运行交互式配置"""
    print("启动交互式配置...")
    try:
        from ..utils.config_generator import ConfigGenerator
        config_gen = ConfigGenerator()
        config_gen.interactive_setup()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 config_generator.py 文件存在")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_quick_example():
    """运行快速示例"""
    print("启动快速示例生成...")
    try:
        from ..core.base_generator import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 main.py 文件存在")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_examples():
    """运行使用示例"""
    print("启动使用示例...")
    try:
        from ..examples.basic_example import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 example.py 文件存在")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_ai_generator():
    """运行AI聊天生成器"""
    print("启动AI聊天生成器...")
    try:
        from ..utils.ai_config_generator import AIConfigGenerator
        config_gen = AIConfigGenerator()
        config_gen.interactive_setup()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 ai_config_generator.py 文件存在")
        print("并且已安装 google-generativeai 包")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def run_planning_generator():
    """运行策划组织聊天生成器"""
    print("启动策划组织聊天生成器...")
    try:
        from ..utils.planning_config_generator import PlanningConfigGenerator
        config_gen = PlanningConfigGenerator()
        config_gen.interactive_setup()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 planning_config_generator.py 文件存在")
        print("并且已安装 google-generativeai 包")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def test_ai_config():
    """测试AI配置"""
    print("启动AI配置测试...")
    try:
        from ..utils.test_config import main
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保 test_config.py 文件存在")
    except Exception as e:
        print(f"❌ 运行错误: {e}")


def show_help():
    """显示帮助文档"""
    print("=" * 60)
    print("📖 聊天记录生成器帮助文档")
    print("=" * 60)
    print()
    print("🎯 功能特点:")
    print("• 支持创建多个具有不同性格的角色")
    print("• 可自定义讨论主题和事件背景")
    print("• 支持设置聊天时长和消息数量")
    print("• 生成QQ和微信两种格式的聊天记录")
    print("• 输出为纯文本格式，便于查看和编辑")
    print("• 🤖 AI智能聊天生成器")
    print("  - 使用Google AI生成更真实的对话")
    print("  - 基于事件自动生成相关角色")
    print("  - 支持上下文感知的对话生成")
    print("• 📋 NEW: 策划组织聊天生成器")
    print("  - 专门用于策划与组织过程的聊天记录")
    print("  - 支持大量消息记录（几千条）")
    print("  - 包含完整的策划逻辑和前后因果关系")
    print("  - 支持多个小事情的穿插")
    print()
    print("📁 文件说明:")
    print("• main.py - 核心生成器类")
    print("• config_generator.py - 交互式配置界面")
    print("• ai_chat_generator.py - AI聊天生成器核心")
    print("• ai_config_generator.py - AI配置界面")
    print("• planning_chat_generator.py - 策划组织生成器核心")
    print("• planning_config_generator.py - 策划配置界面")
    print("• example.py - 使用示例")
    print("• start.py - 快速启动脚本")
    print("• README.md - 详细说明文档")
    print()
    print("🚀 快速开始:")
    print("1. 选择 '交互式配置' 进行详细设置")
    print("2. 选择 '快速示例生成' 体验基本功能")
    print("3. 选择 '查看使用示例' 了解不同场景")
    print("4. 选择 'AI智能聊天生成器' 体验AI功能")
    print("5. 选择 '策划组织聊天生成器' 体验策划功能")
    print()
    print("💡 使用技巧:")
    print("• 角色性格会影响消息内容的生成风格")
    print("• 可以设置2-10个角色参与聊天")
    print("• 建议根据实际需求调整消息模板")
    print("• 生成的文件会保存在当前目录")
    print("• AI功能需要Google AI API密钥")
    print()
    print("🔑 AI功能设置:")
    print("• 获取Google AI API密钥: https://makersuite.google.com/app/apikey")
    print("• 修改 config.py 文件中的 GOOGLE_AI_API_KEY 变量")
    print("• 或设置环境变量: export GOOGLE_AI_API_KEY='your_api_key'")
    print()
    print("📞 如需更多帮助，请查看 README.md 文件")
    print()


def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("请输入选项 (1-8): ").strip()
            
            if choice == "1":
                run_interactive()
            elif choice == "2":
                run_quick_example()
            elif choice == "3":
                run_examples()
            elif choice == "4":
                run_ai_generator()
            elif choice == "5":
                run_planning_generator()
            elif choice == "6":
                test_ai_config()
            elif choice == "7":
                show_help()
            elif choice == "8":
                print("👋 感谢使用聊天记录生成器！")
                break
            else:
                print("❌ 无效选项，请输入1-8之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        print("\n" + "=" * 60)
        input("按回车键继续...")
        print()


if __name__ == "__main__":
    main()
