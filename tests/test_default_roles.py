#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试默认犯罪组织角色
"""

def test_default_criminal_roles():
    """测试默认犯罪组织角色"""
    print("🧪 测试默认犯罪组织角色")
    print("=" * 50)
    
    # 模拟默认角色数据
    default_chars = [
        {
            "name": "强哥",
            "role": "老大",
            "department": "总指挥",
            "level": "老大",
            "expertise": ["指挥行动", "笼络人心", "处理关系"],
            "personality": "心狠手辣、有威信、善于笼络人心",
            "speaking_style": "粗俗直接、带脏话、有威慑力",
            "responsibilities": ["指挥行动", "分配任务", "处理纠纷"],
            "decision_power": "高"
        },
        {
            "name": "阿龙",
            "role": "军师",
            "department": "情报组",
            "level": "骨干",
            "expertise": ["出谋划策", "收集情报", "分析形势"],
            "personality": "狡猾、多疑、善于算计",
            "speaking_style": "阴阳怪气、话里有话",
            "responsibilities": ["制定计划", "收集情报", "分析风险"],
            "decision_power": "中"
        },
        {
            "name": "老六",
            "role": "打手",
            "department": "行动组",
            "level": "骨干",
            "expertise": ["打架斗殴", "威胁恐吓", "执行任务"],
            "personality": "好勇斗狠、冲动、忠诚",
            "speaking_style": "粗鲁、威胁性、带脏话",
            "responsibilities": ["执行任务", "威胁恐吓", "保护老大"],
            "decision_power": "低"
        },
        {
            "name": "小陈",
            "role": "技术员",
            "department": "技术组",
            "level": "马仔",
            "expertise": ["技术操作", "设备维护", "网络技术"],
            "personality": "内向、技术宅、胆小",
            "speaking_style": "结巴、技术术语、不自信",
            "responsibilities": ["技术操作", "设备维护", "网络支持"],
            "decision_power": "低"
        },
        {
            "name": "阿花",
            "role": "联络人",
            "department": "后勤组",
            "level": "马仔",
            "expertise": ["联络沟通", "后勤保障", "信息传递"],
            "personality": "圆滑、善于交际、贪财",
            "speaking_style": "油嘴滑舌、奉承话多",
            "responsibilities": ["联络沟通", "后勤保障", "信息传递"],
            "decision_power": "低"
        },
        {
            "name": "大熊",
            "role": "打手",
            "department": "行动组",
            "level": "马仔",
            "expertise": ["打架斗殴", "威胁恐吓", "看场子"],
            "personality": "四肢发达、头脑简单、忠诚",
            "speaking_style": "粗鲁、简单直接、带脏话",
            "responsibilities": ["看场子", "威胁恐吓", "执行任务"],
            "decision_power": "低"
        }
    ]
    
    print(f"✅ 默认犯罪组织角色 ({len(default_chars)} 个):")
    for i, char in enumerate(default_chars, 1):
        print(f"\n{i}. {char['name']} ({char['role']})")
        print(f"   部门: {char['department']}")
        print(f"   级别: {char['level']}")
        print(f"   专业: {', '.join(char['expertise'])}")
        print(f"   性格: {char['personality']}")
        print(f"   说话风格: {char['speaking_style']}")
        print(f"   职责: {', '.join(char['responsibilities'])}")
        print(f"   决策权限: {char['decision_power']}")
    
    # 模拟策划阶段
    default_phases = [
        {
            "name": "踩点摸底",
            "description": "了解目标情况，收集情报信息",
            "duration_hours": 8.0,
            "key_tasks": ["目标踩点", "收集情报", "分析形势", "评估风险"],
            "deliverables": ["踩点报告", "情报汇总", "风险评估"]
        },
        {
            "name": "制定方案",
            "description": "制定具体的行动计划",
            "duration_hours": 12.0,
            "key_tasks": ["方案设计", "路线规划", "人员安排", "时间安排"],
            "deliverables": ["行动方案", "路线图", "人员分工"]
        },
        {
            "name": "人员准备",
            "description": "安排人手，分配任务",
            "duration_hours": 16.0,
            "key_tasks": ["人员召集", "任务分配", "装备准备", "联络安排"],
            "deliverables": ["人员名单", "任务分工", "装备清单", "联络方式"]
        },
        {
            "name": "物资准备",
            "description": "准备行动所需的物资装备",
            "duration_hours": 10.0,
            "key_tasks": ["装备采购", "工具准备", "车辆安排", "通讯设备"],
            "deliverables": ["装备清单", "工具清单", "车辆安排", "通讯设备"]
        },
        {
            "name": "行动准备",
            "description": "最后的行动前准备",
            "duration_hours": 6.0,
            "key_tasks": ["最终检查", "应急预案", "撤退路线", "善后安排"],
            "deliverables": ["检查清单", "应急预案", "撤退路线", "善后方案"]
        }
    ]
    
    print(f"\n📊 默认策划阶段 ({len(default_phases)} 个):")
    for i, phase in enumerate(default_phases, 1):
        print(f"\n{i}. {phase['name']}")
        print(f"   描述: {phase['description']}")
        print(f"   时长: {phase['duration_hours']}小时")
        print(f"   关键任务: {', '.join(phase['key_tasks'])}")
        print(f"   交付物: {', '.join(phase['deliverables'])}")
    
    # 模拟子事件
    default_events = [
        {
            "name": "目标变更",
            "description": "原定目标情况发生变化，需要重新踩点",
            "urgency": "高",
            "impact": "高",
            "related_phase": "踩点摸底",
            "trigger_conditions": ["目标监控", "情报更新"]
        },
        {
            "name": "人员被抓",
            "description": "有成员被警察抓走，需要重新安排人手",
            "urgency": "高",
            "impact": "中",
            "related_phase": "人员准备",
            "trigger_conditions": ["人员确认", "风险评估"]
        },
        {
            "name": "装备丢失",
            "description": "重要装备丢失或损坏，需要重新准备",
            "urgency": "中",
            "impact": "中",
            "related_phase": "物资准备",
            "trigger_conditions": ["装备检查", "物资盘点"]
        },
        {
            "name": "警察巡逻",
            "description": "目标区域出现警察巡逻，需要调整时间",
            "urgency": "高",
            "impact": "高",
            "related_phase": "制定方案",
            "trigger_conditions": ["情报收集", "风险评估"]
        },
        {
            "name": "内讧冲突",
            "description": "团队成员发生内讧，影响行动执行",
            "urgency": "中",
            "impact": "中",
            "related_phase": "人员准备",
            "trigger_conditions": ["人员确认", "团队协调"]
        }
    ]
    
    print(f"\n⚠️ 默认子事件 ({len(default_events)} 个):")
    for i, event in enumerate(default_events, 1):
        print(f"\n{i}. {event['name']}")
        print(f"   描述: {event['description']}")
        print(f"   紧急程度: {event['urgency']}")
        print(f"   影响程度: {event['impact']}")
        print(f"   相关阶段: {event['related_phase']}")
        print(f"   触发条件: {', '.join(event['trigger_conditions'])}")
    
    print(f"\n🎯 测试完成！")
    print(f"✅ 角色特点:")
    print(f"   - 文化程度不高，说话粗俗、市井范儿十足")
    print(f"   - 有专业人士也有好勇斗狠的，三教九流都有")
    print(f"   - 不再过于职业化，符合犯罪分子的真实情况")
    print(f"   - 说话风格粗俗、直接、带脏话或方言")
    
    print(f"\n✅ 策划阶段特点:")
    print(f"   - 从'需求分析'改为'踩点摸底'")
    print(f"   - 从'方案设计'改为'制定方案'")
    print(f"   - 从'资源准备'改为'人员准备'和'物资准备'")
    print(f"   - 更符合犯罪组织的实际操作流程")
    
    print(f"\n✅ 子事件特点:")
    print(f"   - 从'技术方案变更'改为'目标变更'")
    print(f"   - 从'预算超支'改为'人员被抓'")
    print(f"   - 从'客户需求变更'改为'警察巡逻'")
    print(f"   - 更符合犯罪组织的实际情况和风险")

if __name__ == "__main__":
    test_default_criminal_roles()
