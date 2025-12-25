"""
图片分析工具 - 基于火山方舟多模态大模型的图片分析工具
展示火山引擎大语言模型在多模态场景的应用价值
"""

import os
import json
from typing import Optional, Dict, Any
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from coze_coding_utils.runtime_ctx.context import default_headers


@tool
def analyze_image_for_marketing(
    image_url: str,
    product_name: Optional[str] = None,
    target_platform: str = "general",
    marketing_angle: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """
    使用火山方舟多模态大模型分析图片内容，并生成营销文案。
    
    参数:
        image_url: 图片的URL地址
        product_name: 产品名称（可选）
        target_platform: 目标平台，如 "weibo", "xiaohongshu", "douyin", "wechat"
        marketing_angle: 营销角度，如 "lifestyle", "product_features", "emotional_appeal"
        runtime: 工具运行时上下文
        
    返回:
        包含图片分析和营销建议的文本
    """
    try:
        # 获取运行时上下文
        ctx = runtime.context if runtime else None
        
        # 构建系统提示词
        system_prompt = """你是一个专业的营销视觉分析专家，擅长分析图片内容并生成有针对性的营销文案。
        请根据提供的图片，完成以下任务：
        1. 详细描述图片中的视觉元素（人物、场景、物体、颜色、构图等）
        2. 分析图片传达的情感、氛围和潜在信息
        3. 根据目标平台和营销角度，生成合适的营销文案
        4. 提供图片在营销中的应用建议
        
        请以结构化的方式输出分析结果。"""
        
        # 构建用户提示词
        user_prompt_parts = []
        
        # 构建多模态消息
        message_content = []
        
        # 添加文本部分
        text_part = f"""请分析这张图片，并生成适合在{target_platform}平台发布的营销文案。"""
        
        if product_name:
            text_part += f"\n相关产品：{product_name}"
        
        if marketing_angle:
            text_part += f"\n营销角度：{marketing_angle}"
        
        text_part += "\n\n请提供：\n1. 图片内容详细描述\n2. 情感氛围分析\n3. 营销文案（3个不同版本）\n4. 标签建议\n5. 发布时机建议"
        
        message_content.append({
            "type": "text",
            "text": text_part
        })
        
        # 添加图片部分
        message_content.append({
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        })
        
        # 获取API配置
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        if not api_key or not base_url:
            return "错误：未配置火山方舟大模型API环境变量。请确保COZE_WORKLOAD_IDENTITY_API_KEY和COZE_INTEGRATION_MODEL_BASE_URL已设置。"
        
        # 创建大模型客户端 - 使用视觉模型
        llm = ChatOpenAI(
            model="doubao-seed-1-6-vision-250815",  # 使用火山方舟的视觉模型
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,
            streaming=False,
            timeout=60,
            default_headers=default_headers(ctx) if ctx else {}
        )
        
        # 调用大模型
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message_content)
        ]
        
        response = llm.invoke(messages)
        
        # 返回分析结果
        result = f"# 图片营销分析报告\n\n"
        result += f"**图片URL**: {image_url}\n"
        if product_name:
            result += f"**相关产品**: {product_name}\n"
        result += f"**目标平台**: {target_platform}\n"
        if marketing_angle:
            result += f"**营销角度**: {marketing_angle}\n\n"
        
        result += "## 分析结果\n\n"
        # 确保response.content是字符串
        if isinstance(response.content, list):
            content_str = " ".join(str(item) for item in response.content)
        else:
            content_str = str(response.content)
        result += content_str
        
        return result
        
    except Exception as e:
        return f"图片分析过程中出现错误：{str(e)}"