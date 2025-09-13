#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多阶段犯罪组织聊天生成
"""

def test_multiphase_phases():
    """测试多阶段功能"""
    print("🧪 测试多阶段犯罪组织聊天生成")
    print("=" * 60)
    
    # 模拟多阶段数据
    phases = [
        # 策划阶段
        {"name": "踩点摸底", "description": "了解目标情况，收集情报信息", "duration": 8.0},
        {"name": "制定方案", "description": "制定具体的行动计划", "duration": 12.0},
        {"name": "人员准备", "description": "安排人手，分配任务", "duration": 16.0},
        {"name": "物资准备", "description": "准备行动所需的物资装备", "duration": 10.0},
        {"name": "行动准备", "description": "最后的行动前准备", "duration": 6.0},
        # 施行阶段
        {"name": "开始行动", "description": "正式开始执行犯罪行动", "duration": 4.0},
        {"name": "行动执行", "description": "执行具体的犯罪行动", "duration": 6.0},
        {"name": "撤退转移", "description": "行动完成后的撤退和转移", "duration": 3.0},
        # 应对阶段
        {"name": "被发现应对", "description": "行动被发现后的紧急应对", "duration": 2.0},
        {"name": "公安侦破应对", "description": "应对公安部门的侦破和抓捕", "duration": 8.0},
        {"name": "抓捕应对", "description": "应对公安抓捕行动", "duration": 4.0},
        {"name": "善后处理", "description": "最后的善后处理工作", "duration": 6.0}
    ]
    
    print(f"📊 多阶段策划流程 ({len(phases)} 个阶段):")
    print()
    
    # 策划阶段
    print("🎯 策划阶段 (5个阶段):")
    for i, phase in enumerate(phases[:5], 1):
        print(f"  {i}. {phase['name']}")
        print(f"     描述: {phase['description']}")
        print(f"     时长: {phase['duration']}小时")
        print()
    
    # 施行阶段
    print("⚡ 施行阶段 (3个阶段):")
    for i, phase in enumerate(phases[5:8], 1):
        print(f"  {i}. {phase['name']}")
        print(f"     描述: {phase['description']}")
        print(f"     时长: {phase['duration']}小时")
        print()
    
    # 应对阶段
    print("🚨 应对阶段 (4个阶段):")
    for i, phase in enumerate(phases[8:], 1):
        print(f"  {i}. {phase['name']}")
        print(f"     描述: {phase['description']}")
        print(f"     时长: {phase['duration']}小时")
        print()
    
    # 模拟子事件
    sub_events = [
        # 策划阶段事件
        {"name": "目标变更", "phase": "踩点摸底", "urgency": "高", "impact": "高"},
        {"name": "人员被抓", "phase": "人员准备", "urgency": "高", "impact": "中"},
        {"name": "装备丢失", "phase": "物资准备", "urgency": "中", "impact": "中"},
        {"name": "警察巡逻", "phase": "制定方案", "urgency": "高", "impact": "高"},
        {"name": "内讧冲突", "phase": "人员准备", "urgency": "中", "impact": "中"},
        # 施行阶段事件
        {"name": "行动受阻", "phase": "行动执行", "urgency": "高", "impact": "高"},
        {"name": "目标反抗", "phase": "行动执行", "urgency": "高", "impact": "中"},
        {"name": "设备故障", "phase": "开始行动", "urgency": "中", "impact": "中"},
        {"name": "撤退受阻", "phase": "撤退转移", "urgency": "高", "impact": "高"},
        # 应对阶段事件
        {"name": "被发现", "phase": "被发现应对", "urgency": "高", "impact": "高"},
        {"name": "警方介入", "phase": "公安侦破应对", "urgency": "高", "impact": "高"},
        {"name": "证据暴露", "phase": "公安侦破应对", "urgency": "高", "impact": "高"},
        {"name": "抓捕行动", "phase": "抓捕应对", "urgency": "高", "impact": "高"},
        {"name": "同伙被抓", "phase": "抓捕应对", "urgency": "高", "impact": "高"}
    ]
    
    print(f"⚠️ 多阶段子事件 ({len(sub_events)} 个):")
    print()
    
    # 按阶段分组显示
    phase_groups = {}
    for event in sub_events:
        phase = event['phase']
        if phase not in phase_groups:
            phase_groups[phase] = []
        phase_groups[phase].append(event)
    
    for phase_name, events in phase_groups.items():
        print(f"📋 {phase_name}阶段事件:")
        for event in events:
            print(f"  - {event['name']} (紧急:{event['urgency']}, 影响:{event['impact']})")
        print()
    
    # 模拟对话类型
    dialogue_types = [
        "任务分配和进度汇报",
        "问题提出和解决方案讨论", 
        "决策制定和执行确认",
        "资源协调和风险控制",
        "阶段总结和下一步规划",
        "行动执行和现场反馈",
        "应对措施和紧急处理",
        "警方动向和风险评估",
        "证据销毁和痕迹清理",
        "同伙保护和后路安排"
    ]
    
    print(f"💬 多阶段对话类型 ({len(dialogue_types)} 种):")
    for i, dtype in enumerate(dialogue_types, 1):
        print(f"  {i}. {dtype}")
    print()
    
    # 阶段转换逻辑
    print("🔄 阶段转换逻辑:")
    print("  策划阶段 → 施行阶段 → 应对阶段")
    print("  ↓")
    print("  踩点摸底 → 制定方案 → 人员准备 → 物资准备 → 行动准备")
    print("  ↓")
    print("  开始行动 → 行动执行 → 撤退转移")
    print("  ↓")
    print("  被发现应对 → 公安侦破应对 → 抓捕应对 → 善后处理")
    print()
    
    # 总时长统计
    total_duration = sum(phase['duration'] for phase in phases)
    planning_duration = sum(phase['duration'] for phase in phases[:5])
    execution_duration = sum(phase['duration'] for phase in phases[5:8])
    response_duration = sum(phase['duration'] for phase in phases[8:])
    
    print(f"⏱️ 总时长统计:")
    print(f"  策划阶段: {planning_duration}小时")
    print(f"  施行阶段: {execution_duration}小时")
    print(f"  应对阶段: {response_duration}小时")
    print(f"  总时长: {total_duration}小时")
    print()
    
    print("🎯 测试完成！")
    print("✅ 新增功能:")
    print("  - 增加了施行阶段（开始行动、行动执行、撤退转移）")
    print("  - 增加了应对阶段（被发现应对、公安侦破应对、抓捕应对、善后处理）")
    print("  - 扩展了子事件类型，涵盖所有阶段")
    print("  - 增加了新的对话类型，适应不同阶段特点")
    print("  - 支持完整的犯罪组织活动流程")

if __name__ == "__main__":
    test_multiphase_phases()
