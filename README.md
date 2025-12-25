# 火山引擎智能营销内容创作助手

基于**火山引擎方舟大语言模型**构建的智能营销内容创作Agent，展示火山引擎AI产品在实际业务场景中的应用价值。

## 🎯 项目概述

本项目是一个完整的智能营销内容创作解决方案，通过集成火山引擎方舟大语言模型，实现了：
- **智能内容创作**：根据主题、受众、平台要求生成高质量营销内容
- **多模态图片分析**：分析图片内容并生成针对性的营销文案
- **内容优化润色**：优化现有内容，提高清晰度、吸引力和转化率

## 🚀 核心功能

### 1. 📝 智能内容创作 (`create_content`)
- 支持多种内容类型：文章、博客、社交媒体文案、广告文案、邮件营销等
- 可指定目标受众、语气风格、内容长度
- 基于火山方舟大模型的强大文本生成能力

### 2. 🖼️ 多模态图片分析 (`analyze_image_for_marketing`)
- 分析图片中的视觉元素（人物、场景、物体、颜色、构图等）
- 理解图片传达的情感、氛围和潜在信息
- 为不同平台（小红书、微博、抖音等）生成针对性营销文案
- 利用火山方舟视觉模型的多模态理解能力

### 3. ✨ 内容优化润色 (`optimize_content`)
- 优化现有内容的清晰度、可读性和吸引力
- 根据优化目标调整内容（提高说服力、增加互动性、精简或扩展等）
- 适配不同平台规范和受众偏好

## 🔧 技术架构

### 火山引擎产品集成

本项目核心依赖于**火山引擎方舟大语言模型服务**，具体使用了：

- **产品名称**：火山方舟（Volcano Ark）
- **核心模型**：豆包大模型（`doubao-seed-1-6-251015`）
- **视觉模型**：豆包视觉模型（`doubao-seed-1-6-vision-250815`）
- **集成方式**：通过Coze平台内置集成，无需用户提供API Key

### 架构特点
- 基于LangChain 1.0框架构建
- 模块化工具设计，易于扩展
- 开发环境自动启用内存记忆（MemorySaver）
- 配置文件集中管理，便于维护

## 📦 快速开始

### 环境要求
- Python 3.8+
- 火山引擎账户（用于获取环境变量配置）

### 安装步骤
```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 安装依赖
pip install -r requirements.txt

# 设置环境变量（根据Coze平台配置）
export COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
export COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

### 运行Agent
```bash
# 方式1：直接运行主程序
python src/main.py

# 方式2：通过脚本运行
bash scripts/local_run.sh -m flow
```

### 交互示例
```python
from agents.agent import build_agent

# 初始化Agent
agent = build_agent()

# 内容创作示例
response = agent.invoke({
    "messages": [{
        "role": "user", 
        "content": "请帮我写一篇关于健康饮食的博客文章，目标受众是年轻人"
    }]
})
print(response)
```

## 🔗 火山引擎产品链接

### 火山方舟大语言模型服务
本项目核心使用的火山引擎产品：

- **产品官网**：https://www.volcengine.com/product/ark
- **产品介绍**：火山方舟是火山引擎推出的一站式大模型服务平台，提供多种领先的大语言模型和视觉模型
- **核心能力**：
  - 文本生成与对话交互
  - 多模态视觉理解
  - 意图识别与内容创作
  - 企业级安全与稳定性

### 为什么选择火山引擎？
1. **技术领先**：集成豆包、DeepSeek、Kimi等前沿大语言模型
2. **开箱即用**：无需复杂配置，快速集成到现有系统
3. **企业级服务**：提供高可用、高并发的AI服务能力
4. **成本优化**：灵活的计费方式，适合不同规模的企业

## 📁 项目结构
```
.
├── config/                    # 配置文件目录
│   └── agent_llm_config.json  # Agent模型配置
├── src/                      # 源代码
│   ├── agents/               # Agent核心代码
│   │   └── agent.py          # Agent构建逻辑
│   ├── tools/                # 核心工具实现
│   │   ├── content_creation_tool.py       # 内容创作工具
│   │   ├── image_analysis_tool.py         # 图片分析工具
│   │   └── content_optimization_tool.py   # 内容优化工具
│   └── main.py               # 主程序入口
├── scripts/                  # 辅助脚本
│   ├── local_run.sh          # 本地运行脚本
│   ├── http_run.sh           # HTTP服务脚本
│   └── pack.sh               # 打包脚本
└── requirements.txt          # Python依赖列表
```

## 🧪 测试验证

项目已通过完整测试：
- ✅ Agent初始化测试
- ✅ 内容创作功能测试
- ✅ 工具调用验证
- ✅ 错误处理测试
- ✅ 内容优化功能测试

运行测试：
```bash
# 简单测试
bash scripts/local_run.sh -m flow
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

如有问题或建议，请通过以下方式联系：
- GitHub Issues：提交问题报告
- 火山引擎官网：获取产品支持

---

**免责声明**：本项目为演示用途，展示火山引擎AI产品在实际场景中的应用。实际生产使用请参考火山引擎官方文档和最佳实践。
