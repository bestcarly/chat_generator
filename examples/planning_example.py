#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策划组织聊天记录生成器使用示例
展示如何使用策划组织功能生成不同场景的聊天记录
"""

from src.chat_generator.core.planning_generator import PlanningChatGenerator
import datetime


def example_company_event():
    """公司活动策划示例"""
    print("=" * 60)
    print("示例1：公司年会策划组织")
    print("=" * 60)
    
    generator = PlanningChatGenerator()
    
    # 录入策划事件
    event = "公司年会策划组织"
    context = "需要策划组织一个大型公司年会，包括场地选择、节目安排、嘉宾邀请、预算控制、现场管理等各个方面，预计参与人数500人"
    generator.input_planning_event(event, context)
    
    # 生成策划团队
    characters = generator.generate_planning_characters(8)
    
    # 生成策划对话
    messages = generator.generate_planning_conversation(
        total_duration_hours=72.0,  # 3天
        target_message_count=1500   # 1500条消息
    )
    
    # 保存文件
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generator.save_planning_conversation(messages, f"company_event_qq_{timestamp}.txt", "qq")
    generator.save_planning_conversation(messages, f"company_event_wechat_{timestamp}.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条公司年会策划消息")
    print()


def example_product_launch():
    """产品发布会策划示例"""
    print("=" * 60)
    print("示例2：新产品发布会策划组织")
    print("=" * 60)
    
    generator = PlanningChatGenerator()
    
    # 录入策划事件
    event = "新产品发布会策划组织"
    context = "需要策划组织一个创新的产品发布会，包括活动流程设计、媒体邀请、场地布置、技术演示、嘉宾接待等，预计媒体和客户200人"
    generator.input_planning_event(event, context)
    
    # 生成策划团队
    characters = generator.generate_planning_characters(10)
    
    # 生成策划对话
    messages = generator.generate_planning_conversation(
        total_duration_hours=96.0,  # 4天
        target_message_count=2000   # 2000条消息
    )
    
    # 保存文件
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generator.save_planning_conversation(messages, f"product_launch_qq_{timestamp}.txt", "qq")
    generator.save_planning_conversation(messages, f"product_launch_wechat_{timestamp}.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条产品发布会策划消息")
    print()


def example_conference_organization():
    """会议组织策划示例"""
    print("=" * 60)
    print("示例3：行业会议组织策划")
    print("=" * 60)
    
    generator = PlanningChatGenerator()
    
    # 录入策划事件
    event = "行业会议组织策划"
    context = "需要组织一个大型行业会议，包括主题确定、演讲嘉宾邀请、会议议程安排、参会者注册、场地协调、技术支持等，预计参会者1000人"
    generator.input_planning_event(event, context)
    
    # 生成策划团队
    characters = generator.generate_planning_characters(12)
    
    # 生成策划对话
    messages = generator.generate_planning_conversation(
        total_duration_hours=120.0,  # 5天
        target_message_count=2500    # 2500条消息
    )
    
    # 保存文件
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generator.save_planning_conversation(messages, f"conference_qq_{timestamp}.txt", "qq")
    generator.save_planning_conversation(messages, f"conference_wechat_{timestamp}.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条会议组织策划消息")
    print()


def example_marketing_campaign():
    """营销活动策划示例"""
    print("=" * 60)
    print("示例4：营销活动策划组织")
    print("=" * 60)
    
    generator = PlanningChatGenerator()
    
    # 录入策划事件
    event = "营销活动策划组织"
    context = "需要策划组织一个大型营销活动，包括活动创意、渠道选择、内容制作、执行计划、效果评估等，目标覆盖10万用户"
    generator.input_planning_event(event, context)
    
    # 生成策划团队
    characters = generator.generate_planning_characters(9)
    
    # 生成策划对话
    messages = generator.generate_planning_conversation(
        total_duration_hours=84.0,  # 3.5天
        target_message_count=1800   # 1800条消息
    )
    
    # 保存文件
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    generator.save_planning_conversation(messages, f"marketing_campaign_qq_{timestamp}.txt", "qq")
    generator.save_planning_conversation(messages, f"marketing_campaign_wechat_{timestamp}.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条营销活动策划消息")
    print()


def main():
    """主函数"""
    print("📋 策划组织聊天记录生成器 - 使用示例")
    print("=" * 80)
    
    # 运行所有示例
    example_company_event()
    example_product_launch()
    example_conference_organization()
    example_marketing_campaign()
    
    print("=" * 80)
    print("所有策划组织示例运行完成！")
    print("生成的文件:")
    print("- company_event_qq_*.txt / company_event_wechat_*.txt")
    print("- product_launch_qq_*.txt / product_launch_wechat_*.txt")
    print("- conference_qq_*.txt / conference_wechat_*.txt")
    print("- marketing_campaign_qq_*.txt / marketing_campaign_wechat_*.txt")
    print()
    print("这些文件展示了不同场景下的策划组织聊天记录格式。")
    print("每个文件都包含完整的策划流程、逻辑链条和多个小事情的穿插。")


if __name__ == "__main__":
    main()
