# 项目结构说明

## 目录结构

```
chat_generator/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── setup.py                     # 安装脚本
├── .gitignore                   # Git忽略文件
├── 
├── src/                         # 源代码目录
│   └── chat_generator/          # 主包
│       ├── core/                # 核心功能模块
│       ├── models/              # 数据模型
│       ├── config/              # 配置管理
│       ├── utils/               # 工具函数
│       └── cli/                 # 命令行接口
├── 
├── tests/                       # 测试目录
├── examples/                    # 示例目录
├── docs/                        # 文档目录
├── config/                      # 配置文件目录
├── output/                      # 输出目录
└── scripts/                     # 脚本目录
```

## 主要文件说明

### 核心文件
- `src/chat_generator/core/` - 核心生成器功能
- `src/chat_generator/models/` - 数据模型定义
- `src/chat_generator/config/` - 配置管理
- `src/chat_generator/utils/` - 工具函数
- `src/chat_generator/cli/` - 命令行接口

### 配置文件
- `config/` - 用户配置文件
- `requirements.txt` - Python依赖
- `setup.py` - 包安装配置

### 输出文件
- `output/chat_records/` - 生成的聊天记录
- `output/configs/` - 保存的配置
- `output/temp/` - 临时文件
- `output/logs/` - 日志文件

### 文档文件
- `README.md` - 项目主文档
- `docs/SETUP.md` - 安装指南
- `docs/` - 其他文档

## 使用方式

1. **安装**: `pip install -e .`
2. **命令行**: `chat-generator`
3. **Python API**: `from chat_generator import ChatGenerator`
