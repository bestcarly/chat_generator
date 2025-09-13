#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI配置生成器
用于配置AI聊天记录生成器
"""

import datetime
from typing import Dict, Any
from ..core.ai_generator import AIChatGenerator
from ..config.settings import GOOGLE_AI_API_KEY, DEFAULT_MODEL

class AIConfigGenerator:
    """AI配置生成器"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
    
    def interactive_setup(self):
        """交互式配置设置"""
        print("🤖 AI聊天记录生成器配置")
        print("=" * 50)
        
        # 检查API密钥
        if not self._check_api_key():
            return
        
        # 设置事件
        self._setup_event()
        
        # 设置参数
        self._setup_parameters()
        
        # 运行生成器
        self._run_generator()
    
    def _check_api_key(self):
        """检查API密钥"""
        if not GOOGLE_AI_API_KEY:
            print("❌ 未设置Google AI API密钥")
            print("   请先设置.env文件中的GOOGLE_AI_API_KEY")
            return False
        
        print("✅ API密钥已设置")
        return True
    
    def _setup_event(self):
        """设置事件"""
        print("\n🎯 设置事件")
        print("-" * 30)
        
        self.config['event'] = input("请输入要讨论的事件: ").strip()
        
        if not self.config['event']:
            print("❌ 事件不能为空")
            self._setup_event()
            return
    
    def _setup_parameters(self):
        """设置参数"""
        print("\n⚙️ 设置生成参数")
        print("-" * 30)
        
        # 角色数量
        while True:
            try:
                count = int(input("角色数量 (5-10): "))
                if 5 <= count <= 10:
                    self.config['character_count'] = count
                    break
                else:
                    print("❌ 角色数量必须在5-10之间")
            except ValueError:
                print("❌ 请输入有效数字")
        
        # 消息数量
        while True:
            try:
                count = int(input("消息数量 (20-200): "))
                if 20 <= count <= 200:
                    self.config['message_count'] = count
                    break
                else:
                    print("❌ 消息数量必须在20-200之间")
            except ValueError:
                print("❌ 请输入有效数字")
        
        # 时长
        while True:
            try:
                duration = float(input("聊天时长 (小时, 0.5-12): "))
                if 0.5 <= duration <= 12:
                    self.config['duration_hours'] = duration
                    break
                else:
                    print("❌ 时长必须在0.5-12小时之间")
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
        
        # 实时保存
        save_choice = input("是否启用实时保存? (y/n, 默认y): ").strip().lower()
        self.config['realtime_save'] = save_choice != 'n'
        
        if self.config['realtime_save']:
            while True:
                try:
                    interval = int(input("保存间隔 (条消息, 5-50, 默认10): ") or "10")
                    if 5 <= interval <= 50:
                        self.config['save_interval'] = interval
                        break
                    else:
                        print("❌ 保存间隔必须在5-50之间")
                except ValueError:
                    print("❌ 请输入有效数字")
        else:
            self.config['save_interval'] = 10
    
    def _run_generator(self):
        """运行生成器"""
        print("\n🚀 开始生成AI聊天记录...")
        print("=" * 50)
        
        try:
            generator = AIChatGenerator()
            
            # 设置事件
            generator.input_event(self.config['event'])
            
            # 生成角色
            print("🤖 正在生成AI角色...")
            characters = generator.generate_characters_from_event(self.config['character_count'])
            print(f"✅ 生成了 {len(characters)} 个角色")
            
            # 生成AI聊天记录
            messages = generator.generate_ai_conversation(
                duration_hours=self.config['duration_hours'],
                message_count=self.config['message_count'],
                realtime_save=self.config['realtime_save'],
                save_interval=self.config['save_interval']
            )
            
            # 保存文件
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            generator.save_ai_conversation(messages, f"output/ai_chat_{self.config['format']}_{timestamp}.txt", self.config['format'])
            generator.save_characters_config(f"output/ai_characters_{timestamp}.json")
            
            result = {
                'message_count': len(messages),
                'output_file': f"output/ai_chat_{self.config['format']}_{timestamp}.txt"
            }
            
            if result:
                print("✅ AI聊天记录生成完成!")
                print(f"   事件: {self.config['event']}")
                print(f"   角色数量: {self.config['character_count']}")
                print(f"   消息数量: {result.get('message_count', 0)}")
                print(f"   输出文件: {result.get('output_file', '未知')}")
            else:
                print("❌ AI聊天记录生成失败")
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            print("   请检查API密钥和网络连接")
