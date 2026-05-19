"""
安全模块 - 实现权限控制和请求频率限制
"""

from flask import request, jsonify
from functools import wraps
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

# API密钥存储 (生产环境应使用数据库)
API_KEYS = {
    'dev_key_12345': {
        'name': '开发密钥',
        'level': 'premium',
        'rate_limit': (100, 60),  # 100请求/60秒
        'enabled': True
    },
    'test_key_67890': {
        'name': '测试密钥',
        'level': 'basic',
        'rate_limit': (20, 60),  # 20请求/60秒
        'enabled': True
    }
}

# 存储请求记录
request_records = defaultdict(list)


def require_api_key(f):
    """API密钥验证装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            logger.warning(f"缺少API密钥 - IP: {request.remote_addr}")
            return jsonify({
                'code': 401,
                'message': '缺少API密钥',
                'data': None
            }), 401

        if api_key not in API_KEYS:
            logger.warning(f"无效API密钥: {api_key[:10]}... - IP: {request.remote_addr}")
            return jsonify({
                'code': 401,
                'message': '无效的API密钥',
                'data': None
            }), 401

        key_info = API_KEYS[api_key]
        if not key_info['enabled']:
            logger.warning(f"禁用API密钥: {api_key[:10]}...")
            return jsonify({
                'code': 403,
                'message': 'API密钥已被禁用',
                'data': None
            }), 403

        # 将密钥信息附加到请求上下文
        request.api_key_info = key_info
        return f(*args, **kwargs)
    return wrapper


def rate_limit(max_requests=60, window=60):
    """
    请求频率限制装饰器
    基于令牌桶算法实现

    Args:
        max_requests: 时间窗口内最大请求数
        window: 时间窗口秒数
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 获取客户端标识
            client_id = _get_client_id()

            # 获取密钥级别限制
            key_limit = getattr(request, 'api_key_info', {}).get('rate_limit')
            if key_limit:
                max_requests, window = key_limit

            current_time = time.time()

            # 清理过期记录
            cutoff_time = current_time - window
            request_records[client_id] = [
                t for t in request_records[client_id]
                if t > cutoff_time
            ]

            # 检查频率限制
            if len(request_records[client_id]) >= max_requests:
                retry_after = int(window - (current_time - request_records[client_id][0]))
                logger.warning(
                    f"频率限制触发 - 客户端: {client_id}, "
                    f"请求数: {len(request_records[client_id])}/{max_requests}"
                )
                return jsonify({
                    'code': 429,
                    'message': '请求频率超限，请稍后再试',
                    'data': {
                        'retry_after': retry_after,
                        'limit': max_requests,
                        'window': window
                    }
                }), 429

            # 记录请求
            request_records[client_id].append(current_time)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def _get_client_id():
    """
    获取客户端唯一标识
    优先使用API密钥，其次使用IP+User-Agent
    """
    api_key = request.headers.get('X-API-Key')
    if api_key:
        return f"key:{hashlib.md5(api_key.encode()).hexdigest()[:16]}"

    # 使用IP和User-Agent组合
    identifier = f"{request.remote_addr}:{request.headers.get('User-Agent', 'unknown')}"
    return f"ip:{hashlib.md5(identifier.encode()).hexdigest()[:16]}"


def check_permission(required_level):
    """
    权限级别检查装饰器
    级别: basic < standard < premium < admin
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key_info = getattr(request, 'api_key_info', None)
            if not key_info:
                return jsonify({
                    'code': 401,
                    'message': '需要API密钥',
                    'data': None
                }), 401

            level_hierarchy = ['basic', 'standard', 'premium', 'admin']
            user_level = key_info.get('level', 'basic')

            if level_hierarchy.index(user_level) < level_hierarchy.index(required_level):
                logger.warning(
                    f"权限不足 - 用户级别: {user_level}, 要求: {required_level}"
                )
                return jsonify({
                    'code': 403,
                    'message': f'权限不足，需要{required_level}级别',
                    'data': None
                }), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator


class RateLimiter:
    """速率限制器类，支持更细粒度的控制"""

    def __init__(self):
        self.buckets = defaultdict(lambda: {
            'tokens': 100,
            'last_update': time.time()
        })

    def consume(self, client_id, cost=1):
        """
        消费一个令牌
        返回是否允许请求
        """
        bucket = self.buckets[client_id]
        now = time.time()

        # 每秒补充10个令牌
        elapsed = now - bucket['last_update']
        bucket['tokens'] = min(100, bucket['tokens'] + elapsed * 10)
        bucket['last_update'] = now

        if bucket['tokens'] >= cost:
            bucket['tokens'] -= cost
            return True, bucket['tokens']
        return False, bucket['tokens']

    def get_remaining(self, client_id):
        """获取剩余令牌数"""
        return self.buckets[client_id]['tokens']


# 全局速率限制器实例
global_limiter = RateLimiter()
