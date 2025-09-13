#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
支持从环境变量和.env文件加载配置
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

# Google AI API配置
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY', '')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-2.5-flash-preview-05-20')

# 调试配置
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 默认生成参数
DEFAULT_MESSAGE_COUNT = int(os.getenv('DEFAULT_MESSAGE_COUNT', '30'))
DEFAULT_DURATION_HOURS = float(os.getenv('DEFAULT_DURATION_HOURS', '1.0'))
DEFAULT_CHARACTER_COUNT = int(os.getenv('DEFAULT_CHARACTER_COUNT', '6'))

# 生成参数限制
MIN_CHARACTERS = int(os.getenv('MIN_CHARACTERS', '5'))
MAX_CHARACTERS = int(os.getenv('MAX_CHARACTERS', '10'))
MIN_MESSAGE_COUNT = int(os.getenv('MIN_MESSAGE_COUNT', '10'))
MAX_MESSAGE_COUNT = int(os.getenv('MAX_MESSAGE_COUNT', '100'))
MIN_DURATION = float(os.getenv('MIN_DURATION', '0.1'))
MAX_DURATION = float(os.getenv('MAX_DURATION', '24.0'))

# 实时保存配置
DEFAULT_SAVE_INTERVAL = int(os.getenv('DEFAULT_SAVE_INTERVAL', '10'))
DEFAULT_REALTIME_SAVE = os.getenv('DEFAULT_REALTIME_SAVE', 'true').lower() == 'true'

def validate_config():
    """验证配置是否有效"""
    errors = []
    
    if not GOOGLE_AI_API_KEY:
        errors.append("GOOGLE_AI_API_KEY 未设置")
    
    if not DEFAULT_MODEL:
        errors.append("DEFAULT_MODEL 未设置")
    
    if MIN_MESSAGE_COUNT > MAX_MESSAGE_COUNT:
        errors.append("MIN_MESSAGE_COUNT 不能大于 MAX_MESSAGE_COUNT")
    
    if MIN_DURATION > MAX_DURATION:
        errors.append("MIN_DURATION 不能大于 MAX_DURATION")
    
    return errors

def get_config_summary():
    """获取配置摘要"""
    return {
        'api_key_set': bool(GOOGLE_AI_API_KEY),
        'model': DEFAULT_MODEL,
        'debug': DEBUG,
        'log_level': LOG_LEVEL,
        'default_message_count': DEFAULT_MESSAGE_COUNT,
        'default_duration_hours': DEFAULT_DURATION_HOURS,
        'default_character_count': DEFAULT_CHARACTER_COUNT,
        'save_interval': DEFAULT_SAVE_INTERVAL,
        'realtime_save': DEFAULT_REALTIME_SAVE
    }
