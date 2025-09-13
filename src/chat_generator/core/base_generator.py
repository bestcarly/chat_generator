#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天记录生成器
支持生成类似QQ/微信格式的群聊记录
"""

import random
import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class Character:
    """角色类"""
    name: str
    nickname: str = ""
    avatar: str = ""
    personality: str = ""
    speaking_style: str = ""
    
    def __post_init__(self):
        if not self.nickname:
            self.nickname = self.name


@dataclass
class ChatMessage:
    """聊天消息类"""
    sender: str
    content: str
    timestamp: datetime.datetime
    message_type: str = "text"  # text, image, emoji, etc.


class ChatGenerator:
    """聊天记录生成器"""
    
    def __init__(self):
        self.characters: List[Character] = []
        self.messages: List[ChatMessage] = []
        self.current_topic: str = ""
        self.event_context: str = ""
        
        # 常用表情和语气词
        self.emojis = ["😊", "😂", "😭", "😮", "👍", "👎", "❤️", "💔", "😱", "😤", "🤔", "😴"]
        self.interjections = ["啊", "哦", "嗯", "额", "哈哈", "嘿嘿", "呵呵", "哎", "唉", "哇"]
        
    def add_character(self, character: Character):
        """添加角色"""
        self.characters.append(character)
        
    def set_topic(self, topic: str, event_context: str = ""):
        """设置讨论主题和事件背景"""
        self.current_topic = topic
        self.event_context = event_context
        
    def generate_message_content(self, character: Character, topic: str) -> str:
        """根据角色性格和主题生成消息内容"""
        content_templates = [
            f"关于{topic}，我觉得...",
            f"说到{topic}，我想起...",
            f"我觉得{topic}这个问题...",
            f"对于{topic}，我的看法是...",
            f"你们觉得{topic}怎么样？",
            f"关于{topic}，我有不同的想法...",
        ]
        
        # 根据角色性格调整内容
        if character.personality == "活泼":
            content = random.choice(content_templates) + random.choice(self.emojis)
        elif character.personality == "严肃":
            content = f"关于{topic}，我认为需要认真考虑..."
        elif character.personality == "幽默":
            content = f"哈哈，{topic}这个话题有意思，让我想想..."
        else:
            content = random.choice(content_templates)
            
        # 添加语气词
        if random.random() < 0.3:
            content = random.choice(self.interjections) + "，" + content
            
        return content
        
    def generate_chat_record(self, 
                           duration_hours: float = 1.0, 
                           message_count: int = 50,
                           start_time: datetime.datetime = None) -> List[ChatMessage]:
        """生成聊天记录"""
        if not self.characters:
            raise ValueError("请先添加角色")
            
        if not self.current_topic:
            raise ValueError("请先设置讨论主题")
            
        if start_time is None:
            start_time = datetime.datetime.now() - datetime.timedelta(hours=duration_hours)
            
        self.messages = []
        
        # 生成消息
        for i in range(message_count):
            # 随机选择发送者
            sender = random.choice(self.characters)
            
            # 生成时间戳（在时间范围内随机分布）
            time_progress = i / message_count
            message_time = start_time + datetime.timedelta(
                hours=duration_hours * time_progress + random.uniform(-0.1, 0.1)
            )
            
            # 生成消息内容
            content = self.generate_message_content(sender, self.current_topic)
            
            # 创建消息
            message = ChatMessage(
                sender=sender.name,
                content=content,
                timestamp=message_time
            )
            
            self.messages.append(message)
            
        # 按时间排序
        self.messages.sort(key=lambda x: x.timestamp)
        
        return self.messages
        
    def format_qq_style(self) -> str:
        """格式化为QQ风格"""
        if not self.messages:
            return "暂无聊天记录"
            
        output = []
        output.append("=" * 50)
        output.append(f"群聊记录 - {self.current_topic}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 50)
        output.append("")
        
        current_date = None
        for message in self.messages:
            # 检查是否需要显示日期
            message_date = message.timestamp.date()
            if current_date != message_date:
                current_date = message_date
                output.append(f"\n{current_date.strftime('%Y年%m月%d日')}")
                output.append("-" * 30)
                
            # 格式化时间
            time_str = message.timestamp.strftime("%H:%M:%S")
            
            # 格式化消息
            output.append(f"[{time_str}] {message.sender}: {message.content}")
            
        return "\n".join(output)
        
    def format_wechat_style(self) -> str:
        """格式化为微信风格"""
        if not self.messages:
            return "暂无聊天记录"
            
        output = []
        output.append("=" * 50)
        output.append(f"微信群聊 - {self.current_topic}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 50)
        output.append("")
        
        current_date = None
        for message in self.messages:
            # 检查是否需要显示日期
            message_date = message.timestamp.date()
            if current_date != message_date:
                current_date = message_date
                output.append(f"\n{current_date.strftime('%Y年%m月%d日')}")
                output.append("-" * 30)
                
            # 格式化时间
            time_str = message.timestamp.strftime("%H:%M")
            
            # 格式化消息
            output.append(f"{time_str} {message.sender}\n{message.content}")
            output.append("")
            
        return "\n".join(output)
        
    def save_to_file(self, filename: str, style: str = "qq"):
        """保存聊天记录到文件"""
        if style == "qq":
            content = self.format_qq_style()
        elif style == "wechat":
            content = self.format_wechat_style()
        else:
            raise ValueError("不支持的格式，请使用 'qq' 或 'wechat'")
        
        # 确保目录存在
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"聊天记录已保存到: {filename}")


def create_sample_characters() -> List[Character]:
    """创建示例角色"""
    characters = [
        Character(
            name="张三",
            nickname="小张",
            personality="活泼",
            speaking_style="喜欢用表情符号"
        ),
        Character(
            name="李四",
            nickname="老李",
            personality="严肃",
            speaking_style="说话比较正式"
        ),
        Character(
            name="王五",
            nickname="小王",
            personality="幽默",
            speaking_style="喜欢开玩笑"
        ),
        Character(
            name="赵六",
            nickname="小赵",
            personality="温和",
            speaking_style="说话比较温和"
        )
    ]
    return characters


def main():
    """主函数 - 演示用法"""
    print("聊天记录生成器")
    print("=" * 50)
    
    # 创建生成器实例
    generator = ChatGenerator()
    
    # 添加角色
    characters = create_sample_characters()
    for char in characters:
        generator.add_character(char)
        print(f"添加角色: {char.name} ({char.nickname}) - {char.personality}")
    
    print()
    
    # 设置讨论主题
    topic = "周末聚餐计划"
    event_context = "大家商量周末去哪里聚餐，讨论时间和地点"
    generator.set_topic(topic, event_context)
    print(f"讨论主题: {topic}")
    print(f"事件背景: {event_context}")
    print()
    
    # 生成聊天记录
    print("正在生成聊天记录...")
    messages = generator.generate_chat_record(
        duration_hours=2.0,
        message_count=30,
        start_time=datetime.datetime.now() - datetime.timedelta(hours=2)
    )
    
    print(f"生成了 {len(messages)} 条消息")
    print()
    
    # 显示QQ格式
    print("QQ格式预览:")
    print("-" * 30)
    qq_content = generator.format_qq_style()
    print(qq_content[:500] + "..." if len(qq_content) > 500 else qq_content)
    print()
    
    # 保存文件
    generator.save_to_file("output/chat_record_qq.txt", "qq")
    generator.save_to_file("output/chat_record_wechat.txt", "wechat")
    
    print("生成完成！")


if __name__ == "__main__":
    main()
