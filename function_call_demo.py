def get_weather(city: str) -> str:
    """
    获取指定城市的天气情况
    
    Args:
        city: 城市名称，如"北京"、"上海"
    
    Returns:
        天气信息字符串
    """
    weather_data = {
        "北京": "晴转多云，温度18-28°C，东北风3级",
        "上海": "阴有小雨，温度22-26°C，东南风2级",
        "广州": "晴，温度26-35°C，西南风4级",
        "深圳": "多云，温度25-33°C，东风2级",
        "杭州": "阵雨，温度20-27°C，西北风3级",
        "成都": "阴，温度16-24°C，北风2级",
        "武汉": "晴，温度19-30°C，南风3级",
        "南京": "多云转晴，温度17-28°C，东北风2级"
    }
    return weather_data.get(city, f"暂未获取到{city}的天气信息")


def get_fruit_guide(season: str) -> str:
    """
    获取指定季节的水果指南
    
    Args:
        season: 季节名称，如"春季"、"夏季"、"秋季"、"冬季"
    
    Returns:
        水果指南信息字符串
    """
    fruit_data = {
        "春季": "推荐水果：草莓、樱桃、枇杷、桑葚、菠萝。春季水果富含维生素C，帮助增强免疫力。",
        "夏季": "推荐水果：西瓜、桃子、葡萄、荔枝、芒果。夏季水果水分充足，清热解暑。",
        "秋季": "推荐水果：苹果、梨、柿子、石榴、猕猴桃。秋季水果有助于润燥养肺。",
        "冬季": "推荐水果：橙子、柚子、柑橘、香蕉、山楂。冬季水果富含维生素，预防感冒。"
    }
    return fruit_data.get(season, f"暂未获取到{season}的水果指南")


def get_city_intro(city: str) -> str:
    """
    获取指定城市的介绍
    
    Args:
        city: 城市名称，如"北京"、"上海"
    
    Returns:
        城市介绍信息字符串
    """
    city_data = {
        "北京": "北京是中华人民共和国的首都，是全国政治、文化中心。著名景点有故宫、天安门广场、八达岭长城等。",
        "上海": "上海是中国最大的经济中心和国际化大都市。著名景点有外滩、东方明珠、豫园等。",
        "广州": "广州是中国南方重要的港口城市，素有'羊城'之称。著名景点有广州塔、陈家祠、白云山等。",
        "深圳": "深圳是中国改革开放的窗口，现代化创新城市。著名景点有深圳湾公园、世界之窗、欢乐谷等。",
        "杭州": "杭州是著名的风景旅游城市，以西湖闻名于世。著名景点有西湖、灵隐寺、千岛湖等。",
        "成都": "成都是四川省省会，以美食和悠闲生活著称。著名景点有都江堰、青城山、宽窄巷子等。",
        "西安": "西安是中国历史文化名城，古称长安。著名景点有兵马俑、大雁塔、古城墙等。",
        "苏州": "苏州是江南水乡名城，以园林艺术闻名。著名景点有拙政园、留园、周庄古镇等。"
    }
    return city_data.get(city, f"暂未获取到{city}的城市介绍")


def function_call(func_name: str, **kwargs) -> str:
    """
    统一的函数调用接口
    
    Args:
        func_name: 要调用的函数名称，可选值：'get_weather', 'get_fruit_guide', 'get_city_intro'
        kwargs: 函数参数
    
    Returns:
        函数执行结果
    """
    functions = {
        "get_weather": get_weather,
        "get_fruit_guide": get_fruit_guide,
        "get_city_intro": get_city_intro
    }
    
    if func_name not in functions:
        return f"未知函数：{func_name}"
    
    try:
        return functions[func_name](**kwargs)
    except TypeError as e:
        return f"函数调用参数错误：{str(e)}"


if __name__ == "__main__":
    print("=== Function Call Demo ===")
    print()
    
    print("1. 天气查询示例：")
    print(function_call("get_weather", city="北京"))
    print()
    
    print("2. 水果指南示例：")
    print(function_call("get_fruit_guide", season="夏季"))
    print()
    
    print("3. 城市介绍示例：")
    print(function_call("get_city_intro", city="杭州"))
    print()
    
    print("=== 可用函数列表 ===")
    print("- get_weather(city): 获取天气情况")
    print("- get_fruit_guide(season): 获取水果指南")
    print("- get_city_intro(city): 获取城市介绍")