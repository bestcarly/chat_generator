#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天记录生成器使用示例
展示如何使用编程方式生成聊天记录
"""

from src.chat_generator.core.base_generator import ChatGenerator, Character
import datetime


def example_work_discussion():
    """工作讨论示例"""
    print("=" * 50)
    print("示例1：工作项目讨论")
    print("=" * 50)
    
    generator = ChatGenerator()
    
    # 添加工作团队成员
    team_members = [
        Character(name="项目经理", nickname="PM", personality="严肃", speaking_style="说话比较正式"),
        Character(name="前端开发", nickname="前端", personality="活泼", speaking_style="喜欢用技术术语"),
        Character(name="后端开发", nickname="后端", personality="直率", speaking_style="说话直接"),
        Character(name="UI设计师", nickname="设计师", personality="温和", speaking_style="注重细节")
    ]
    
    for member in team_members:
        generator.add_character(member)
        print(f"添加团队成员: {member.name} ({member.nickname})")
    
    # 设置讨论主题
    generator.set_topic("新功能开发计划", "讨论下个版本的新功能需求和开发时间安排")
    
    # 生成聊天记录
    messages = generator.generate_chat_record(
        duration_hours=1.0,
        message_count=25
    )
    
    # 保存文件
    generator.save_to_file("output/work_discussion_qq.txt", "qq")
    generator.save_to_file("output/work_discussion_wechat.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条工作讨论消息")
    print()


def example_friend_chat():
    """朋友聊天示例"""
    print("=" * 50)
    print("示例2：朋友聚会聊天")
    print("=" * 50)
    
    generator = ChatGenerator()
    
    # 添加朋友
    friends = [
        Character(name="小明", nickname="小明", personality="活泼", speaking_style="喜欢开玩笑"),
        Character(name="小红", nickname="小红", personality="温和", speaking_style="说话比较温柔"),
        Character(name="小刚", nickname="小刚", personality="幽默", speaking_style="喜欢讲段子"),
        Character(name="小丽", nickname="小丽", personality="直率", speaking_style="说话比较直接")
    ]
    
    for friend in friends:
        generator.add_character(friend)
        print(f"添加朋友: {friend.name}")
    
    # 设置讨论主题
    generator.set_topic("同学聚会安排", "商量大学同学聚会的具体安排，包括时间、地点和活动内容")
    
    # 生成聊天记录
    messages = generator.generate_chat_record(
        duration_hours=2.0,
        message_count=40
    )
    
    # 保存文件
    generator.save_to_file("output/friend_chat_qq.txt", "qq")
    generator.save_to_file("output/friend_chat_wechat.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条朋友聊天消息")
    print()


def example_family_chat():
    """家庭聊天示例"""
    print("=" * 50)
    print("示例3：家庭群聊")
    print("=" * 50)
    
    generator = ChatGenerator()
    
    # 添加家庭成员
    family = [
        Character(name="爸爸", nickname="老爸", personality="严肃", speaking_style="说话比较正式"),
        Character(name="妈妈", nickname="老妈", personality="温和", speaking_style="关心家人"),
        Character(name="儿子", nickname="小明", personality="活泼", speaking_style="喜欢用网络用语"),
        Character(name="女儿", nickname="小红", personality="幽默", speaking_style="喜欢开玩笑")
    ]
    
    for member in family:
        generator.add_character(member)
        print(f"添加家庭成员: {member.name} ({member.nickname})")
    
    # 设置讨论主题
    generator.set_topic("春节回家安排", "讨论春节假期的回家安排和家庭聚会计划")
    
    # 生成聊天记录
    messages = generator.generate_chat_record(
        duration_hours=1.5,
        message_count=35
    )
    
    # 保存文件
    generator.save_to_file("output/family_chat_qq.txt", "qq")
    generator.save_to_file("output/family_chat_wechat.txt", "wechat")
    
    print(f"生成了 {len(messages)} 条家庭聊天消息")
    print()


def main():
    """主函数"""
    print("聊天记录生成器 - 使用示例")
    print("=" * 60)
    
    # 运行所有示例
    example_work_discussion()
    example_friend_chat()
    example_family_chat()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("生成的文件:")
    print("- work_discussion_qq.txt / work_discussion_wechat.txt")
    print("- friend_chat_qq.txt / friend_chat_wechat.txt")
    print("- family_chat_qq.txt / family_chat_wechat.txt")
    print()
    print("你可以查看这些文件来了解不同场景下的聊天记录格式。")


if __name__ == "__main__":
    main()
