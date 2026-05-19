# LLM API 调用系统 - 完整API文档

## 概述

LLM API 调用系统是一个基于 Flask 的 RESTful API 服务，实现了 Function Calling 机制，支持天气查询、新闻聚合、文档读取、Excel 知识库等功能。

## 项目结构

```
PythonProject/
├── api_server.py          # 主服务器文件
├── modules/
│   ├── __init__.py
│   ├── weather.py         # 天气查询模块
│   ├── news.py            # 新闻聚合模块
│   ├── document.py        # 文档读取模块
│   ├── excel_knowledge.py # Excel知识库模块
│   └── security.py        # 安全模块
├── requirements.txt       # 依赖包
└── README_API.md          # API文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python api_server.py
```

服务将在 `http://0.0.0.0:5000` 启动。

### 3. 获取API文档

```bash
curl http://localhost:5000/api/v1/docs
```

---

## API 端点

### 基础信息

- **Base URL**: `http://localhost:5000/api/v1`
- **Content-Type**: `application/json`
- **认证方式**: `X-API-Key` 请求头

### 健康检查

#### GET /api/v1/health

检查服务健康状态。

**响应示例:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-19T10:30:00",
  "version": "v1.0.0"
}
```

---

## Function Calling 接口

### POST /api/v1/function_call

统一的 Function Calling 接口，可调用所有功能函数。

**请求头:**
```
X-API-Key: your_api_key
Content-Type: application/json
```

**请求体:**
```json
{
  "function_name": "get_weather",
  "parameters": {
    "city": "深圳"
  }
}
```

**支持的函数:**

| 函数名 | 描述 | 必需参数 |
|--------|------|----------|
| `get_weather` | 获取城市天气 | city |
| `get_news` | 获取热门新闻 | - |
| `read_document` | 读取文档 | file_path |
| `query_excel` | 查询Excel数据 | file_path |

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "city": "深圳",
    "temperature": 26,
    "humidity": 75,
    "condition": "多云",
    "wind": "东南风3级"
  }
}
```

---

## 天气查询 API

### POST /api/v1/weather

查询指定城市的实时天气。

**请求体:**
```json
{
  "city": "深圳"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "city": "深圳",
    "temperature": 26,
    "temperature_range": "21~31",
    "humidity": 75,
    "condition": "多云",
    "wind": "东南风3级",
    "air_quality": "良",
    "update_time": "2026-05-19 10:30:00",
    "tips": "今日天气适宜户外活动"
  }
}
```

**支持城市:**
北京、上海、广州、深圳、杭州、成都、武汉、南京、西安、重庆、天津、苏州

---

## 新闻聚合 API

### POST /api/v1/news

获取当天最热门的新闻。

**请求体:**
```json
{
  "category": "tech",
  "count": 10
}
```

**参数说明:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 新闻分类，默认 general |
| count | integer | 否 | 返回数量，默认10，最大50 |

**分类选项:**
- `general` - 综合
- `politics` - 政治
- `tech` - 科技
- `sports` - 体育
- `entertainment` - 娱乐
- `economy` - 经济
- `society` - 社会
- `international` - 国际

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 10,
    "category": "科技",
    "news": [
      {
        "id": "news_tech_1",
        "title": "华为发布新一代鸿蒙操作系统",
        "source": "科技日报",
        "publish_time": "2026-05-19 10:30:00",
        "summary": "分布式能力进一步提升，生态更加完善",
        "hot_score": 8500
      }
    ]
  }
}
```

### GET /api/v1/news/headlines

获取各分类的头条新闻。

---

## 文档读取 API

### POST /api/v1/document/read

读取并解析常见格式文档。

**请求体:**
```json
{
  "file_path": "/path/to/document.pdf",
  "max_length": 50000
}
```

**支持的格式:**
- `txt` - 文本文件
- `pdf` - PDF文档
- `doc` / `docx` - Word文档
- `md` - Markdown

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "file_name": "document.pdf",
    "file_size": 1024000,
    "format": "pdf",
    "content": "文档内容...",
    "char_count": 12345,
    "word_count": 3500,
    "key_info": {
      "emails": ["example@email.com"],
      "phone_numbers": ["13800138000"],
      "urls": ["https://example.com"]
    }
  }
}
```

### POST /api/v1/document/search

在文档中搜索关键词。

**请求体:**
```json
{
  "file_path": "/path/to/document.pdf",
  "keyword": "关键词",
  "case_sensitive": false
}
```

---

## Excel 知识库 API

### POST /api/v1/excel/query

查询 Excel 数据。

**请求体:**
```json
{
  "file_path": "/path/to/data.xlsx",
  "query": "age>25,department=技术部",
  "sheet_name": "Sheet1"
}
```

**查询语法:**
- `column=value` - 等于
- `column>value` - 大于
- `column<value` - 小于
- `column!=value` - 不等于
- `column like %value%` - 包含

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "file_name": "data.xlsx",
    "total_rows": 1000,
    "columns": ["name", "age", "department", "salary"],
    "data": [
      {"name": "张三", "age": 28, "department": "技术部", "salary": 15000}
    ],
    "statistics": {
      "numeric_columns": [
        {"name": "age", "min": 22, "max": 60, "mean": 35.5}
      ]
    }
  }
}
```

### POST /api/v1/excel/aggregate

Excel 数据聚合分析。

**请求体:**
```json
{
  "file_path": "/path/to/data.xlsx",
  "group_by": "department",
  "aggregations": [
    {"column": "salary", "func": "sum"},
    {"column": "salary", "func": "avg"},
    {"column": "name", "func": "count"}
  ]
}
```

---

## 认证与权限

### API 密钥

使用 `X-API-Key` 请求头传递 API 密钥。

**测试密钥:**
- `dev_key_12345` - 开发密钥 (premium级别，100请求/分钟)
- `test_key_67890` - 测试密钥 (basic级别，20请求/分钟)

### 权限级别

| 级别 | 说明 |
|------|------|
| basic | 基础权限 |
| standard | 标准权限 |
| premium | 高级权限 |
| admin | 管理员权限 |

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权访问 |
| 403 | 禁止访问/权限不足 |
| 404 | 资源未找到 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

**错误响应格式:**
```json
{
  "code": 400,
  "message": "缺少必填参数: city",
  "data": null
}
```

---

## 使用示例

### cURL 示例

```bash
# 查询天气
curl -X POST http://localhost:5000/api/v1/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "深圳"}'

# 获取新闻
curl -X POST http://localhost:5000/api/v1/news \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev_key_12345" \
  -d '{"category": "tech", "count": 5}'

# Function Calling
curl -X POST http://localhost:5000/api/v1/function_call \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev_key_12345" \
  -d '{
    "function_name": "get_weather",
    "parameters": {"city": "上海"}
  }'
```

### Python 示例

```python
import requests

# 查询天气
response = requests.post(
    'http://localhost:5000/api/v1/weather',
    json={'city': '深圳'}
)
print(response.json())

# Function Calling
response = requests.post(
    'http://localhost:5000/api/v1/function_call',
    headers={'X-API-Key': 'dev_key_12345'},
    json={
        'function_name': 'get_weather',
        'parameters': {'city': '北京'}
    }
)
print(response.json())
```

---

## 速率限制

| 密钥级别 | 请求限制 |
|----------|----------|
| basic | 20请求/分钟 |
| premium | 100请求/分钟 |

超出限制将返回 429 错误码，包含 `retry_after` 字段告知重试时间。

---

## 依赖包

```
Flask>=2.0.0
pandas>=1.3.0
python-docx>=0.8.11
PyPDF2>=1.26.0
pdfminer>=20191125
openpyxl>=3.0.0
```
