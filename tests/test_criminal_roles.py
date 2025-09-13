#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试犯罪组织角色生成
"""

from planning_chat_generator import PlanningChatGenerator

def test_criminal_roles():
    """测试犯罪组织角色生成"""
    print("🧪 测试犯罪组织角色生成")
    print("=" * 50)
    
    # 创建生成器
    generator = PlanningChatGenerator()
    
    # 设置犯罪事件
    event = "抢劫银行"
    context = "目标银行位于市中心，安保严密，需要精心策划"
    
    generator.input_planning_event(event, context)
    
    print(f"📋 事件: {event}")
    print(f"📋 背景: {context}")
    print()
    
    # 生成角色
    print("👥 生成犯罪组织角色...")
    characters = generator.generate_planning_characters(6)
    
    print(f"\n✅ 生成了 {len(characters)} 个角色:")
    for i, char in enumerate(characters, 1):
        print(f"\n{i}. {char.name} ({char.role})")
        print(f"   部门: {char.department}")
        print(f"   级别: {char.level}")
        print(f"   专业: {', '.join(char.expertise)}")
        print(f"   性格: {char.personality}")
        print(f"   说话风格: {char.speaking_style}")
        print(f"   职责: {', '.join(char.responsibilities)}")
        print(f"   决策权限: {char.decision_power}")
    
    # 生成策划阶段
    print(f"\n📊 生成策划阶段...")
    phases = generator.generate_planning_phases()
    
    print(f"\n✅ 生成了 {len(phases)} 个策划阶段:")
    for i, phase in enumerate(phases, 1):
        print(f"\n{i}. {phase.name}")
        print(f"   描述: {phase.description}")
        print(f"   时长: {phase.duration_hours}小时")
        print(f"   关键任务: {', '.join(phase.key_tasks)}")
        print(f"   交付物: {', '.join(phase.deliverables)}")
    
    # 生成子事件
    print(f"\n⚠️ 生成子事件...")
    sub_events = generator.generate_sub_events(5)
    
    print(f"\n✅ 生成了 {len(sub_events)} 个子事件:")
    for i, event in enumerate(sub_events, 1):
        print(f"\n{i}. {event.name}")
        print(f"   描述: {event.description}")
        print(f"   紧急程度: {event.urgency}")
        print(f"   影响程度: {event.impact}")
        print(f"   相关阶段: {event.related_phase}")
        print(f"   触发条件: {', '.join(event.trigger_conditions)}")
    
    print(f"\n🎯 测试完成！角色更符合犯罪组织的真实情况。")

if __name__ == "__main__":
    test_criminal_roles()
