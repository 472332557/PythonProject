"""
新闻聚合模块 - 实现热门新闻获取功能
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import logging
import requests
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

news_bp = Blueprint('news', __name__)


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
            logger.error(f"新闻获取错误: {str(e)}")
            return jsonify({
                'code': 500,
                'message': f'服务器错误: {str(e)}',
                'data': None
            }), 500
    return wrapper


CATEGORY_MAP = {
    'general': '综合',
    'politics': '政治',
    'tech': '科技',
    'sports': '体育',
    'entertainment': '娱乐',
    'economy': '经济',
    'society': '社会',
    'international': '国际'
}


def get_hot_news(category: str = 'general', count: int = 10) -> list:
    """
    获取热门新闻 (function-calling核心函数)

    Args:
        category: 新闻分类
        count: 返回数量，默认10条

    Returns:
        包含标题、来源、发布时间和摘要的新闻列表
    """
    if count < 1 or count > 50:
        raise ValueError("新闻数量应在1-50之间")

    # 实际应用中应调用真实新闻API
    # 这里使用模拟数据
    return _generate_mock_news(category, count)


def _generate_mock_news(category: str, count: int) -> list:
    """生成模拟新闻数据"""
    category_name = CATEGORY_MAP.get(category, '综合')

    news_templates = {
        'general': [
            ("国家发改委发布最新经济数据", "新华社", "一季度GDP增长5.3%，经济运行开局良好"),
            ("多地迎来降雨天气，部分地区有暴雨", "中国气象网", "专家提醒注意防范次生灾害"),
            ("五一假期旅游市场持续火爆", "人民日报", "预计接待游客超过2亿人次"),
            ("医保支付方式改革全面推开", "光明日报", "将进一步减轻患者就医负担"),
            ("食品安全监管力度持续加强", "市场监督管理报", "开展专项整治行动")
        ],
        'tech': [
            ("华为发布新一代鸿蒙操作系统", "科技日报", "分布式能力进一步提升，生态更加完善"),
            ("人工智能在医疗领域取得新突破", "中国科学报", "AI辅助诊断准确率超过95%"),
            ("新能源汽车销量持续增长", "汽车之家", "渗透率首次超过50%"),
            ("量子计算原型机研制成功", "中科院之声", "实现里程碑式突破"),
            ("5G网络覆盖进一步扩大", "人民邮电报", "基站总数超过350万座")
        ],
        'politics': [
            ("全国两会圆满闭幕", "新华网", "审议通过多项重要决议"),
            ("中央深改委召开会议", "央视新闻", "部署2026年重点改革任务"),
            ("外交部长访问欧洲多国", "外交部官网", "深化中欧全面战略伙伴关系"),
            ("乡村振兴战略深入推进", "农业农村部", "农民收入持续增长"),
            ("反腐倡廉工作取得新成效", "中央纪委国家监委", "营造风清气正的政治生态")
        ],
        'sports': [
            ("中国队在亚运会再获金牌", "体育总局", "金牌总数已突破100枚"),
            ("中超联赛新赛季开幕", "足球报", "多支球队引进强力外援"),
            ("CBA总决赛即将开战", "篮球先锋报", "粤辽两队再次对决"),
            ("马拉松运动在全国蓬勃发展", "中国田径协会", "全年举办超过500场赛事"),
            ("电子竞技成为亚运会正式项目", "电竞之家", "中国战队备战中")
        ],
        'entertainment': [
            ("年度票房突破600亿", "电影频道", "国产电影占比超过80%"),
            ("多部国产剧集海外热播", "文汇报", "中国文化软实力不断提升"),
            ("音乐节巡演火热进行", "娱乐周刊", "周杰伦等多位顶流歌手举办演唱会"),
            ("短视频平台规范发展", "网络视听节目管理司", "推动内容精品化"),
            ("电竞产业规模持续扩大", "游戏陀螺", "相关人才需求激增")
        ],
        'economy': [
            ("央行宣布降准0.25个百分点", "金融时报", "释放长期资金约5000亿元"),
            ("外贸进出口保持增长态势", "海关总署", "一季度出口同比增长4.9%"),
            ("房地产市场总体平稳", "住房城乡建设部", "因城施策效果显现"),
            ("数字经济成为增长新引擎", "经济参考报", "占GDP比重超过40%"),
            ("消费市场持续回暖", "商务部", "实体零售明显复苏")
        ],
        'society': [
            ("高等教育入学率进一步提高", "教育部", "毛入学率已达60%"),
            ("养老服务体系不断完善", "民政部", "社区养老覆盖率达到95%"),
            ("公共交通出行更加便捷", "交通运输部", "城市公交网络持续优化"),
            ("就业形势总体稳定", "人力资源社会保障部", "城镇新增就业完成目标"),
            ("志愿服务蓬勃发展", "共青团中央", "注册志愿者超过2亿人")
        ],
        'international': [
            ("G20峰会成功举行", "新华社", "就全球经济治理达成重要共识"),
            ("中国与多国签署合作文件", "外交部", "高质量共建一带一路"),
            ("联合国安理会召开会议", "联合国官网", "讨论国际热点问题"),
            ("全球气候治理取得进展", "中新社", "多国承诺碳中和目标"),
            ("国际航班逐步恢复", "民航资源网", "跨境出行更加便利")
        ]
    }

    templates = news_templates.get(category, news_templates['general'])

    news_list = []
    base_time = datetime.now()

    for i, (title, source, summary) in enumerate(templates[:count]):
        # 添加一些变化使新闻不完全相同
        variation = random.randint(0, 9)
        news_list.append({
            'id': f'news_{category}_{i+1}_{variation}',
            'title': title if variation < 7 else f'{title}（续）' if variation < 9 else f'最新：{title}',
            'source': source,
            'category': category_name,
            'publish_time': (base_time - timedelta(minutes=i*random.randint(10, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            'summary': summary,
            'hot_score': random.randint(1000, 10000),
            'image_url': None,
            'url': f'https://news.example.com/article/{category}/{i+1}'
        })

    # 按热度排序
    news_list.sort(key=lambda x: x['hot_score'], reverse=True)

    return news_list


@news_bp.route('', methods=['POST'])
@error_handler
def get_news():
    """
    获取热门新闻接口

    Request Body:
        {
            "category": "tech",  // 可选: general/politics/tech/sports/entertainment/economy/society/international
            "count": 10          // 可选，默认10
        }

    Response:
        {
            "code": 200,
            "message": "success",
            "data": [
                {
                    "id": "news_tech_1",
                    "title": "华为发布新一代鸿蒙操作系统",
                    "source": "科技日报",
                    "publish_time": "2026-05-19 10:30:00",
                    "summary": "分布式能力进一步提升，生态更加完善",
                    "hot_score": 8500,
                    ...
                }
            ]
        }
    """
    data = request.get_json() or {}
    category = data.get('category', 'general')
    count = min(data.get('count', 10), 50)

    if category not in CATEGORY_MAP:
        return jsonify({
            'code': 400,
            'message': f'无效的新闻分类: {category}',
            'data': None
        }), 400

    logger.info(f"获取{category}类新闻，数量: {count}")

    news_data = get_hot_news(category, count)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'total': len(news_data),
            'category': CATEGORY_MAP[category],
            'news': news_data
        }
    })


@news_bp.route('/headlines', methods=['GET'])
@error_handler
def get_headlines():
    """获取各分类头条新闻"""
    headlines = {}
    for cat in CATEGORY_MAP.keys():
        news = get_hot_news(cat, 1)
        if news:
            headlines[cat] = news[0]

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': headlines
    })


@news_bp.route('/search', methods=['POST'])
@error_handler
def search_news():
    """
    搜索新闻

    Request Body:
        {
            "keyword": "华为",
            "count": 10
        }
    """
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少keyword参数',
            'data': None
        }), 400

    keyword = data['keyword']
    count = min(data.get('count', 10), 50)

    # 模拟搜索结果
    results = []
    for i in range(min(count, 5)):
        results.append({
            'id': f'search_{i+1}',
            'title': f'关于{keyword}的最新消息（第{i+1}条）',
            'source': random.choice(['新华社', '人民日报', '央视新闻', '科技日报']),
            'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': f'这里是关于{keyword}的相关报道详细内容...',
            'relevance_score': random.randint(70, 99)
        })

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'keyword': keyword,
            'total': len(results),
            'results': results
        }
    })


# Function Calling 函数定义
FUNCTION_DEFINITIONS = {
    'name': 'get_news',
    'description': '获取当天最热门的新闻，支持多种分类',
    'parameters': {
        'type': 'object',
        'properties': {
            'category': {
                'type': 'string',
                'description': '新闻分类，可选值: general/politics/tech/sports/entertainment/economy/society/international',
                'example': 'tech'
            },
            'count': {
                'type': 'integer',
                'description': '返回新闻数量，默认10条，最多50条',
                'example': 10
            }
        },
        'required': []
    }
}
