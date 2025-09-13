#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目清理脚本
用于清理重构后的旧文件和目录
"""

import os
import shutil
import sys
from pathlib import Path

def cleanup_old_files():
    """清理旧文件"""
    print("🧹 开始清理旧文件...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # 需要清理的旧文件列表
    old_files = [
        "main.py",
        "ai_chat_generator.py", 
        "planning_chat_generator.py",
        "config.py",
        "start.py",
        "example.py",
        "planning_example.py",
        "test_config.py",
        "test_criminal_roles.py",
        "test_default_roles.py",
        "test_json_cleanup.py",
        "test_multiphase.py",
        "config_generator.py",
        "ai_config_generator.py",
        "planning_config_generator.py"
    ]
    
    # 需要清理的旧目录列表
    old_dirs = [
        "config/templates",  # 旧的config目录
        "src/cli",           # 重复的cli目录
        "src/examples"       # 重复的examples目录
    ]
    
    # 清理旧文件
    for file_name in old_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  🗑️  删除文件: {file_name}")
            file_path.unlink()
        else:
            print(f"  ⏭️  文件不存在: {file_name}")
    
    # 清理旧目录
    for dir_name in old_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  🗑️  删除目录: {dir_name}")
            shutil.rmtree(dir_path)
        else:
            print(f"  ⏭️  目录不存在: {dir_name}")
    
    print("✅ 旧文件清理完成！")

def cleanup_duplicate_docs():
    """清理重复的文档文件"""
    print("\n📚 清理重复的文档文件...")
    
    project_root = Path(__file__).parent.parent
    
    # 根目录下的文档文件（应该移动到docs/）
    doc_files = [
        "CONTENT_FILTER_FIX.md",
        "CRIMINAL_ROLES_UPDATE.md", 
        "ERROR_HANDLING.md",
        "MULTIPHASE_UPDATE.md",
        "PLANNING_FEATURES.md",
        "PROJECT_RESTRUCTURE_PLAN.md",
        "REALTIME_SAVE.md",
        "SETUP.md"
    ]
    
    for doc_file in doc_files:
        root_path = project_root / doc_file
        docs_path = project_root / "docs" / doc_file
        
        if root_path.exists() and docs_path.exists():
            print(f"  🗑️  删除重复文档: {doc_file}")
            root_path.unlink()
        elif root_path.exists():
            print(f"  📁 移动文档到docs/: {doc_file}")
            shutil.move(str(root_path), str(docs_path))
    
    print("✅ 文档清理完成！")

def cleanup_output_files():
    """整理输出文件"""
    print("\n📁 整理输出文件...")
    
    project_root = Path(__file__).parent.parent
    
    # 移动根目录下的输出文件到output/
    output_files = [
        "planning_chat_*.txt",
        "planning_config_*.json", 
        "planning_temp_*.txt"
    ]
    
    output_dir = project_root / "output"
    
    # 确保output目录存在
    output_dir.mkdir(exist_ok=True)
    
    for pattern in output_files:
        for file_path in project_root.glob(pattern):
            if file_path.is_file():
                target_dir = output_dir / "temp"
                target_dir.mkdir(exist_ok=True)
                target_path = target_dir / file_path.name
                
                print(f"  📁 移动文件: {file_path.name} -> output/temp/")
                shutil.move(str(file_path), str(target_path))
    
    print("✅ 输出文件整理完成！")

def cleanup_cache():
    """清理缓存文件"""
    print("\n🗂️  清理缓存文件...")
    
    project_root = Path(__file__).parent.parent
    
    # 清理__pycache__目录
    for pycache_dir in project_root.rglob("__pycache__"):
        print(f"  🗑️  删除缓存目录: {pycache_dir.relative_to(project_root)}")
        shutil.rmtree(pycache_dir)
    
    # 清理.pyc文件
    for pyc_file in project_root.rglob("*.pyc"):
        print(f"  🗑️  删除缓存文件: {pyc_file.relative_to(project_root)}")
        pyc_file.unlink()
    
    print("✅ 缓存清理完成！")

def main():
    """主函数"""
    print("🚀 开始项目清理...")
    print("=" * 50)
    
    try:
        cleanup_old_files()
        cleanup_duplicate_docs()
        cleanup_output_files()
        cleanup_cache()
        
        print("\n" + "=" * 50)
        print("🎉 项目清理完成！")
        print("\n📋 清理总结:")
        print("  ✅ 删除了旧的核心文件")
        print("  ✅ 清理了重复的文档文件")
        print("  ✅ 整理了输出文件")
        print("  ✅ 清理了缓存文件")
        print("\n💡 建议:")
        print("  - 运行测试确保功能正常")
        print("  - 更新导入路径")
        print("  - 检查文档链接")
        
    except Exception as e:
        print(f"\n❌ 清理过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
