#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础配置生成器
用于生成基础聊天记录的配置
"""

import json
import datetime
from typing import List, Dict, Any
from ..core.base_generator import ChatGenerator, Character

class ConfigGenerator:
    """基础配置生成器"""
    
    def __init__(self):
        self.characters: List[Character] = []
        self.config: Dict[str, Any] = {}
    
    def interactive_setup(self):
        """交互式配置设置"""
        print("🎯 基础聊天记录生成器配置")
        print("=" * 50)
        
        # 设置角色
        self._setup_characters()
        
        # 设置主题
        self._setup_topic()
        
        # 设置参数
        self._setup_parameters()
        
        # 生成配置
        self._generate_config()
        
        # 运行生成器
        self._run_generator()
    
    def _setup_characters(self):
        """设置角色"""
        print("\n👥 设置角色")
        print("-" * 30)
        
        while True:
            try:
                count = int(input("请输入角色数量 (3-8): "))
                if 3 <= count <= 8:
                    break
                else:
                    print("❌ 角色数量必须在3-8之间")
            except ValueError:
                print("❌ 请输入有效数字")
        
        for i in range(count):
            print(f"\n角色 {i+1}:")
            name = input("  姓名: ").strip()
            nickname = input("  昵称 (可选): ").strip()
            personality = input("  性格特点 (可选): ").strip()
            speaking_style = input("  说话风格 (可选): ").strip()
            
            character = Character(
                name=name,
                nickname=nickname or name,
                personality=personality,
                speaking_style=speaking_style
            )
            self.characters.append(character)
    
    def _setup_topic(self):
        """设置主题"""
        print("\n💬 设置聊天主题")
        print("-" * 30)
        
        self.config['topic'] = input("请输入聊天主题: ").strip()
        self.config['event_context'] = input("请输入事件背景 (可选): ").strip()
    
    def _setup_parameters(self):
        """设置参数"""
        print("\n⚙️ 设置生成参数")
        print("-" * 30)
        
        # 消息数量
        while True:
            try:
                count = int(input("消息数量 (10-100): "))
                if 10 <= count <= 100:
                    self.config['message_count'] = count
                    break
                else:
                    print("❌ 消息数量必须在10-100之间")
            except ValueError:
                print("❌ 请输入有效数字")
        
        # 时长
        while True:
            try:
                duration = float(input("聊天时长 (小时, 0.1-24): "))
                if 0.1 <= duration <= 24:
                    self.config['duration_hours'] = duration
                    break
                else:
                    print("❌ 时长必须在0.1-24小时之间")
            except ValueError:
                print("❌ 请输入有效数字")
        
        # 输出格式
        print("\n输出格式:")
        print("1. QQ格式")
        print("2. 微信格式")
        
        while True:
            choice = input("请选择格式 (1-2): ").strip()
            if choice == "1":
                self.config['format'] = "qq"
                break
            elif choice == "2":
                self.config['format'] = "wechat"
                break
            else:
                print("❌ 请输入1或2")
    
    def _generate_config(self):
        """生成配置"""
        self.config.update({
            'characters': [
                {
                    'name': char.name,
                    'nickname': char.nickname,
                    'personality': char.personality,
                    'speaking_style': char.speaking_style
                }
                for char in self.characters
            ],
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    def _run_generator(self):
        """运行生成器"""
        print("\n🚀 开始生成聊天记录...")
        print("=" * 50)
        
        try:
            generator = ChatGenerator()
            
            # 添加角色
            for char in self.characters:
                generator.add_character(char)
            
            # 设置主题
            generator.set_topic(self.config['topic'])
            if self.config.get('event_context'):
                generator.set_event_context(self.config['event_context'])
            
            # 生成聊天记录
            generator.generate_conversation(
                message_count=self.config['message_count'],
                duration_hours=self.config['duration_hours']
            )
            
            # 保存结果
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/basic_chat_{self.config['format']}_{timestamp}.txt"
            
            generator.save_to_file(filename, format_type=self.config['format'])
            
            print(f"✅ 聊天记录已生成: {filename}")
            print(f"   消息数量: {len(generator.messages)}")
            print(f"   参与角色: {len(generator.characters)}")
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
