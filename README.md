# Chat Generator - 聊天记录生成器

一个功能强大的聊天记录生成工具，支持多种生成模式和格式。

## ✨ 主要特性

- 🎭 **多种生成模式**：基础生成、AI生成、策划生成
- 🤖 **AI集成**：集成Google AI，智能生成角色和对话
- 📊 **多阶段支持**：支持策划、施行、应对等多个阶段
- 💾 **实时保存**：每10条消息自动保存，防止数据丢失
- 📱 **多格式输出**：支持QQ和微信格式
- 🛡️ **错误处理**：完善的错误处理和恢复机制
- 🔧 **模块化设计**：清晰的代码结构，易于维护和扩展

## 🏗️ 项目结构

```
chat_generator/
├── src/chat_generator/          # 主包目录
│   ├── core/                   # 核心功能模块
│   │   ├── base_generator.py   # 基础生成器
│   │   ├── ai_generator.py     # AI生成器
│   │   └── planning_generator.py # 策划生成器
│   ├── models/                 # 数据模型
│   ├── config/                 # 配置管理
│   ├── utils/                  # 工具函数
│   └── cli/                    # 命令行接口
├── tests/                      # 测试目录
├── examples/                   # 示例目录
├── docs/                       # 文档目录
├── config/                     # 配置文件目录
├── output/                     # 输出目录
└── scripts/                    # 脚本目录
```

## 🚀 快速开始

### 安装

1. 克隆项目：
```bash
git clone https://github.com/yourusername/chat-generator.git
cd chat-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装包：
```bash
pip install -e .
```

### 配置

1. 创建环境配置文件：
```bash
# 复制环境配置模板
cp env.example .env

# 编辑.env文件，设置您的API密钥
GOOGLE_AI_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-2.5-flash-preview-05-20
```

2. 测试配置：
```bash
python scripts/test_env_config.py
```

### 使用

#### 命令行使用

```bash
# 启动主程序
chat-generator

# 或者直接运行
python -m chat_generator.cli.main
```

#### Python API使用

```python
from chat_generator import ChatGenerator, AIChatGenerator, PlanningChatGenerator

# 基础生成器
generator = ChatGenerator()
generator.add_character("张三", "项目经理")
generator.set_topic("项目讨论")
messages = generator.generate_conversation(100)

# AI生成器
ai_generator = AIChatGenerator()
ai_generator.input_event("组织活动")
characters = ai_generator.generate_ai_characters(5)
messages = ai_generator.generate_ai_conversation(200)

# 策划生成器
planning_generator = PlanningChatGenerator()
planning_generator.input_planning_event("组织活动")
phases = planning_generator.generate_planning_phases()
messages = planning_generator.generate_planning_conversation(500)
```

## 📖 功能说明

### 1. 基础生成器
- 支持手动配置角色和话题
- 生成简单的聊天记录
- 支持QQ和微信格式

### 2. AI生成器
- 集成Google AI API
- 智能生成角色和对话
- 支持事件驱动的对话生成
- 上下文感知的对话

### 3. 策划生成器
- 支持多阶段策划流程
- 包含策划、施行、应对阶段
- 支持子事件和复杂场景
- 实时保存功能

## 🔧 配置选项

### 基础配置
- `num_messages`: 生成消息数量
- `time_range_hours`: 时间范围（小时）
- `output_format`: 输出格式（qq/wechat）
- `save_interval`: 保存间隔

### AI配置
- `GOOGLE_AI_API_KEY`: Google AI API密钥
- `DEFAULT_MODEL`: 默认AI模型
- `max_retries`: 最大重试次数

## 📁 输出文件

生成的文件会保存在 `output/` 目录下：

- `chat_records/`: 聊天记录文件
- `configs/`: 配置文件
- `temp/`: 临时文件
- `logs/`: 日志文件

## 🧪 测试

运行测试：
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_core/
```

## 📚 文档

详细文档请查看 `docs/` 目录：

- `features/`: 功能说明
- `api/`: API文档
- `troubleshooting/`: 故障排除
- `updates/`: 更新日志

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。

## 🆘 支持

如果您遇到问题或有建议，请：

1. 查看 [故障排除文档](docs/troubleshooting/)
2. 提交 [Issue](https://github.com/yourusername/chat-generator/issues)
3. 联系维护者

## 🔄 更新日志

### v2.0.0 (当前版本)
- 重构项目结构
- 模块化设计
- 改进错误处理
- 增强AI集成
- 多阶段支持

### v1.x.x (历史版本)
- 基础功能实现
- AI功能添加
- 策划功能扩展

---

**注意**：本项目仅用于学习和研究目的，请遵守相关法律法规。