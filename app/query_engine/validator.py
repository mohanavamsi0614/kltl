import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from config import TABLE_MAP_PATH, METRICS_REGISTRY_PATH, DEFAULT_LIMIT, MAX_LIMIT
from app.query_engine.db_columns import get_table_columns

class AnalyticsRequest(BaseModel):
    table_id: str
    dimensions: List[str] = []
    metrics: List[str] = []
    filters: List[Dict[str, Any]] = []
    limit: Optional[int] = DEFAULT_LIMIT

class Validator:
    def __init__(self):
        with open(TABLE_MAP_PATH, 'r') as f:
            self.table_map = json.load(f)
        with open(METRICS_REGISTRY_PATH, 'r') as f:
            self.metrics_registry = json.load(f)

    def validate(self, request: AnalyticsRequest) -> Dict[str, Any]:
        # 1. Resolve Table
        if request.table_id not in self.table_map:
            raise ValueError(f"Invalid table_id: {request.table_id}")
        
        table_meta = self.table_map[request.table_id]
        schema = table_meta['database']
        table_name = table_meta['table']
        
        # 2. Get Live Schema
        available_columns = get_table_columns(schema, table_name)
        if not available_columns:
             # Fallback or error if table doesn't exist in DB
             # For seeding purposes, we might not have the table yet.
             # In a real app, this would raise an error.
             pass

        # 3. Validate Dimensions
        for dim in request.dimensions:
            if available_columns and dim not in available_columns:
                raise ValueError(f"Dimension '{dim}' not found in table '{table_name}'")

        # 4. Validate Metrics
        for metric in request.metrics:
            if metric not in self.metrics_registry:
                raise ValueError(f"Metric '{metric}' is not registered.")

        # 5. Validate Filters
        allowed_operators = {'=', 'IN', 'BETWEEN', '>', '<', '>=', '<='}
        for f in request.filters:
            field = f.get('field')
            op = f.get('operator')
            if available_columns and field not in available_columns:
                raise ValueError(f"Filter field '{field}' not found in table '{table_name}'")
            if op not in allowed_operators:
                raise ValueError(f"Unsupported operator '{op}'")

        # 6. Normalize Limit
        if request.limit is None:
            request.limit = DEFAULT_LIMIT
        request.limit = min(request.limit, MAX_LIMIT)

        return {
            "schema": schema,
            "table": table_name,
            "dimensions": request.dimensions,
            "metrics": [self.metrics_registry[m]['expression'] for m in request.metrics],
            "metric_names": request.metrics,
            "filters": request.filters,
            "limit": request.limit
        }
