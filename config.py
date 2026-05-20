"""
配置文件 - 存储 API 密钥和其他配置
支持从 .env 文件加载配置
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# OpenAI API 配置 (Kimi 使用相同的接口)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.moonshot.cn/v1")

# 默认模型 - Kimi支持的模型: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "moonshot-v1-8k")

# API 基础URL（用于代理或兼容接口）
# 如果使用代理，设置为你的代理地址，例如：http://127.0.0.1:7890
API_PROXY_URL = ""

# 日志配置
LOG_LEVEL = "INFO"

# 功能开关
ENABLE_WEATHER = True
ENABLE_NEWS = True
ENABLE_DOCUMENT = True
ENABLE_EXCEL = True
