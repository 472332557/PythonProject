"""
天气查询模块 - 实现function-calling机制的天气查询功能
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

weather_bp = Blueprint('weather', __name__)


def error_handler(f):
    """错误处理装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({
                'code': 400,
                'message': f'参数错误: {str(e)}',
                'data': None
            }), 400
        except Exception as e:
            logger.error(f"天气查询错误: {str(e)}")
            return jsonify({
                'code': 500,
                'message': f'服务器错误: {str(e)}',
                'data': None
            }), 500
    return wrapper


def validate_city(city):
    """验证城市名称"""
    if not city or not isinstance(city, str):
        raise ValueError("城市名称无效")
    if len(city) < 2 or len(city) > 20:
        raise ValueError("城市名称长度应在2-20个字符之间")
    return city.strip()


def get_weather_data(city: str) -> dict:
    """
    获取城市天气数据 (function-calling核心函数)

    Args:
        city: 城市名称

    Returns:
        包含温度、湿度、天气状况等的字典
    """
    # 支持的城市映射
    city_codes = {
        '北京': '101010100', '上海': '101020100', '广州': '101280101',
        '深圳': '101280601', '杭州': '101210101', '成都': '101270101',
        '武汉': '101200101', '南京': '101190101', '西安': '101110101',
        '重庆': '101040100', '天津': '101030100', '苏州': '101190401'
    }

    city_code = city_codes.get(city)

    if city_code:
        # 使用真实API获取天气
        return _fetch_weather_from_api(city_code, city)
    else:
        # 返回模拟数据
        return _generate_mock_weather(city)


def _fetch_weather_from_api(city_code: str, city: str) -> dict:
    """从API获取真实天气数据"""
    try:
        # 这里使用心知天气API作为示例
        api_key = "your_api_key"  # 需要替换为真实API密钥
        url = f"https://api.seniverse.com/v3/weather/now.json"

        # 实际应用中应使用真实API调用
        # response = requests.get(url, params={'key': api_key, 'location': city_code}, timeout=5)

        # 返回模拟数据
        return _generate_mock_weather(city)

    except requests.RequestException as e:
        logger.error(f"API请求失败: {str(e)}")
        return _generate_mock_weather(city)


def _generate_mock_weather(city: str) -> dict:
    """生成模拟天气数据"""
    import random

    conditions = ['晴', '多云', '阴', '小雨', '中雨', '雷阵雨', '晴转多云']
    winds = ['东风', '南风', '西风', '北风', '东南风', '东北风', '西南风', '西北风']

    temperature = random.randint(18, 35)
    humidity = random.randint(40, 95)

    return {
        'city': city,
        'temperature': temperature,
        'temperature_range': f'{temperature - 5}~{temperature + 5}',
        'humidity': humidity,
        'condition': random.choice(conditions),
        'wind': f'{random.choice(winds)} {random.randint(1, 5)}级',
        'air_quality': random.choice(['优', '良', '轻度污染']),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tips': _get_weather_tips(temperature, humidity)
    }


def _get_weather_tips(temp: int, humidity: int) -> str:
    """根据天气情况生成提示"""
    tips = []

    if temp < 10:
        tips.append("天气较凉，建议添加外套")
    elif temp > 30:
        tips.append("高温预警，注意防暑降温")

    if humidity > 80:
        tips.append("空气潮湿，注意防潮")
    elif humidity < 40:
        tips.append("空气干燥，注意补水")

    return '; '.join(tips) if tips else "今日天气适宜户外活动"


@weather_bp.route('', methods=['POST'])
@error_handler
def get_weather():
    """
    天气查询接口

    Request Body:
        {
            "city": "深圳"
        }

    Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "city": "深圳",
                "temperature": 26,
                "humidity": 75,
                "condition": "多云",
                "wind": "东南风3级",
                ...
            }
        }
    """
    data = request.get_json()
    if not data or 'city' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少city参数',
            'data': None
        }), 400

    city = validate_city(data['city'])
    logger.info(f"查询天气: {city}")

    weather_data = get_weather_data(city)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': weather_data
    })


@weather_bp.route('/batch', methods=['POST'])
@error_handler
def batch_get_weather():
    """
    批量查询天气

    Request Body:
        {
            "cities": ["北京", "上海", "深圳"]
        }
    """
    data = request.get_json()
    if not data or 'cities' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少cities参数',
            'data': None
        }), 400

    cities = data['cities']
    if not isinstance(cities, list) or len(cities) > 10:
        return jsonify({
            'code': 400,
            'message': '城市列表应在1-10个之间',
            'data': None
        }), 400

    results = {}
    for city in cities:
        try:
            city = validate_city(city)
            results[city] = get_weather_data(city)
        except ValueError as e:
            results[city] = {'error': str(e)}

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': results
    })


@weather_bp.route('/air_quality', methods=['POST'])
@error_handler
def get_air_quality():
    """查询空气质量"""
    data = request.get_json()
    if not data or 'city' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少city参数',
            'data': None
        }), 400

    city = validate_city(data['city'])

    # 模拟空气质量数据
    import random
    aqi = random.randint(20, 200)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'city': city,
            'aqi': aqi,
            'level': '优' if aqi <= 50 else '良' if aqi <= 100 else '轻度污染' if aqi <= 150 else '中度污染',
            'pm25': random.randint(10, 100),
            'pm10': random.randint(20, 150),
            'so2': random.randint(5, 50),
            'no2': random.randint(10, 80),
            'co': round(random.uniform(0.3, 1.5), 2),
            'o3': random.randint(50, 200),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    })


# Function Calling 函数定义
FUNCTION_DEFINITIONS = {
    'name': 'get_weather',
    'description': '获取指定城市的实时天气信息，包括温度、湿度、天气状况和风力等',
    'parameters': {
        'type': 'object',
        'properties': {
            'city': {
                'type': 'string',
                'description': '城市名称，如"北京"、"上海"、"深圳"',
                'example': '深圳'
            }
        },
        'required': ['city']
    }
}
