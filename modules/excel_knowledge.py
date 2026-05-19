"""
Excel知识库模块 - 实现Excel文件的读取、数据查询和统计分析能力
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import logging
import os
import re
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)

excel_bp = Blueprint('excel', __name__)


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
        except FileNotFoundError as e:
            return jsonify({
                'code': 404,
                'message': f'文件未找到: {str(e)}',
                'data': None
            }), 404
        except Exception as e:
            logger.error(f"Excel处理错误: {str(e)}")
            return jsonify({
                'code': 500,
                'message': f'服务器错误: {str(e)}',
                'data': None
            }), 500
    return wrapper


def validate_file_path(file_path: str) -> str:
    """验证文件路径"""
    if not file_path:
        raise ValueError("文件路径不能为空")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.xlsx', '.xls', '.csv']:
        raise ValueError(f"不支持的文件格式: {ext}，仅支持.xlsx/.xls/.csv")

    # 检查文件大小 (限制100MB)
    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:
        raise ValueError("文件大小超过100MB限制")

    return file_path


def query_excel_data(file_path: str, query: str = None, sheet_name: str = None) -> dict:
    """
    查询Excel数据 (function-calling核心函数)

    Args:
        file_path: Excel文件路径
        query: 查询条件 (可选)
        sheet_name: 工作表名称 (可选)

    Returns:
        包含查询结果的字典
    """
    file_path = validate_file_path(file_path)

    # 读取Excel文件
    if file_path.endswith('.csv'):
        import pandas as pd
        df = pd.read_csv(file_path)
    else:
        import pandas as pd
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names

        if sheet_name and sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        elif sheet_name:
            raise ValueError(f"未找到工作表: {sheet_name}")
        else:
            # 默认读取第一个工作表
            df = pd.read_excel(file_path, sheet_name=0)

    result = {
        'file_name': os.path.basename(file_path),
        'sheet_name': sheet_name or 'Sheet1',
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns)
    }

    if query:
        # 执行查询
        filtered_df = _execute_query(df, query)
        result['query'] = query
        result['filtered_rows'] = len(filtered_df)
        result['data'] = _df_to_records(filtered_df)
    else:
        # 返回所有数据（限制数量）
        result['data'] = _df_to_records(df.head(1000))
        result['display_rows'] = min(len(df), 1000)

    # 添加统计信息
    result['statistics'] = _generate_statistics(df)

    return result


def _execute_query(df, query: str):
    """执行查询条件"""
    # 简单的查询语法支持
    # 格式: column=value, column>value, column<value, column like %value%

    conditions = query.split(',')
    filtered_df = df

    for condition in conditions:
        condition = condition.strip()
        if not condition:
            continue

        # 等于
        if '=' in condition and '!=' not in condition:
            col, val = condition.split('=', 1)
            col = col.strip()
            val = val.strip().strip('"\'')
            if col in df.columns:
                filtered_df = filtered_df[filtered_df[col].astype(str) == val]

        # 不等于
        elif '!=' in condition:
            col, val = condition.split('!=', 1)
            col = col.strip()
            val = val.strip().strip('"\'')
            if col in df.columns:
                filtered_df = filtered_df[filtered_df[col].astype(str) != val]

        # 大于
        elif '>' in condition:
            col, val = condition.split('>', 1)
            col = col.strip()
            try:
                val = float(val.strip())
                if col in df.columns:
                    filtered_df = filtered_df[pd.to_numeric(filtered_df[col], errors='coerce') > val]
            except ValueError:
                pass

        # 小于
        elif '<' in condition:
            col, val = condition.split('<', 1)
            col = col.strip()
            try:
                val = float(val.strip())
                if col in df.columns:
                    filtered_df = filtered_df[pd.to_numeric(filtered_df[col], errors='coerce') < val]
            except ValueError:
                pass

        # LIKE
        elif ' like ' in condition.lower():
            parts = re.split(r'\s+like\s+', condition, flags=re.IGNORECASE)
            if len(parts) == 2:
                col, val = parts[0].strip(), parts[1].strip().strip('"\'')
                val = val.replace('%', '')
                if col in df.columns:
                    filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(val, na=False)]

    return filtered_df


def _df_to_records(df):
    """将DataFrame转换为记录列表"""
    import pandas as pd

    # 处理数据类型
    records = []
    for _, row in df.iterrows():
        record = {}
        for col, val in row.items():
            if pd.isna(val):
                record[col] = None
            elif isinstance(val, (pd.Timestamp, datetime)):
                record[col] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, (int, float)):
                if val == int(val):
                    record[col] = int(val)
                else:
                    record[col] = round(val, 4)
            else:
                record[col] = str(val)
        records.append(record)

    return records


def _generate_statistics(df):
    """生成数据统计信息"""
    import pandas as pd

    stats = {
        'numeric_columns': [],
        'text_columns': []
    }

    for col in df.columns:
        col_data = df[col]
        non_null = col_data.dropna()

        if len(non_null) == 0:
            continue

        # 尝试识别数值列
        try:
            numeric_data = pd.to_numeric(col_data, errors='coerce').dropna()
            if len(numeric_data) / len(non_null) > 0.5:  # 超过50%可转为数值
                stats['numeric_columns'].append({
                    'name': col,
                    'count': len(numeric_data),
                    'min': round(numeric_data.min(), 4) if len(numeric_data) > 0 else None,
                    'max': round(numeric_data.max(), 4) if len(numeric_data) > 0 else None,
                    'mean': round(numeric_data.mean(), 4) if len(numeric_data) > 0 else None,
                    'median': round(numeric_data.median(), 4) if len(numeric_data) > 0 else None
                })
            else:
                # 文本列
                value_counts = col_data.value_counts().head(10)
                stats['text_columns'].append({
                    'name': col,
                    'count': len(non_null),
                    'unique_count': col_data.nunique(),
                    'top_values': [
                        {'value': str(k), 'count': int(v)}
                        for k, v in value_counts.items()
                    ]
                })
        except Exception:
            # 文本列
            value_counts = col_data.value_counts().head(10)
            stats['text_columns'].append({
                'name': col,
                'count': len(non_null),
                'unique_count': col_data.nunique(),
                'top_values': [
                    {'value': str(k), 'count': int(v)}
                    for k, v in value_counts.items()
                ]
            })

    return stats


@excel_bp.route('/query', methods=['POST'])
@error_handler
def query_excel():
    """
    查询Excel数据接口

    Request Body:
        {
            "file_path": "/path/to/data.xlsx",
            "query": "age>25,name like 张",  // 可选
            "sheet_name": "Sheet1"           // 可选
        }

    Response:
        {
            "code": 200,
            "message": "success",
            "data": {
                "file_name": "data.xlsx",
                "total_rows": 1000,
                "columns": ["name", "age", ...],
                "data": [...],
                "statistics": {...}
            }
        }
    """
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少file_path参数',
            'data': None
        }), 400

    file_path = data['file_path']
    query = data.get('query')
    sheet_name = data.get('sheet_name')

    logger.info(f"查询Excel: {file_path}, 查询条件: {query}")

    result = query_excel_data(file_path, query, sheet_name)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': result
    })


@excel_bp.route('/info', methods=['POST'])
@error_handler
def get_excel_info():
    """
    获取Excel文件信息

    Request Body:
        {
            "file_path": "/path/to/data.xlsx"
        }
    """
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少file_path参数',
            'data': None
        }), 400

    file_path = validate_file_path(data['file_path'])

    import pandas as pd

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        sheets = ['default']
    else:
        excel_file = pd.ExcelFile(file_path)
        sheets = excel_file.sheet_names

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'sheets': sheets,
            'sheet_count': len(sheets),
            'total_rows': len(df) if 'df' in dir() else None,
            'columns': list(df.columns) if 'df' in dir() else None,
            'last_modified': datetime.fromtimestamp(
                os.path.getmtime(file_path)
            ).strftime('%Y-%m-%d %H:%M:%S')
        }
    })


@excel_bp.route('/aggregate', methods=['POST'])
@error_handler
def aggregate_excel():
    """
    Excel数据聚合分析

    Request Body:
        {
            "file_path": "/path/to/data.xlsx",
            "group_by": "department",
            "aggregations": [
                {"column": "salary", "func": "sum"},
                {"column": "salary", "func": "avg"},
                {"column": "name", "func": "count"}
            ],
            "sheet_name": "Sheet1"
        }
    """
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少file_path参数',
            'data': None
        }), 400

    file_path = validate_file_path(data['file_path'])
    group_by = data.get('group_by')
    aggregations = data.get('aggregations', [])
    sheet_name = data.get('sheet_name')

    if not group_by:
        return jsonify({
            'code': 400,
            'message': '缺少group_by参数',
            'data': None
        }), 400

    if not aggregations:
        return jsonify({
            'code': 400,
            'message': '缺少aggregations参数',
            'data': None
        }), 400

    import pandas as pd

    # 读取数据
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

    if group_by not in df.columns:
        return jsonify({
            'code': 400,
            'message': f'列不存在: {group_by}',
            'data': None
        }), 400

    # 执行聚合
    agg_dict = {}
    for agg in aggregations:
        col = agg.get('column')
        func = agg.get('func', 'sum')
        if col in df.columns:
            agg_dict[col] = func

    if not agg_dict:
        return jsonify({
            'code': 400,
            'message': '没有有效的聚合列',
            'data': None
        }), 400

    grouped = df.groupby(group_by).agg(agg_dict)

    # 转换为记录格式
    records = []
    for idx, row in grouped.iterrows():
        record = {group_by: str(idx)}
        for col, val in row.items():
            if pd.isna(val):
                record[f"{col}_{func}"] = None
            else:
                record[f"{col}_{func}"] = round(val, 4) if isinstance(val, float) else val
        records.append(record)

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'group_by': group_by,
            'aggregations': aggregations,
            'result': records
        }
    })


@excel_bp.route('/search', methods=['POST'])
@error_handler
def search_excel():
    """
    在Excel中搜索数据

    Request Body:
        {
            "file_path": "/path/to/data.xlsx",
            "keyword": "张三",
            "sheet_name": "Sheet1"
        }
    """
    data = request.get_json()
    if not data or 'file_path' not in data or 'keyword' not in data:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数',
            'data': None
        }), 400

    file_path = data['file_path']
    keyword = data['keyword']
    sheet_name = data.get('sheet_name')

    # 查询数据
    result = query_excel_data(file_path, None, sheet_name)

    # 在结果中搜索
    matches = []
    for i, record in enumerate(result.get('data', [])):
        for col, val in record.items():
            if val and keyword.lower() in str(val).lower():
                matches.append({
                    'row_index': i,
                    'column': col,
                    'value': str(val),
                    'record': record
                })
                break

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'keyword': keyword,
            'total_matches': len(matches),
            'matches': matches[:100]  # 限制返回数量
        }
    })


# Function Calling 函数定义
FUNCTION_DEFINITIONS = {
    'name': 'query_excel',
    'description': '读取Excel文件并执行数据查询、搜索和统计分析',
    'parameters': {
        'type': 'object',
        'properties': {
            'file_path': {
                'type': 'string',
                'description': 'Excel文件的完整路径',
                'example': '/path/to/data.xlsx'
            },
            'query': {
                'type': 'string',
                'description': '查询条件，支持格式: column=value, column>value, column<value, column!=value, column like %value%',
                'example': 'age>25,department=技术部'
            },
            'sheet_name': {
                'type': 'string',
                'description': '工作表名称，不传则默认读取第一个工作表',
                'example': 'Sheet1'
            }
        },
        'required': ['file_path']
    }
}
