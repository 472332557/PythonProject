"""
LLM API 调用系统主模块
实现function-calling机制，支持天气查询、新闻聚合、文档读取、Excel知识库等功能
集成 OpenAI GPT 实现真正的 LLM Function Calling
"""

from flask import Flask, request, jsonify, render_template
from functools import wraps
import time
import logging
from datetime import datetime
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入功能模块
from modules.weather import weather_bp
from modules.news import news_bp
from modules.document import document_bp
from modules.excel_knowledge import excel_bp
from modules.security import rate_limit, require_api_key
from modules.llm import chat_with_llm

# 创建Flask应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.template_folder = 'templates'
app.static_folder = 'static'

# 注册蓝图
app.register_blueprint(weather_bp, url_prefix='/api/weather')
app.register_blueprint(news_bp, url_prefix='/api/news')
app.register_blueprint(document_bp, url_prefix='/api/document')
app.register_blueprint(excel_bp, url_prefix='/api/excel')

# API版本
API_VERSION = 'v2.0.0'
API_PREFIX = '/api/v1'


def validate_params(required_params):
    """参数验证装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json() or {}
            missing = [p for p in required_params if p not in data]
            if missing:
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填参数: {", ".join(missing)}',
                    'data': None
                }), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator


def error_handler(f):
    """统一错误处理装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"参数错误: {str(e)}")
            return jsonify({
                'code': 400,
                'message': f'参数错误: {str(e)}',
                'data': None
            }), 400
        except FileNotFoundError as e:
            logger.error(f"文件未找到: {str(e)}")
            return jsonify({
                'code': 404,
                'message': f'文件未找到: {str(e)}',
                'data': None
            }), 404
        except Exception as e:
            logger.error(f"服务器错误: {str(e)}")
            return jsonify({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }), 500
    return wrapper


@app.route('/')
def index():
    """API首页 - 返回HTML界面"""
    return render_template('index.html')


@app.route('/web')
def web_interface():
    """Web界面"""
    return render_template('index.html')


@app.route(f'{API_PREFIX}/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': API_VERSION
    })


@app.route(f'{API_PREFIX}/function_call', methods=['POST'])
@error_handler
@rate_limit(max_requests=100, window=60)
def function_call():
    """
    统一的function-calling接口
    支持动态调用各种功能函数
    """
    data = request.get_json()
    if not data or 'function_name' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少function_name参数',
            'data': None
        }), 400

    function_name = data['function_name']
    parameters = data.get('parameters', {})

    # 函数映射表
    function_map = {
        'get_weather': _call_weather,
        'get_news': _call_news,
        'read_document': _call_document,
        'query_excel': _call_excel
    }

    if function_name not in function_map:
        return jsonify({
            'code': 404,
            'message': f'未知函数: {function_name}',
            'data': None
        }), 404

    result = function_map[function_name](parameters)
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': result
    })


def _call_weather(params):
    """调用天气查询函数"""
    from modules.weather import get_weather_data
    city = params.get('city')
    if not city:
        raise ValueError("缺少city参数")
    return get_weather_data(city)


def _call_news(params):
    """调用新闻获取函数"""
    from modules.news import get_hot_news
    category = params.get('category', 'general')
    return get_hot_news(category)


def _call_document(params):
    """调用文档读取函数"""
    from modules.document import read_document
    file_path = params.get('file_path')
    if not file_path:
        raise ValueError("缺少file_path参数")
    return read_document(file_path)


def _call_excel(params):
    """调用Excel查询函数"""
    from modules.excel_knowledge import query_excel_data
    file_path = params.get('file_path')
    query = params.get('query')
    if not file_path:
        raise ValueError("缺少file_path参数")
    return query_excel_data(file_path, query)


@app.route(f'{API_PREFIX}/chat', methods=['POST'])
@error_handler
def chat():
    """
    LLM 聊天接口 - 实现真正的 Function Calling

    Request Body:
        {
            "message": "深圳天气怎么样？",
            "model": "gpt-4o",  // 可选，默认 gpt-4o
            "history": []       // 可选的对话历史
        }

    Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "response": "深圳今天天气...",
                "function_calls": [
                    {
                        "name": "get_weather",
                        "arguments": {"city": "深圳"},
                        "result": {...}
                    }
                ],
                "history": [...]
            }
        }
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少message参数',
            'data': None
        }), 400

    message = data['message']
    model = data.get('model', 'gpt-4o')
    history = data.get('history', [])

    # 获取 API 密钥（优先从请求中获取，其次从环境变量）
    api_key = data.get('api_key') or os.getenv('OPENAI_API_KEY')
    base_url = data.get('base_url') or os.getenv('OPENAI_BASE_URL')

    logger.info(f"Chat请求 - 模型: {model}, 消息: {message[:50]}...")

    # 调用 LLM
    result = chat_with_llm(
        message=message,
        model=model,
        history=history,
        api_key=api_key,
        base_url=base_url
    )

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': result
    })


@app.route(f'{API_PREFIX}/docs')
def api_docs():
    """API文档"""
    docs = {
        'title': 'LLM API 调用系统文档',
        'version': API_VERSION,
        'base_url': request.host_url.rstrip('/'),
        'endpoints': [
            {
                'path': '/api/v1/weather',
                'method': 'POST',
                'description': '查询城市天气',
                'parameters': {
                    'city': '城市名称 (必填)'
                },
                'response': {
                    'temperature': '温度 (°C)',
                    'humidity': '湿度 (%)',
                    'condition': '天气状况',
                    'wind': '风力风向'
                }
            },
            {
                'path': '/api/v1/news',
                'method': 'POST',
                'description': '获取热门新闻',
                'parameters': {
                    'category': '新闻分类 (可选: general/politics/tech/sports/entertainment)'
                },
                'response': {
                    'title': '新闻标题',
                    'source': '来源',
                    'publish_time': '发布时间',
                    'summary': '摘要'
                }
            },
            {
                'path': '/api/v1/document/read',
                'method': 'POST',
                'description': '读取文档内容',
                'parameters': {
                    'file_path': '文件路径 (必填)',
                    'format': '文档格式 (pdf/word/txt)'
                }
            },
            {
                'path': '/api/v1/excel/query',
                'method': 'POST',
                'description': '查询Excel数据',
                'parameters': {
                    'file_path': 'Excel文件路径 (必填)',
                    'query': '查询条件 (可选)',
                    'sheet_name': '工作表名称 (可选)'
                }
            }
        ],
        'error_codes': {
            400: '请求参数错误',
            401: '未授权访问',
            403: '禁止访问/权限不足',
            404: '资源未找到',
            429: '请求频率超限',
            500: '服务器内部错误'
        }
    }
    return jsonify(docs)


if __name__ == '__main__':
    print(f"启动 LLM API 调用系统 v{API_VERSION.replace('v', '')}")
    print("=" * 50)
    print("可用端点:")
    print(f"  - Web界面: GET /")
    print(f"  - LLM对话: POST /api/v1/chat")
    print(f"  - 天气查询: POST /api/v1/weather")
    print(f"  - 新闻聚合: POST /api/v1/news")
    print(f"  - 文档读取: POST /api/v1/document/read")
    print(f"  - Excel查询: POST /api/v1/excel/query")
    print(f"  - API文档: GET /api/v1/docs")
    print("=" * 50)
    print("! 请设置 OPENAI_API_KEY 环境变量以启用 LLM Function Calling")
    print("   Windows: set OPENAI_API_KEY=your-key")
    print("   Linux/Mac: export OPENAI_API_KEY=your-key")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)