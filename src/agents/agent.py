"""
火山引擎智能营销内容创作助手 - Agent核心代码
展示火山方舟大语言模型在营销内容创作场景的应用价值
"""

import os
import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from coze_coding_utils.runtime_ctx.context import default_headers
from utils.helper.graph_helper import is_dev_env

# 导入工具
from tools.content_creation_tool import create_content
from tools.image_analysis_tool import analyze_image_for_marketing
from tools.content_optimization_tool import optimize_content

# 配置文件路径
LLM_CONFIG = "config/agent_llm_config.json"

# 内存检查点 - 开发环境使用内存记忆
in_memory_checkpointer = None

# 开发环境默认使用内存记忆, 生产环境默认无记忆
if is_dev_env():
    in_memory_checkpointer = MemorySaver()


def build_agent(ctx=None):
    """
    构建并返回智能营销内容创作助手Agent
    
    参数:
        ctx: 运行时上下文
        
    返回:
        Agent实例
    """
    # 获取工作空间路径
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    
    # 构建配置文件完整路径
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except Exception as e:
        raise RuntimeError(f"无法读取配置文件 {config_path}: {str(e)}")
    
    # 获取API配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    if not api_key or not base_url:
        raise RuntimeError(
            "未配置火山方舟大模型API环境变量。请确保COZE_WORKLOAD_IDENTITY_API_KEY和COZE_INTEGRATION_MODEL_BASE_URL已设置。"
        )
    
    # 创建大语言模型实例
    llm = ChatOpenAI(
        model=cfg['config'].get("model", "doubao-seed-1-6-251015"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,  # 必须为True，遵循集成要求
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 准备工具列表
    tools = [
        create_content,
        analyze_image_for_marketing,
        optimize_content
    ]
    
    # 创建Agent
    global in_memory_checkpointer
    agent = create_agent(
        model=llm,
        system_prompt=cfg.get("sp", "You are a helpful assistant. Use tools when helpful."),
        tools=tools,
        checkpointer=in_memory_checkpointer
    )
    
    return agent


# 用于测试的简单运行函数
if __name__ == "__main__":
    print("正在初始化火山引擎智能营销内容创作助手...")
    try:
        agent = build_agent()
        print("Agent初始化成功！")
        print("\n可用工具：")
        print("1. create_content - 创建各种类型的内容")
        print("2. analyze_image_for_marketing - 分析图片并生成营销文案")
        print("3. optimize_content - 优化和润色现有内容")
        print("\n示例用法：")
        print("agent.invoke({\"messages\": [{\"role\": \"user\", \"content\": \"请帮我写一篇关于健康饮食的博客文章\"}]})")
    except Exception as e:
        print(f"Agent初始化失败：{str(e)}")