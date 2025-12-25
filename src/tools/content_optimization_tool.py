"""
内容优化工具 - 基于火山方舟大模型的内容优化工具
展示火山引擎大语言模型在内容优化和润色方面的应用价值
"""

import os
import json
from typing import Optional, Dict, Any
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from coze_coding_utils.runtime_ctx.context import default_headers


@tool
def optimize_content(
    original_content: str,
    optimization_goal: str = "improve_clarity",
    target_audience: str = "general",
    platform_constraints: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    使用火山方舟大模型优化和润色现有内容。
    
    参数:
        original_content: 原始内容文本
        optimization_goal: 优化目标，如 "improve_clarity", "increase_engagement", 
                          "make_more_persuasive", "shorten", "expand"
        target_audience: 目标受众，如 "young_adults", "professionals", "international"
        platform_constraints: 平台限制，如 "twitter_280_chars", "linkedin_professional"
        runtime: 工具运行时上下文
        
    返回:
        优化后的内容文本和改进说明
    """
    try:
        # 获取运行时上下文
        ctx = runtime.context if runtime else None
        
        # 根据优化目标构建系统提示词
        goal_descriptions = {
            "improve_clarity": "提高内容的清晰度和可读性",
            "increase_engagement": "增加内容的互动性和吸引力",
            "make_more_persuasive": "使内容更具说服力和转化力",
            "shorten": "精简内容，保留核心信息",
            "expand": "扩展内容，增加细节和深度"
        }
        
        goal_desc = goal_descriptions.get(optimization_goal, "优化内容")
        
        system_prompt = f"""你是一个专业的内容优化专家，擅长根据不同的优化目标改进文本内容。
        你的任务是：{goal_desc}
        
        优化时请考虑：
        1. 目标受众：{target_audience}
        2. 保持原文的核心信息和意图
        3. 改善语言表达、逻辑结构和可读性
        4. 确保优化后的内容自然流畅
        
        请先输出优化后的内容，然后简要说明所做的改进。"""
        
        if platform_constraints:
            system_prompt += f"\n5. 平台限制：{platform_constraints}"
        
        # 构建用户提示词
        user_prompt = f"""请优化以下内容：

【原始内容】
{original_content}

优化目标：{optimization_goal}
{f"平台限制：{platform_constraints}" if platform_constraints else ""}

请提供优化后的版本，并简要说明改进之处。"""
        
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
            temperature=0.5,  # 较低的创造性，保持原文意图
            streaming=False,
            timeout=60,
            default_headers=default_headers(ctx) if ctx else {}
        )
        
        # 调用大模型
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # 返回优化结果
        result = f"# 内容优化报告\n\n"
        result += f"**优化目标**: {optimization_goal}\n"
        result += f"**目标受众**: {target_audience}\n"
        if platform_constraints:
            result += f"**平台限制**: {platform_constraints}\n\n"
        
        result += "## 优化后的内容\n\n"
        # 确保response.content是字符串
        if isinstance(response.content, list):
            content_str = " ".join(str(item) for item in response.content)
        else:
            content_str = str(response.content)
        result += content_str
        
        return result
        
    except Exception as e:
        return f"内容优化过程中出现错误：{str(e)}"