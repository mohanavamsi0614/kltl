from langchain.tools import tool
from typing import Dict, Any, List, Optional
from app.query_engine.db_client import DBClient
from app.charts.orchestrator import ChartOrchestrator
import json
from app.utils import DecimalEncoder

db_client = DBClient()
chart_orchestrator = ChartOrchestrator()

# Global cache to prevent truncation issues with LLM passing large JSON strings
_LAST_RESULT = None

@tool
def execute_analytics_query(table_id: str, dimensions: List[str], metrics: List[str], filters: Optional[List[Dict[str, Any]]] = None, limit: int = 100) -> str:
    """
    Executes a constrained analytical query on the database.
    - table_id: Logical identifier (e.g., 'sales_performance')
    - dimensions: Columns to group by (e.g., ['region'])
    - metrics: Predefined metrics (e.g., ['total_revenue'])
    - filters: Optional list of objects with 'field', 'operator', 'value'
    Returns a JSON string containing 'columns', 'rows', and 'meta'.
    """
    request = {
        "table_id": table_id,
        "dimensions": dimensions,
        "metrics": metrics,
        "filters": filters or [],
        "limit": limit
    }
    try:
        global _LAST_RESULT
        result = db_client.fetch_analytics(request)
        _LAST_RESULT = result
        return json.dumps(result, cls=DecimalEncoder)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@tool
def generate_chart_payload(analytics_result_json: Optional[str] = None, chart_kind: str = "auto") -> str:
    """
    Transforms raw analytical results into a chart-oriented payload.
    - analytics_result_json: The JSON string output from execute_analytics_query. 
      If omitted, uses the result of the last successful query.
    - chart_kind: 'bar', 'line', or 'auto'.
    Returns a JSON string containing 'kind', 'categories', and 'series'.
    """
    try:
        global _LAST_RESULT
        if (not analytics_result_json or analytics_result_json.strip() == "" or analytics_result_json == "LATEST") and _LAST_RESULT:
            analytics_result = _LAST_RESULT
        else:
            # If we have a string, try to parse it. 
            # If it's truncated, this might still fail, but we've tried.
            try:
                analytics_result = json.loads(analytics_result_json)
            except json.JSONDecodeError as e:
                if _LAST_RESULT:
                    # Fallback to cache if parsing fails (likely due to truncation)
                    analytics_result = _LAST_RESULT
                else:
                    raise e
        
        # Determine instructions from the analytics metadata
        meta = analytics_result.get('meta', {})
        
        chart_instructions = {
            "table_id": meta.get('table_id'),
            "dimensions": meta.get('dimensions', []),
            "metrics": meta.get('metric_names', []),
            "chart_kind": chart_kind
        }
        
        chart_payload = chart_orchestrator.generate_chart_payload(analytics_result, chart_instructions)
        return json.dumps(chart_payload, cls=DecimalEncoder)
    except Exception as e:
        return f"Error generating chart: {str(e)}"
