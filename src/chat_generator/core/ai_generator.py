#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI聊天记录生成器
使用Google AI API生成更真实的多人对话
"""

import os
import json
import time
import random
import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import google.generativeai as genai
from .base_generator import ChatGenerator, Character, ChatMessage
from ..config.settings import GOOGLE_AI_API_KEY, DEFAULT_MODEL


@dataclass
class AICharacter:
    """AI角色类"""
    name: str
    role: str  # 角色身份
    personality: str
    background: str
    expertise: str
    speaking_style: str
    avatar: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "role": self.role,
            "personality": self.personality,
            "background": self.background,
            "expertise": self.expertise,
            "speaking_style": self.speaking_style
        }


class AIChatGenerator:
    """AI聊天记录生成器"""
    
    def __init__(self, api_key: str = None):
        """初始化AI聊天生成器"""
        # 获取API密钥：优先使用传入的，然后是环境变量，最后是配置文件
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY') or GOOGLE_AI_API_KEY
        
        if not self.api_key or self.api_key == "YOUR_GOOGLE_AI_API_KEY_HERE":
            raise ValueError("请设置Google AI API密钥。请修改 config.py 文件中的 GOOGLE_AI_API_KEY 变量")
        
        # 配置Google AI
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(DEFAULT_MODEL)
        
        # 初始化基础生成器
        self.base_generator = ChatGenerator()
        
        # 存储AI角色和对话历史
        self.ai_characters: List[AICharacter] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_event: str = ""
        self.event_context: str = ""
        
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def input_event(self, event: str, context: str = ""):
        """录入事件"""
        self.current_event = event
        self.event_context = context
        print(f"✅ 事件已录入: {event}")
        if context:
            print(f"✅ 事件背景: {context}")
    
    def generate_characters_from_event(self, num_characters: int = 8) -> List[AICharacter]:
        """基于事件生成相关角色"""
        if not self.current_event:
            raise ValueError("请先录入事件")
        
        prompt = f"""
        基于以下事件，生成{num_characters}个不同的角色来参与1：

        事件：{self.current_event}
        背景：{self.event_context if self.event_context else "无特殊背景"}

        请为每个角色生成以下信息：
        1. 姓名（中文）
        2. 角色身份（如：项目经理、设计师、技术专家、用户代表等）
        3. 性格特点（如：理性、感性、幽默、严肃等）
        4. 背景经历（简要描述）
        5. 专业领域（与事件相关的专长）
        6. 说话风格（如：直接、委婉、专业、通俗等）

        请以JSON格式返回，格式如下：
        {{
            "characters": [
                {{
                    "name": "角色姓名",
                    "role": "角色身份",
                    "personality": "性格特点",
                    "background": "背景经历",
                    "expertise": "专业领域",
                    "speaking_style": "说话风格"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # 清理和解析JSON
            response_text = self._clean_json_response(response_text)
            data = json.loads(response_text)
            characters_data = data.get('characters', [])
            
            # 创建AI角色对象
            self.ai_characters = []
            for char_data in characters_data:
                ai_char = AICharacter(
                    name=char_data.get('name', ''),
                    role=char_data.get('role', ''),
                    personality=char_data.get('personality', ''),
                    background=char_data.get('background', ''),
                    expertise=char_data.get('expertise', ''),
                    speaking_style=char_data.get('speaking_style', '')
                )
                self.ai_characters.append(ai_char)
            
            print(f"✅ 成功生成 {len(self.ai_characters)} 个AI角色")
            for char in self.ai_characters:
                print(f"   - {char.name} ({char.role}) - {char.personality}")
            
            return self.ai_characters
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"AI返回的内容: {response_text[:200]}...")
            return self._create_default_characters()
        except Exception as e:
            print(f"❌ 生成角色失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            # 如果AI生成失败，使用默认角色
            return self._create_default_characters()
    
    def _create_default_characters(self) -> List[AICharacter]:
        """创建默认角色（当AI生成失败时使用）"""
        default_chars = [
            AICharacter(
                name="项目负责人",
                role="项目经理",
                personality="理性、有条理",
                background="有多年项目管理经验",
                expertise="项目管理、资源协调",
                speaking_style="直接、专业"
            ),
            AICharacter(
                name="技术专家",
                role="技术顾问",
                personality="严谨、专注",
                background="资深技术专家",
                expertise="技术架构、系统设计",
                speaking_style="专业、详细"
            ),
            AICharacter(
                name="用户代表",
                role="产品经理",
                personality="感性、用户导向",
                background="了解用户需求",
                expertise="用户体验、需求分析",
                speaking_style="温和、关注细节"
            ),
            AICharacter(
                name="设计师",
                role="UI/UX设计师",
                personality="创意、审美敏感",
                background="设计专业背景",
                expertise="界面设计、用户体验",
                speaking_style="创意、形象化"
            )
        ]
        self.ai_characters = default_chars
        return default_chars
    
    def generate_ai_message(self, character: AICharacter, context: str = "") -> str:
        """使用AI生成单个角色的消息"""
        # 构建角色信息
        character_info = f"""
        角色信息：
        - 姓名：{character.name}
        - 身份：{character.role}
        - 性格：{character.personality}
        - 背景：{character.background}
        - 专长：{character.expertise}
        - 说话风格：{character.speaking_style}
        """
        
        # 构建对话历史
        history_text = ""
        if self.conversation_history:
            history_text = "\n最近的对话历史：\n"
            for msg in self.conversation_history[-5:]:  # 只取最近5条
                history_text += f"- {msg['sender']}: {msg['content']}\n"
        
        prompt = f"""
        请基于以下信息生成一条聊天消息：

        {character_info}

        当前讨论事件：{self.current_event}
        事件背景：{self.event_context if self.event_context else "无特殊背景"}
        
        {history_text}
        
        上下文：{context}

        要求：
        1. 消息长度控制在20-80字之间
        2. 符合角色的身份、性格和说话风格
        3. 与当前讨论事件相关
        4. 考虑对话历史，避免重复
        5. 使用中文，自然流畅
        6. 可以包含适当的语气词和表情符号
        7. 不要包含任何标记或前缀，直接输出消息内容

        请生成消息：
        """
        
        try:
            response = self.model.generate_content(prompt)
            message = response.text.strip()
            
            # 清理消息内容
            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]
            
            return message
            
        except Exception as e:
            print(f"❌ 生成消息失败: {e}")
            # 返回默认消息
            return f"关于{self.current_event}，我觉得需要进一步讨论..."
    
    def generate_ai_conversation(self, 
                               duration_hours: float = 1.0,
                               message_count: int = 30,
                               start_time: datetime.datetime = None,
                               realtime_save: bool = True,
                               save_interval: int = 10) -> List[ChatMessage]:
        """生成AI对话"""
        if not self.ai_characters:
            raise ValueError("请先生成角色")
        
        if not self.current_event:
            raise ValueError("请先录入事件")
        
        if start_time is None:
            start_time = datetime.datetime.now() - datetime.timedelta(hours=duration_hours)
        
        self.conversation_history = []
        messages = []
        
        # 实时保存相关变量
        temp_filename_qq = None
        temp_filename_wechat = None
        if realtime_save:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename_qq = f"output/temp/ai_temp_qq_{timestamp}.txt"
            temp_filename_wechat = f"output/temp/ai_temp_wechat_{timestamp}.txt"
            # 创建临时文件头部
            self._create_ai_temp_file_header(temp_filename_qq, "qq")
            self._create_ai_temp_file_header(temp_filename_wechat, "wechat")
        
        print("🤖 开始生成AI对话...")
        if realtime_save:
            print(f"实时保存: 每 {save_interval} 条消息保存一次")
            print(f"临时文件: {temp_filename_qq}, {temp_filename_wechat}")
        
        try:
            for i in range(message_count):
                # 随机选择角色（但避免连续相同角色）
                available_chars = self.ai_characters.copy()
                if messages and len(messages) > 0:
                    last_sender = messages[-1].sender
                    available_chars = [char for char in available_chars if char.name != last_sender]
                
                if not available_chars:
                    available_chars = self.ai_characters
                
                character = random.choice(available_chars)
                
                # 生成时间戳
                time_progress = i / message_count
                message_time = start_time + datetime.timedelta(
                    hours=duration_hours * time_progress + random.uniform(-0.05, 0.05)
                )
                
                # 构建上下文
                context = f"这是第{i+1}条消息，当前已有{len(messages)}条消息"
                
                # 生成AI消息
                print(f"  生成第{i+1}条消息 - {character.name}...")
                content = self.generate_ai_message(character, context)
                
                # 创建消息对象
                message = ChatMessage(
                    sender=character.name,
                    content=content,
                    timestamp=message_time
                )
                
                messages.append(message)
                
                # 添加到对话历史
                self.conversation_history.append({
                    'sender': character.name,
                    'content': content,
                    'timestamp': message_time.isoformat()
                })
                
                # 实时保存
                if realtime_save and (i + 1) % save_interval == 0:
                    self._append_to_ai_temp_files(messages[-save_interval:], temp_filename_qq, temp_filename_wechat)
                    print(f"  💾 已保存 {i+1} 条消息到临时文件")
                
                # 添加延迟避免API限制
                time.sleep(0.5)
            
            # 保存剩余的消息
            if realtime_save and len(messages) % save_interval != 0:
                remaining_messages = messages[-(len(messages) % save_interval):]
                self._append_to_ai_temp_files(remaining_messages, temp_filename_qq, temp_filename_wechat)
            
            # 按时间排序
            messages.sort(key=lambda x: x.timestamp)
            
            print(f"✅ 成功生成 {len(messages)} 条AI对话")
            return messages
            
        except KeyboardInterrupt:
            print(f"\n⚠️ 用户中断生成，已保存 {len(messages)} 条消息")
            if realtime_save and messages:
                # 保存已生成的消息
                self._append_to_ai_temp_files(messages, temp_filename_qq, temp_filename_wechat)
                print(f"💾 已保存到临时文件: {temp_filename_qq}, {temp_filename_wechat}")
            return messages
        except Exception as e:
            print(f"\n❌ 生成过程中出现错误: {e}")
            if realtime_save and messages:
                # 保存已生成的消息
                self._append_to_ai_temp_files(messages, temp_filename_qq, temp_filename_wechat)
                print(f"💾 已保存到临时文件: {temp_filename_qq}, {temp_filename_wechat}")
            raise
    
    def save_ai_conversation(self, messages: List[ChatMessage], 
                           filename: str, style: str = "qq"):
        """保存AI对话到文件"""
        if style == "qq":
            content = self._format_qq_style(messages)
        elif style == "wechat":
            content = self._format_wechat_style(messages)
        else:
            raise ValueError("不支持的格式，请使用 'qq' 或 'wechat'")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ AI对话已保存到: {filename}")
    
    def _format_qq_style(self, messages: List[ChatMessage]) -> str:
        """格式化为QQ风格"""
        output = []
        output.append("=" * 50)
        output.append(f"AI群聊记录 - {self.current_event}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 50)
        output.append("")
        
        current_date = None
        for message in messages:
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
    
    def _format_wechat_style(self, messages: List[ChatMessage]) -> str:
        """格式化为微信风格"""
        output = []
        output.append("=" * 50)
        output.append(f"AI微信群聊 - {self.current_event}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 50)
        output.append("")
        
        current_date = None
        for message in messages:
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
    
    def save_characters_config(self, filename: str = "ai_characters.json"):
        """保存AI角色配置"""
        config = {
            "event": self.current_event,
            "event_context": self.event_context,
            "characters": [char.to_dict() for char in self.ai_characters]
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ AI角色配置已保存到: {filename}")
    
    def _clean_json_response(self, response_text: str) -> str:
        """清理AI返回的JSON响应"""
        # 移除markdown代码块标记
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        elif response_text.startswith('```'):
            response_text = response_text[3:]
        
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # 移除首尾空白
        response_text = response_text.strip()
        
        # 如果响应为空或不是JSON格式，返回默认结构
        if not response_text or not response_text.startswith('{'):
            print("⚠️ AI返回的内容不是有效的JSON格式，使用默认数据")
            return '{"characters": []}'
        
        return response_text
    
    def _create_ai_temp_file_header(self, filename: str, style: str):
        """创建AI临时文件头部"""
        output = []
        output.append("=" * 50)
        if style == "qq":
            output.append(f"AI群聊记录 - {self.current_event} (实时保存)")
        else:
            output.append(f"AI微信群聊 - {self.current_event} (实时保存)")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 50)
        output.append("")
        output.append("💾 实时保存中，请勿手动编辑此文件...")
        output.append("")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output))
    
    def _append_to_ai_temp_files(self, messages: List[ChatMessage], 
                                qq_filename: str, wechat_filename: str):
        """追加消息到AI临时文件"""
        if not messages:
            return
        
        # QQ格式
        qq_lines = []
        for message in messages:
            time_str = message.timestamp.strftime("%H:%M:%S")
            qq_lines.append(f"[{time_str}] {message.sender}: {message.content}")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(qq_filename), exist_ok=True)
        os.makedirs(os.path.dirname(wechat_filename), exist_ok=True)
        
        with open(qq_filename, 'a', encoding='utf-8') as f:
            f.write("\n".join(qq_lines) + "\n")
        
        # 微信格式
        wechat_lines = []
        for message in messages:
            time_str = message.timestamp.strftime("%H:%M")
            wechat_lines.append(f"{time_str} {message.sender}\n{message.content}\n")
        
        with open(wechat_filename, 'a', encoding='utf-8') as f:
            f.write("\n".join(wechat_lines))
    
    def finalize_ai_temp_files(self, temp_qq_filename: str, temp_wechat_filename: str,
                              final_qq_filename: str, final_wechat_filename: str):
        """完成AI临时文件，重命名为最终文件"""
        import shutil
        
        if os.path.exists(temp_qq_filename):
            shutil.move(temp_qq_filename, final_qq_filename)
            print(f"✅ AI QQ格式文件已保存到: {final_qq_filename}")
        
        if os.path.exists(temp_wechat_filename):
            shutil.move(temp_wechat_filename, final_wechat_filename)
            print(f"✅ AI 微信格式文件已保存到: {final_wechat_filename}")
    
    def load_characters_config(self, filename: str = "ai_characters.json"):
        """加载AI角色配置"""
        if not os.path.exists(filename):
            print(f"❌ 配置文件不存在: {filename}")
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.current_event = config.get("event", "")
            self.event_context = config.get("event_context", "")
            
            self.ai_characters = []
            for char_data in config.get("characters", []):
                ai_char = AICharacter(
                    name=char_data["name"],
                    role=char_data["role"],
                    personality=char_data["personality"],
                    background=char_data["background"],
                    expertise=char_data["expertise"],
                    speaking_style=char_data["speaking_style"]
                )
                self.ai_characters.append(ai_char)
            
            print(f"✅ AI角色配置已从 {filename} 加载")
            return True
            
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            return False


def main():
    """主函数 - 演示AI聊天生成器"""
    print("🤖 AI聊天记录生成器演示")
    print("=" * 50)
    
    try:
        # 创建AI生成器（使用代码中的API密钥）
        ai_generator = AIChatGenerator()
        
        # 录入事件
        event = "公司年会策划"
        context = "需要策划一个有趣的公司年会，包括节目安排、场地选择、预算分配等"
        ai_generator.input_event(event, context)
        
        # 生成角色
        characters = ai_generator.generate_characters_from_event(6)
        
        # 生成对话
        messages = ai_generator.generate_ai_conversation(
            duration_hours=1.5,
            message_count=25
        )
        
        # 保存文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ai_generator.save_ai_conversation(messages, f"output/ai_chat_qq_{timestamp}.txt", "qq")
        ai_generator.save_ai_conversation(messages, f"output/ai_chat_wechat_{timestamp}.txt", "wechat")
        
        # 保存角色配置
        ai_generator.save_characters_config(f"output/ai_characters_{timestamp}.json")
        
        print("\n🎉 AI聊天记录生成完成！")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")


if __name__ == "__main__":
    main()
