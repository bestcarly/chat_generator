#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试JSON清理功能
"""

def clean_json_response(response_text: str) -> str:
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

def test_json_cleanup():
    """测试JSON清理功能"""
    print("🧪 测试JSON清理功能")
    print("=" * 40)
    
    test_cases = [
        # 正常JSON
        '{"characters": [{"name": "张三"}]}',
        
        # 带markdown标记的JSON
        '```json\n{"characters": [{"name": "张三"}]}\n```',
        
        # 带普通markdown标记的JSON
        '```\n{"characters": [{"name": "张三"}]}\n```',
        
        # 空响应
        '',
        
        # 非JSON内容
        '这不是JSON格式的内容',
        
        # 只有markdown标记
        '```json\n```',
        
        # 带空格的JSON
        '  {"characters": [{"name": "张三"}]}  ',
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {repr(test_case[:30])}...")
        try:
            cleaned = clean_json_response(test_case)
            print(f"清理后: {repr(cleaned[:50])}...")
            
            # 尝试解析JSON
            import json
            data = json.loads(cleaned)
            print("✅ JSON解析成功")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
        except Exception as e:
            print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_json_cleanup()
