"""
LLM 集成模块 - 实现与 OpenAI GPT 的 Function Calling 交互
"""

import os
import sys
import openai
import json
import logging
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import OPENAI_API_KEY, OPENAI_BASE_URL, DEFAULT_MODEL
except ImportError:
    # 如果配置文件不存在，使用环境变量
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
    DEFAULT_MODEL = "gpt-4o"

logger = logging.getLogger(__name__)


class FunctionCallingAgent:
    """Function Calling 代理类"""

    # 可用函数定义 - 对应 OpenAI 的 tools 格式
    FUNCTIONS = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的实时天气信息，包括温度、湿度、天气状况和风力等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如'北京'、'上海'、'深圳'",
                            "example": "深圳"
                        }
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_news",
                "description": "获取当天最热门的新闻，支持多种分类",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "新闻分类，可选值: general/politics/tech/sports/entertainment/economy/society/international",
                            "example": "tech"
                        },
                        "count": {
                            "type": "integer",
                            "description": "返回新闻数量，默认10条，最多50条",
                            "example": 10
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_document",
                "description": "读取并解析常见格式文档(PDF、Word、TXT、Markdown)，提取文档内容和关键信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文档的完整路径",
                            "example": "/path/to/document.pdf"
                        },
                        "max_length": {
                            "type": "integer",
                            "description": "最大读取字符数，默认50000",
                            "example": 50000
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "query_excel",
                "description": "读取Excel文件并执行数据查询、搜索和统计分析",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Excel文件的完整路径",
                            "example": "/path/to/data.xlsx"
                        },
                        "query": {
                            "type": "string",
                            "description": "查询条件，支持格式: column=value, column>value, column<value, column!=value, column like %value%",
                            "example": "age>25,department=技术部"
                        },
                        "sheet_name": {
                            "type": "string",
                            "description": "工作表名称，不传则默认读取第一个工作表",
                            "example": "Sheet1"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }
    ]

    # 函数名到本地函数的映射
    FUNCTION_MAP = {
        "get_weather": "_call_get_weather",
        "get_news": "_call_get_news",
        "read_document": "_call_read_document",
        "query_excel": "_call_query_excel"
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """初始化 LLM 代理"""
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url or OPENAI_BASE_URL

        # 配置 OpenAI 客户端
        if self.base_url:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def chat(
        self,
        message: str,
        model: str = "gpt-4o",
        history: List[Dict[str, str]] = None,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        处理聊天请求，自动执行 Function Calling

        Args:
            message: 用户消息
            model: 使用的模型
            history: 对话历史
            max_iterations: 最大迭代次数（防止无限循环）

        Returns:
            包含响应文本、函数调用记录和更新后的历史
        """
        # 初始化消息历史
        if history is None:
            history = []

        # 添加用户消息
        messages = history + [{"role": "user", "content": message}]

        function_calls_record = []
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                # 调用 OpenAI API
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=self.FUNCTIONS,
                    tool_choice="auto",
                    temperature=0.7
                )

                assistant_message = response.choices[0].message

                # 检查是否有函数调用
                if assistant_message.tool_calls:
                    # 添加助手的函数调用消息
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": tc.type,
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })

                    # 执行每个函数调用
                    for tc in assistant_message.tool_calls:
                        function_name = tc.function.name
                        arguments = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments

                        logger.info(f"执行函数调用: {function_name}, 参数: {arguments}")

                        # 调用本地函数
                        result = self._execute_function(function_name, arguments)

                        # 添加函数结果到消息历史
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(result, ensure_ascii=False)
                        })

                        function_calls_record.append({
                            "name": function_name,
                            "arguments": arguments,
                            "result": result
                        })

                else:
                    # 没有函数调用，返回最终结果
                    final_response = assistant_message.content or "抱歉，我没有理解您的问题。"

                    # 更新历史
                    messages.append({"role": "assistant", "content": final_response})

                    return {
                        "response": final_response,
                        "function_calls": function_calls_record,
                        "history": messages[1:]  # 去除初始空历史
                    }

            except openai.APIError as e:
                logger.error(f"OpenAI API 错误: {str(e)}")
                return {
                    "response": f"API 调用错误: {str(e)}",
                    "function_calls": function_calls_record,
                    "history": history
                }
            except Exception as e:
                logger.error(f"未知错误: {str(e)}")
                return {
                    "response": f"发生错误: {str(e)}",
                    "function_calls": function_calls_record,
                    "history": history
                }

        # 达到最大迭代次数
        return {
            "response": "对话处理超时，请稍后重试。",
            "function_calls": function_calls_record,
            "history": messages[1:]
        }

    def _execute_function(self, function_name: str, arguments: Dict) -> Any:
        """执行本地函数"""
        from modules.weather import get_weather_data
        from modules.news import get_hot_news
        from modules.document import read_document
        from modules.excel_knowledge import query_excel_data

        function_map = {
            "get_weather": lambda args: get_weather_data(args.get("city")),
            "get_news": lambda args: get_hot_news(
                args.get("category", "general"),
                args.get("count", 10)
            ),
            "read_document": lambda args: read_document(
                args.get("file_path"),
                args.get("max_length", 50000)
            ),
            "query_excel": lambda args: query_excel_data(
                args.get("file_path"),
                args.get("query"),
                args.get("sheet_name")
            )
        }

        if function_name in function_map:
            try:
                result = function_map[function_name](arguments)
                return result
            except Exception as e:
                logger.error(f"函数执行错误: {str(e)}")
                return {"error": str(e)}
        else:
            return {"error": f"未知函数: {function_name}"}

    def _call_get_weather(self, city: str) -> Dict:
        """调用天气函数"""
        from modules.weather import get_weather_data
        return get_weather_data(city)

    def _call_get_news(self, category: str = "general", count: int = 10) -> Dict:
        """调用新闻函数"""
        from modules.news import get_hot_news
        return {"news": get_hot_news(category, count)}

    def _call_read_document(self, file_path: str, max_length: int = 50000) -> Dict:
        """调用文档读取函数"""
        from modules.document import read_document
        return read_document(file_path, max_length)

    def _call_query_excel(self, file_path: str, query: str = None, sheet_name: str = None) -> Dict:
        """调用Excel查询函数"""
        from modules.excel_knowledge import query_excel_data
        return query_excel_data(file_path, query, sheet_name)


# 全局单例
_agent = None


def get_agent(api_key: str = None, base_url: str = None) -> FunctionCallingAgent:
    """获取 LLM 代理单例"""
    global _agent
    if _agent is None:
        _agent = FunctionCallingAgent(api_key, base_url)
    return _agent


def chat_with_llm(
    message: str,
    model: str = "gpt-4o",
    history: List[Dict[str, str]] = None,
    api_key: str = None,
    base_url: str = None
) -> Dict[str, Any]:
    """
    便捷函数：与 LLM 对话

    Args:
        message: 用户消息
        model: 使用的模型
        history: 对话历史
        api_key: OpenAI API 密钥
        base_url: API 基础URL（用于代理）

    Returns:
        包含响应文本、函数调用记录和更新后的历史
    """
    agent = get_agent(api_key, base_url)
    return agent.chat(message, model, history)
