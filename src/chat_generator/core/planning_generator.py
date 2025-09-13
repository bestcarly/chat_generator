#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策划组织聊天记录生成器
专门用于生成完整的策划与组织过程的聊天记录
支持大量消息、完整逻辑链条、多个小事情穿插
"""

import os
import json
import time
import random
import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import google.generativeai as genai
from .base_generator import ChatGenerator, Character, ChatMessage
from ..config.settings import GOOGLE_AI_API_KEY, DEFAULT_MODEL


@dataclass
class PlanningCharacter:
    """策划角色类"""
    name: str
    role: str  # 角色身份
    department: str  # 部门
    level: str  # 级别（高层、中层、基层）
    expertise: List[str]  # 专业领域
    personality: str
    speaking_style: str
    responsibilities: List[str]  # 职责范围
    decision_power: str  # 决策权限（高、中、低）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "level": self.level,
            "expertise": self.expertise,
            "personality": self.personality,
            "speaking_style": self.speaking_style,
            "responsibilities": self.responsibilities,
            "decision_power": self.decision_power
        }


@dataclass
class PlanningPhase:
    """策划阶段"""
    name: str
    description: str
    duration_hours: float
    key_tasks: List[str]
    deliverables: List[str]
    dependencies: List[str]  # 依赖的前置阶段


@dataclass
class SubEvent:
    """子事件/小事情"""
    name: str
    description: str
    urgency: str  # 紧急程度
    impact: str  # 影响程度
    related_phase: str  # 相关阶段
    trigger_conditions: List[str]  # 触发条件


class PlanningChatGenerator:
    """策划组织聊天记录生成器"""
    
    def __init__(self, api_key: str = None):
        """初始化策划聊天生成器"""
        # 获取API密钥
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY') or GOOGLE_AI_API_KEY
        
        if not self.api_key or self.api_key == "YOUR_GOOGLE_AI_API_KEY_HERE":
            raise ValueError("请设置Google AI API密钥。请修改 config.py 文件中的 GOOGLE_AI_API_KEY 变量")
        
        # 配置Google AI
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(DEFAULT_MODEL)
        
        # 策划相关数据
        self.main_event: str = ""
        self.event_context: str = ""
        self.planning_characters: List[PlanningCharacter] = []
        self.planning_phases: List[PlanningPhase] = []
        self.sub_events: List[SubEvent] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_phase: str = ""
        self.phase_progress: Dict[str, float] = {}  # 各阶段进度
        self.decisions_made: List[Dict[str, Any]] = []  # 已做决策
        self.issues_raised: List[Dict[str, Any]] = []  # 提出的问题
        
        # 策划阶段模板
        self.default_phases = [
            # 策划阶段
            PlanningPhase(
                name="踩点摸底",
                description="了解目标情况，收集情报信息",
                duration_hours=8.0,
                key_tasks=["目标踩点", "收集情报", "分析形势", "评估风险"],
                deliverables=["踩点报告", "情报汇总", "风险评估"],
                dependencies=[]
            ),
            PlanningPhase(
                name="制定方案",
                description="制定具体的行动计划",
                duration_hours=12.0,
                key_tasks=["方案设计", "路线规划", "人员安排", "时间安排"],
                deliverables=["行动方案", "路线图", "人员分工"],
                dependencies=["踩点摸底"]
            ),
            PlanningPhase(
                name="人员准备",
                description="安排人手，分配任务",
                duration_hours=16.0,
                key_tasks=["人员召集", "任务分配", "装备准备", "联络安排"],
                deliverables=["人员名单", "任务分工", "装备清单", "联络方式"],
                dependencies=["制定方案"]
            ),
            PlanningPhase(
                name="物资准备",
                description="准备行动所需的物资装备",
                duration_hours=10.0,
                key_tasks=["装备采购", "工具准备", "车辆安排", "通讯设备"],
                deliverables=["装备清单", "工具清单", "车辆安排", "通讯设备"],
                dependencies=["人员准备"]
            ),
            PlanningPhase(
                name="行动准备",
                description="最后的行动前准备",
                duration_hours=6.0,
                key_tasks=["最终检查", "应急预案", "撤退路线", "善后安排"],
                deliverables=["检查清单", "应急预案", "撤退路线", "善后方案"],
                dependencies=["物资准备"]
            ),
            # 施行阶段
            PlanningPhase(
                name="开始行动",
                description="正式开始执行犯罪行动",
                duration_hours=4.0,
                key_tasks=["按计划行动", "实时监控", "应对突发情况", "保持联络"],
                deliverables=["行动进展", "现场情况", "问题反馈"],
                dependencies=["行动准备"]
            ),
            PlanningPhase(
                name="行动执行",
                description="执行具体的犯罪行动",
                duration_hours=6.0,
                key_tasks=["执行计划", "处理目标", "收集财物", "清理现场"],
                deliverables=["行动结果", "财物清单", "现场清理"],
                dependencies=["开始行动"]
            ),
            PlanningPhase(
                name="撤退转移",
                description="行动完成后的撤退和转移",
                duration_hours=3.0,
                key_tasks=["按撤退路线撤离", "分散转移", "销毁证据", "联络确认"],
                deliverables=["撤退报告", "安全确认", "证据销毁"],
                dependencies=["行动执行"]
            ),
            # 应对阶段
            PlanningPhase(
                name="被发现应对",
                description="行动被发现后的紧急应对",
                duration_hours=2.0,
                key_tasks=["评估暴露程度", "制定应对策略", "通知相关人员", "准备应对措施"],
                deliverables=["暴露评估", "应对方案", "通知记录"],
                dependencies=["撤退转移"]
            ),
            PlanningPhase(
                name="外部侦破应对",
                description="应对外部部门的侦破和抓捕",
                duration_hours=8.0,
                key_tasks=["监控外部动向", "调整藏身地点", "销毁证据", "准备应对"],
                deliverables=["外部动向报告", "藏身安排", "证据销毁记录"],
                dependencies=["被发现应对"]
            ),
            PlanningPhase(
                name="抓捕应对",
                description="应对外部抓捕行动",
                duration_hours=4.0,
                key_tasks=["应对抓捕", "保护同伙", "销毁证据", "准备后路"],
                deliverables=["应对记录", "同伙保护", "证据销毁"],
                dependencies=["外部侦破应对"]
            ),
            PlanningPhase(
                name="善后处理",
                description="最后的善后处理工作",
                duration_hours=6.0,
                key_tasks=["处理剩余问题", "安排后路", "清理痕迹", "总结教训"],
                deliverables=["善后报告", "后路安排", "清理记录", "经验总结"],
                dependencies=["抓捕应对"]
            )
        ]
    
    def input_planning_event(self, event: str, context: str = ""):
        """录入策划事件"""
        self.main_event = event
        self.event_context = context
        print(f"✅ 策划事件已录入: {event}")
        if context:
            print(f"✅ 事件背景: {context}")
    
    def generate_planning_characters(self, num_characters: int = 8) -> List[PlanningCharacter]:
        """生成策划团队成员"""
        if not self.main_event:
            raise ValueError("请先录入策划事件")
        
        prompt = f"""
        基于以下组织活动事件，生成{num_characters}个不同的组织成员来参与策划：

        事件：{self.main_event}
        背景：{self.event_context if self.event_context else "无特殊背景"}

        请为每个角色生成以下信息：
        1. 姓名（中文，使用常见的市井名字，如：强哥、阿龙、老六等）
        2. 角色身份（如：负责人、参谋、执行员、联络人、技术员、后勤等）
        3. 部门（如：行动组、后勤组、情报组、技术组等）
        4. 级别（负责人、骨干、成员）
        5. 专业领域（列表，如：执行任务、技术操作、联络沟通、后勤保障等）
        6. 性格特点（如：果断、狡猾、冲动、胆小、贪婪等）
        7. 说话风格（如：粗俗直接、带脏话、方言、威胁性等）
        8. 职责范围（列表，如：指挥行动、技术操作、联络沟通、后勤保障等）
        9. 决策权限（高、中、低）

        要求：
        - 文化程度不高，说话粗俗、市井范儿十足
        - 有专业人士也有执行人员，三教九流都有
        - 不要过于职业化，要符合市井人物的真实情况
        - 说话风格要粗俗、直接、带脏话或方言

        请以JSON格式返回，格式如下：
        {{
            "characters": [
                {{
                    "name": "角色姓名",
                    "role": "角色身份",
                    "department": "部门",
                    "level": "级别",
                    "expertise": ["专业领域1", "专业领域2"],
                    "personality": "性格特点",
                    "speaking_style": "说话风格",
                    "responsibilities": ["职责1", "职责2"],
                    "decision_power": "决策权限"
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
            
            # 创建策划角色对象
            self.planning_characters = []
            for char_data in characters_data:
                planning_char = PlanningCharacter(
                    name=char_data.get('name', ''),
                    role=char_data.get('role', ''),
                    department=char_data.get('department', ''),
                    level=char_data.get('level', ''),
                    expertise=char_data.get('expertise', []),
                    personality=char_data.get('personality', ''),
                    speaking_style=char_data.get('speaking_style', ''),
                    responsibilities=char_data.get('responsibilities', []),
                    decision_power=char_data.get('decision_power', '')
                )
                self.planning_characters.append(planning_char)
            
            print(f"✅ 成功生成 {len(self.planning_characters)} 个策划团队成员")
            for char in self.planning_characters:
                print(f"   - {char.name} ({char.role}) - {char.department} - {char.level}")
            
            return self.planning_characters
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"AI返回的内容: {response_text[:200]}...")
            return self._create_default_planning_characters()
        except Exception as e:
            print(f"❌ 生成角色失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            return self._create_default_planning_characters()
    
    def _create_default_planning_characters(self) -> List[PlanningCharacter]:
        """创建默认犯罪组织角色"""
        default_chars = [
            PlanningCharacter(
                name="强哥",
                role="老大",
                department="总指挥",
                level="老大",
                expertise=["指挥行动", "笼络人心", "处理关系"],
                personality="心狠手辣、有威信、善于笼络人心",
                speaking_style="粗俗直接、带脏话、有威慑力",
                responsibilities=["指挥行动", "分配任务", "处理纠纷"],
                decision_power="高"
            ),
            PlanningCharacter(
                name="阿龙",
                role="军师",
                department="情报组",
                level="骨干",
                expertise=["出谋划策", "收集情报", "分析形势"],
                personality="狡猾、多疑、善于算计",
                speaking_style="阴阳怪气、话里有话",
                responsibilities=["制定计划", "收集情报", "分析风险"],
                decision_power="中"
            ),
            PlanningCharacter(
                name="老六",
                role="打手",
                department="行动组",
                level="骨干",
                expertise=["打架斗殴", "威胁恐吓", "执行任务"],
                personality="好勇斗狠、冲动、忠诚",
                speaking_style="粗鲁、威胁性、带脏话",
                responsibilities=["执行任务", "威胁恐吓", "保护老大"],
                decision_power="低"
            ),
            PlanningCharacter(
                name="小陈",
                role="技术员",
                department="技术组",
                level="马仔",
                expertise=["技术操作", "设备维护", "网络技术"],
                personality="内向、技术宅、胆小",
                speaking_style="结巴、技术术语、不自信",
                responsibilities=["技术操作", "设备维护", "网络支持"],
                decision_power="低"
            ),
            PlanningCharacter(
                name="阿花",
                role="联络人",
                department="后勤组",
                level="马仔",
                expertise=["联络沟通", "后勤保障", "信息传递"],
                personality="圆滑、善于交际、贪财",
                speaking_style="油嘴滑舌、奉承话多",
                responsibilities=["联络沟通", "后勤保障", "信息传递"],
                decision_power="低"
            ),
            PlanningCharacter(
                name="大熊",
                role="打手",
                department="行动组",
                level="马仔",
                expertise=["打架斗殴", "威胁恐吓", "看场子"],
                personality="四肢发达、头脑简单、忠诚",
                speaking_style="粗鲁、简单直接、带脏话",
                responsibilities=["看场子", "威胁恐吓", "执行任务"],
                decision_power="低"
            )
        ]
        self.planning_characters = default_chars
        return default_chars
    
    def generate_planning_phases(self) -> List[PlanningPhase]:
        """生成策划阶段"""
        if not self.main_event:
            raise ValueError("请先录入策划事件")
        
        # 使用默认阶段，但可以根据事件调整
        self.planning_phases = self.default_phases.copy()
        
        print(f"✅ 生成 {len(self.planning_phases)} 个策划阶段:")
        for phase in self.planning_phases:
            print(f"   - {phase.name}: {phase.description}")
        
        return self.planning_phases
    
    def generate_sub_events(self, num_sub_events: int = 5) -> List[SubEvent]:
        """生成子事件/小事情"""
        if not self.main_event:
            raise ValueError("请先录入策划事件")
        
        prompt = f"""
        基于以下组织活动事件，生成{num_sub_events}个可能出现的子事件或小事情：

        主事件：{self.main_event}
        背景：{self.event_context if self.event_context else "无特殊背景"}

        这些子事件应该包括：
        1. 策划阶段问题（如：目标变更、人员变动、装备丢失等）
        2. 施行阶段问题（如：行动受阻、目标反应、设备故障等）
        3. 应对阶段问题（如：被发现、外部介入、证据暴露等）
        4. 外部因素（如：外部巡逻、目击者出现、天气变化等）
        5. 内部问题（如：内讧、背叛、人员不足等）
        6. 执行细节（如：路线问题、时间延误、技术故障等）

        请为每个子事件生成：
        1. 事件名称
        2. 事件描述
        3. 紧急程度（高、中、低）
        4. 影响程度（高、中、低）
        5. 相关阶段（踩点摸底、制定方案、人员准备、物资准备、行动准备、开始行动、行动执行、撤退转移、被发现应对、外部侦破应对、抓捕应对、善后处理）
        6. 触发条件（列表）

        请以JSON格式返回：
        {{
            "sub_events": [
                {{
                    "name": "事件名称",
                    "description": "事件描述",
                    "urgency": "紧急程度",
                    "impact": "影响程度",
                    "related_phase": "相关阶段",
                    "trigger_conditions": ["触发条件1", "触发条件2"]
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
            sub_events_data = data.get('sub_events', [])
            
            # 创建子事件对象
            self.sub_events = []
            for event_data in sub_events_data:
                sub_event = SubEvent(
                    name=event_data.get('name', ''),
                    description=event_data.get('description', ''),
                    urgency=event_data.get('urgency', ''),
                    impact=event_data.get('impact', ''),
                    related_phase=event_data.get('related_phase', ''),
                    trigger_conditions=event_data.get('trigger_conditions', [])
                )
                self.sub_events.append(sub_event)
            
            print(f"✅ 成功生成 {len(self.sub_events)} 个子事件:")
            for event in self.sub_events:
                print(f"   - {event.name} ({event.urgency}紧急, {event.impact}影响)")
            
            return self.sub_events
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"AI返回的内容: {response_text[:200]}...")
            return self._create_default_sub_events()
        except Exception as e:
            print(f"❌ 生成子事件失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            return self._create_default_sub_events()
    
    def _create_default_sub_events(self) -> List[SubEvent]:
        """创建默认子事件"""
        default_events = [
            # 策划阶段事件
            SubEvent(
                name="目标变更",
                description="原定目标情况发生变化，需要重新踩点",
                urgency="高",
                impact="高",
                related_phase="踩点摸底",
                trigger_conditions=["目标监控", "情报更新"]
            ),
            SubEvent(
                name="人员变动",
                description="有成员被外部人员带走，需要重新安排人手",
                urgency="高",
                impact="中",
                related_phase="人员准备",
                trigger_conditions=["人员确认", "风险评估"]
            ),
            SubEvent(
                name="装备丢失",
                description="重要装备丢失或损坏，需要重新准备",
                urgency="中",
                impact="中",
                related_phase="物资准备",
                trigger_conditions=["装备检查", "物资盘点"]
            ),
            SubEvent(
                name="外部巡逻",
                description="目标区域出现外部巡逻，需要调整时间",
                urgency="高",
                impact="高",
                related_phase="制定方案",
                trigger_conditions=["情报收集", "风险评估"]
            ),
            SubEvent(
                name="内讧冲突",
                description="团队成员发生内讧，影响行动执行",
                urgency="中",
                impact="中",
                related_phase="人员准备",
                trigger_conditions=["人员确认", "团队协调"]
            ),
            # 施行阶段事件
            SubEvent(
                name="行动受阻",
                description="行动过程中遇到意外阻碍，无法按计划进行",
                urgency="高",
                impact="高",
                related_phase="行动执行",
                trigger_conditions=["行动监控", "现场反馈"]
            ),
            SubEvent(
                name="目标反应",
                description="目标对象进行反应，增加了行动难度",
                urgency="高",
                impact="中",
                related_phase="行动执行",
                trigger_conditions=["现场情况", "目标反应"]
            ),
            SubEvent(
                name="设备故障",
                description="关键设备出现故障，影响行动效果",
                urgency="中",
                impact="中",
                related_phase="开始行动",
                trigger_conditions=["设备检查", "使用反馈"]
            ),
            SubEvent(
                name="撤退受阻",
                description="撤退过程中遇到阻碍，无法按原计划撤离",
                urgency="高",
                impact="高",
                related_phase="撤退转移",
                trigger_conditions=["撤退监控", "路线检查"]
            ),
            # 应对阶段事件
            SubEvent(
                name="被发现",
                description="行动被目击者或监控发现，暴露了身份",
                urgency="高",
                impact="高",
                related_phase="被发现应对",
                trigger_conditions=["目击报告", "监控发现"]
            ),
            SubEvent(
                name="外部介入",
                description="外部开始介入调查，加大了风险",
                urgency="高",
                impact="高",
                related_phase="外部侦破应对",
                trigger_conditions=["外部调查", "案件立案"]
            ),
            SubEvent(
                name="证据暴露",
                description="重要证据被外部发现，增加了被抓风险",
                urgency="高",
                impact="高",
                related_phase="外部侦破应对",
                trigger_conditions=["证据检查", "现场勘查"]
            ),
            SubEvent(
                name="抓捕行动",
                description="外部开始实施抓捕行动，需要紧急应对",
                urgency="高",
                impact="高",
                related_phase="抓捕应对",
                trigger_conditions=["抓捕通知", "外部行动"]
            ),
            SubEvent(
                name="同伙被抓",
                description="有同伙被外部抓获，可能供出其他人",
                urgency="高",
                impact="高",
                related_phase="抓捕应对",
                trigger_conditions=["抓捕报告", "人员确认"]
            )
        ]
        self.sub_events = default_events
        return default_events
    
    def get_current_phase(self, progress: float) -> str:
        """根据进度获取当前阶段"""
        total_duration = sum(phase.duration_hours for phase in self.planning_phases)
        current_time = progress * total_duration
        
        accumulated_time = 0
        for phase in self.planning_phases:
            accumulated_time += phase.duration_hours
            if current_time <= accumulated_time:
                return phase.name
        
        return self.planning_phases[-1].name
    
    def should_trigger_sub_event(self, current_phase: str, message_count: int) -> Optional[SubEvent]:
        """判断是否应该触发子事件"""
        # 每50-100条消息随机触发一个子事件
        if message_count > 0 and message_count % random.randint(50, 100) == 0:
            # 选择与当前阶段相关的子事件
            related_events = [event for event in self.sub_events if event.related_phase == current_phase]
            if related_events:
                return random.choice(related_events)
        
        return None
    
    def generate_planning_message(self, character: PlanningCharacter, 
                                current_phase: str, context: Dict[str, Any]) -> str:
        """生成策划消息"""
        # 构建角色信息
        character_info = f"""
        角色信息：
        - 姓名：{character.name}
        - 身份：{character.role}
        - 部门：{character.department}
        - 级别：{character.level}
        - 专业领域：{', '.join(character.expertise)}
        - 性格：{character.personality}
        - 说话风格：{character.speaking_style}
        - 职责：{', '.join(character.responsibilities)}
        - 决策权限：{character.decision_power}
        """
        
        # 构建当前阶段信息
        current_phase_info = ""
        for phase in self.planning_phases:
            if phase.name == current_phase:
                current_phase_info = f"""
                当前阶段：{phase.name}
                阶段描述：{phase.description}
                关键任务：{', '.join(phase.key_tasks)}
                交付物：{', '.join(phase.deliverables)}
                """
                break
        
        # 构建对话历史
        history_text = ""
        if self.conversation_history:
            history_text = "\n最近的对话历史：\n"
            for msg in self.conversation_history[-3:]:  # 只取最近3条
                history_text += f"- {msg['sender']}: {msg['content']}\n"
        
        # 构建上下文信息
        context_text = ""
        if context.get('sub_event'):
            sub_event = context['sub_event']
            context_text = f"""
            当前子事件：{sub_event.name}
            事件描述：{sub_event.description}
            紧急程度：{sub_event.urgency}
            影响程度：{sub_event.impact}
            """
        
        prompt = f"""
        请基于以下信息生成一条组织活动相关的聊天消息：

        {character_info}

        主活动事件：{self.main_event}
        事件背景：{self.event_context if self.event_context else "无特殊背景"}
        
        {current_phase_info}
        
        {history_text}
        
        {context_text}
        
        上下文：{context.get('general_context', '')}

        要求：
        1. 消息长度控制在30-100字之间
        2. 符合角色的身份、级别、专业领域和说话风格
        3. 与当前策划阶段相关，体现组织活动的特点
        4. 考虑对话历史，避免重复
        5. 使用中文，自然流畅，符合市井人物的语言特点
        6. 体现策划过程的逻辑性和现实性
        7. 如果有子事件，要体现对子事件的响应
        8. 不要包含任何标记或前缀，直接输出消息内容
        9. 说话要粗俗、直接、带脏话或方言，符合文化程度不高的特点
        10. 不要过于职业化，要符合市井人物的真实情况

        消息类型可以是：
        - 任务分配和进度汇报
        - 问题提出和解决方案讨论
        - 决策制定和执行确认
        - 资源协调和风险控制
        - 阶段总结和下一步规划
        - 行动执行和现场反馈
        - 应对措施和紧急处理
        - 外部动向和风险评估
        - 痕迹清理和善后处理
        - 团队保护和后路安排

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
            return f"关于{current_phase}阶段，我需要进一步确认..."
    
    def generate_planning_conversation(self, 
                                     total_duration_hours: float = 48.0,
                                     target_message_count: int = 2000,
                                     start_time: datetime.datetime = None,
                                     realtime_save: bool = True,
                                     save_interval: int = 10) -> List[ChatMessage]:
        """生成策划组织对话"""
        if not self.planning_characters:
            raise ValueError("请先生成策划团队成员")
        
        if not self.main_event:
            raise ValueError("请先录入策划事件")
        
        if start_time is None:
            start_time = datetime.datetime.now() - datetime.timedelta(hours=total_duration_hours)
        
        # 生成策划阶段和子事件
        self.generate_planning_phases()
        self.generate_sub_events()
        
        self.conversation_history = []
        messages = []
        self.phase_progress = {}
        self.decisions_made = []
        self.issues_raised = []
        
        # 实时保存相关变量
        temp_filename_qq = None
        temp_filename_wechat = None
        if realtime_save:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename_qq = f"output/temp/planning_temp_qq_{timestamp}.txt"
            temp_filename_wechat = f"output/temp/planning_temp_wechat_{timestamp}.txt"
            # 创建临时文件头部
            self._create_temp_file_header(temp_filename_qq, "qq")
            self._create_temp_file_header(temp_filename_wechat, "wechat")
        
        print("🤖 开始生成策划组织对话...")
        print(f"目标消息数量: {target_message_count}")
        print(f"预计时长: {total_duration_hours} 小时")
        if realtime_save:
            print(f"实时保存: 每 {save_interval} 条消息保存一次")
            print(f"临时文件: {temp_filename_qq}, {temp_filename_wechat}")
        
        try:
            for i in range(target_message_count):
                # 计算当前进度
                progress = i / target_message_count
                current_phase = self.get_current_phase(progress)
                
                # 更新阶段进度
                if current_phase not in self.phase_progress:
                    self.phase_progress[current_phase] = 0.0
                self.phase_progress[current_phase] = progress
                
                # 随机选择角色（避免连续相同角色）
                available_chars = self.planning_characters.copy()
                if messages and len(messages) > 0:
                    last_sender = messages[-1].sender
                    available_chars = [char for char in available_chars if char.name != last_sender]
                
                if not available_chars:
                    available_chars = self.planning_characters
                
                character = random.choice(available_chars)
                
                # 生成时间戳
                time_progress = i / target_message_count
                message_time = start_time + datetime.timedelta(
                    hours=total_duration_hours * time_progress + random.uniform(-0.1, 0.1)
                )
                
                # 判断是否触发子事件
                sub_event = self.should_trigger_sub_event(current_phase, i)
                
                # 构建上下文
                context = {
                    'general_context': f"第{i+1}条消息，当前进度{progress:.1%}",
                    'current_phase': current_phase,
                    'sub_event': sub_event
                }
                
                # 生成策划消息
                if i % 100 == 0:  # 每100条消息显示一次进度
                    print(f"  生成进度: {i+1}/{target_message_count} ({progress:.1%}) - 当前阶段: {current_phase}")
                
                content = self.generate_planning_message(character, current_phase, context)
                
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
                    'timestamp': message_time.isoformat(),
                    'phase': current_phase,
                    'sub_event': sub_event.name if sub_event else None
                })
                
                # 实时保存
                if realtime_save and (i + 1) % save_interval == 0:
                    self._append_to_temp_files(messages[-save_interval:], temp_filename_qq, temp_filename_wechat)
                    print(f"  💾 已保存 {i+1} 条消息到临时文件")
                
                # 添加延迟避免API限制
                time.sleep(0.3)
            
            # 保存剩余的消息
            if realtime_save and len(messages) % save_interval != 0:
                remaining_messages = messages[-(len(messages) % save_interval):]
                self._append_to_temp_files(remaining_messages, temp_filename_qq, temp_filename_wechat)
            
            # 按时间排序
            messages.sort(key=lambda x: x.timestamp)
            
            print(f"✅ 成功生成 {len(messages)} 条策划组织对话")
            return messages
            
        except KeyboardInterrupt:
            print(f"\n⚠️ 用户中断生成，已保存 {len(messages)} 条消息")
            if realtime_save and messages:
                # 保存已生成的消息
                self._append_to_temp_files(messages, temp_filename_qq, temp_filename_wechat)
                print(f"💾 已保存到临时文件: {temp_filename_qq}, {temp_filename_wechat}")
            return messages
        except Exception as e:
            print(f"\n❌ 生成过程中出现错误: {e}")
            if realtime_save and messages:
                # 保存已生成的消息
                self._append_to_temp_files(messages, temp_filename_qq, temp_filename_wechat)
                print(f"💾 已保存到临时文件: {temp_filename_qq}, {temp_filename_wechat}")
            raise
    
    def save_planning_conversation(self, messages: List[ChatMessage], 
                                 filename: str, style: str = "qq"):
        """保存策划对话到文件"""
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
        
        print(f"✅ 策划对话已保存到: {filename}")
    
    def _format_qq_style(self, messages: List[ChatMessage]) -> str:
        """格式化为QQ风格"""
        output = []
        output.append("=" * 60)
        output.append(f"策划组织聊天记录 - {self.main_event}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 60)
        output.append("")
        
        # 添加策划信息摘要
        output.append("📋 策划信息摘要:")
        output.append(f"主事件: {self.main_event}")
        output.append(f"团队成员: {len(self.planning_characters)} 人")
        output.append(f"策划阶段: {len(self.planning_phases)} 个")
        output.append(f"子事件: {len(self.sub_events)} 个")
        output.append(f"总消息数: {len(messages)} 条")
        output.append("")
        
        current_date = None
        for message in messages:
            # 检查是否需要显示日期
            message_date = message.timestamp.date()
            if current_date != message_date:
                current_date = message_date
                output.append(f"\n{current_date.strftime('%Y年%m月%d日')}")
                output.append("-" * 40)
                
            # 格式化时间
            time_str = message.timestamp.strftime("%H:%M:%S")
            
            # 格式化消息
            output.append(f"[{time_str}] {message.sender}: {message.content}")
            
        return "\n".join(output)
    
    def _format_wechat_style(self, messages: List[ChatMessage]) -> str:
        """格式化为微信风格"""
        output = []
        output.append("=" * 60)
        output.append(f"策划组织微信群聊 - {self.main_event}")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 60)
        output.append("")
        
        # 添加策划信息摘要
        output.append("📋 策划信息摘要:")
        output.append(f"主事件: {self.main_event}")
        output.append(f"团队成员: {len(self.planning_characters)} 人")
        output.append(f"策划阶段: {len(self.planning_phases)} 个")
        output.append(f"子事件: {len(self.sub_events)} 个")
        output.append(f"总消息数: {len(messages)} 条")
        output.append("")
        
        current_date = None
        for message in messages:
            # 检查是否需要显示日期
            message_date = message.timestamp.date()
            if current_date != message_date:
                current_date = message_date
                output.append(f"\n{current_date.strftime('%Y年%m月%d日')}")
                output.append("-" * 40)
                
            # 格式化时间
            time_str = message.timestamp.strftime("%H:%M")
            
            # 格式化消息
            output.append(f"{time_str} {message.sender}\n{message.content}")
            output.append("")
            
        return "\n".join(output)
    
    def save_planning_config(self, filename: str = "planning_config.json"):
        """保存策划配置"""
        config = {
            "main_event": self.main_event,
            "event_context": self.event_context,
            "characters": [char.to_dict() for char in self.planning_characters],
            "phases": [asdict(phase) for phase in self.planning_phases],
            "sub_events": [asdict(event) for event in self.sub_events]
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 策划配置已保存到: {filename}")
    
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
            return '{"characters": [], "sub_events": []}'
        
        return response_text
    
    def _create_temp_file_header(self, filename: str, style: str):
        """创建临时文件头部"""
        output = []
        output.append("=" * 60)
        if style == "qq":
            output.append(f"策划组织聊天记录 - {self.main_event} (实时保存)")
        else:
            output.append(f"策划组织微信群聊 - {self.main_event} (实时保存)")
        if self.event_context:
            output.append(f"事件背景: {self.event_context}")
        output.append("=" * 60)
        output.append("")
        
        # 添加策划信息摘要
        output.append("📋 策划信息摘要:")
        output.append(f"主事件: {self.main_event}")
        output.append(f"团队成员: {len(self.planning_characters)} 人")
        output.append(f"策划阶段: {len(self.planning_phases)} 个")
        output.append(f"子事件: {len(self.sub_events)} 个")
        output.append("")
        output.append("💾 实时保存中，请勿手动编辑此文件...")
        output.append("")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output))
    
    def _append_to_temp_files(self, messages: List[ChatMessage], 
                            qq_filename: str, wechat_filename: str):
        """追加消息到临时文件"""
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
    
    def finalize_temp_files(self, temp_qq_filename: str, temp_wechat_filename: str,
                          final_qq_filename: str, final_wechat_filename: str):
        """完成临时文件，重命名为最终文件"""
        import shutil
        
        if os.path.exists(temp_qq_filename):
            shutil.move(temp_qq_filename, final_qq_filename)
            print(f"✅ QQ格式文件已保存到: {final_qq_filename}")
        
        if os.path.exists(temp_wechat_filename):
            shutil.move(temp_wechat_filename, final_wechat_filename)
            print(f"✅ 微信格式文件已保存到: {final_wechat_filename}")


def main():
    """主函数 - 演示策划聊天生成器"""
    print("🤖 策划组织聊天记录生成器演示")
    print("=" * 60)
    
    try:
        # 创建策划生成器
        planning_generator = PlanningChatGenerator()
        
        # 录入策划事件
        event = "公司数字化转型项目"
        context = "公司需要进行全面的数字化转型，包括系统升级、流程优化、人员培训等多个方面"
        planning_generator.input_planning_event(event, context)
        
        # 生成策划团队
        characters = planning_generator.generate_planning_characters(8)
        
        # 生成策划对话
        messages = planning_generator.generate_planning_conversation(
            total_duration_hours=72.0,  # 3天
            target_message_count=1500   # 1500条消息
        )
        
        # 保存文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        planning_generator.save_planning_conversation(messages, f"output/chat_records/planning_chat_qq_{timestamp}.txt", "qq")
        planning_generator.save_planning_conversation(messages, f"output/chat_records/planning_chat_wechat_{timestamp}.txt", "wechat")
        
        # 保存策划配置
        planning_generator.save_planning_config(f"output/configs/planning_config_{timestamp}.json")
        
        print("\n🎉 策划组织聊天记录生成完成！")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")


if __name__ == "__main__":
    main()
