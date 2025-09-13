# 安装指南

## 环境要求

- Python 3.7+
- pip

## 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/chat-generator.git
cd chat-generator
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 安装包
```bash
pip install -e .
```

### 4. 配置API密钥
```bash
# 复制环境配置模板
cp env.example .env

# 编辑.env文件，设置您的API密钥
GOOGLE_AI_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-2.5-flash-preview-05-20
```

### 5. 测试安装
```bash
python scripts/test_env_config.py
```

## 使用方式

### 命令行使用
```bash
chat-generator
```

### Python API使用
```python
from chat_generator import ChatGenerator, AIChatGenerator, PlanningChatGenerator
```

## 故障排除

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 依赖包是否正确安装
3. API密钥是否正确配置
4. 网络连接是否正常