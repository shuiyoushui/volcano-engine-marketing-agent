"""
内容创作工具 - 基于火山方舟大模型的内容生成工具
展示火山引擎大语言模型在内容创作场景的应用价值
"""

import os
import json
from typing import Optional, Dict, Any
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from coze_coding_utils.runtime_ctx.context import default_headers


@tool
def create_content(
    content_type: str,
    topic: str,
    target_audience: str = "general",
    tone: str = "professional",
    length: str = "medium",
    additional_requirements: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    使用火山方舟大模型创建各种类型的内容。
    
    参数:
        content_type: 内容类型，如 "article", "blog_post", "social_media", "ad_copy", "email"
        topic: 内容主题
        target_audience: 目标受众，如 "young_adults", "professionals", "parents" 等
        tone: 语气风格，如 "professional", "casual", "friendly", "persuasive"
        length: 内容长度，如 "short", "medium", "long"
        additional_requirements: 额外要求或说明
        runtime: 工具运行时上下文
        
    返回:
        生成的内容文本
    """
    try:
        # 获取运行时上下文
        ctx = runtime.context if runtime else None
        
        # 构建系统提示词
        system_prompt = """你是一个专业的营销内容创作专家，擅长为不同平台和受众创作高质量的内容。
        请根据用户的要求，创作出符合以下标准的内容：
        1. 内容类型和格式符合要求
        2. 语气风格与目标受众匹配
        3. 内容结构清晰，逻辑连贯
        4. 语言生动，有吸引力
        5. 符合营销传播的最佳实践
        
        请直接输出创作的内容，不要添加额外的说明或注释。"""
        
        # 构建用户提示词
        user_prompt = f"""请创作一个{content_type}，主题是：{topic}

具体要求：
- 目标受众：{target_audience}
- 语气风格：{tone}
- 内容长度：{length}
{f"- 额外要求：{additional_requirements}" if additional_requirements else ""}

请创作出高质量的内容。"""
        
        # 获取API配置
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        if not api_key or not base_url:
            return "错误：未配置火山方舟大模型API环境变量。请确保COZE_WORKLOAD_IDENTITY_API_KEY和COZE_INTEGRATION_MODEL_BASE_URL已设置。"
        
        # 创建大模型客户端
        llm = ChatOpenAI(
            model="doubao-seed-1-6-251015",  # 使用火山方舟的豆包模型
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,  # 适度的创造性
            streaming=False,  # 非流式输出
            timeout=60,
            default_headers=default_headers(ctx) if ctx else {}
        )
        
        # 调用大模型
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # 返回生成的内容，确保是字符串
        if isinstance(response.content, list):
            return " ".join(str(item) for item in response.content)
        else:
            return str(response.content)
        
    except Exception as e:
        return f"内容创作过程中出现错误：{str(e)}"