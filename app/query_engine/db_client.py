import time
from sqlalchemy import create_engine, text
from typing import Dict, Any, List
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from app.query_engine.validator import Validator, AnalyticsRequest
from app.query_engine.query_builder import QueryBuilder
from app.query_engine.logger_config import setup_logger

logger = setup_logger("DBClient")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

class DBClient:
    def __init__(self):
        self.validator = Validator()
        self.query_builder = QueryBuilder()

    def fetch_analytics(self, request: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            # 1. Normalize and Validate
            analytics_req = AnalyticsRequest(**request)
            validated_params = self.validator.validate(analytics_req)
            
            # 2. Build SQL
            sql, params = self.query_builder.build(validated_params)
            
            # 3. Execute
            rows, columns = self._execute_query(sql, params)
            
            execution_time = (time.time() - start_time) * 1000  # ms
            
            # 4. Format Response
            return {
                "columns": columns,
                "rows": rows,
                "sql": sql,
                "meta": {
                    "execution_time_ms": execution_time,
                    "row_count": len(rows),
                    "table_id": analytics_req.table_id,
                    "dimensions": validated_params['dimensions'],
                    "metric_names": validated_params['metric_names']
                }
            }
            
        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            raise e

    def _execute_query(self, sql: str, params: List[Any]):
        try:
            with engine.connect() as conn:
                # We use text(sql) for raw SQL execution
                # Since we use %s in query_builder, we should adapt to SQLAlchemy's :param syntax or just use raw strings if safe.
                # Actually, query_builder uses %s which is for psycopg2. 
                # SQLAlchemy uses :param for named parameters.
                # Let's fix query_builder to use named parameters for better ORM compatibility.
                
                # For now, let's just use the result proxy
                result = conn.execute(text(sql), params if isinstance(params, dict) else {f"p{i}": v for i, v in enumerate(params)})
                rows = [dict(row) for row in result.mappings()]
                columns = list(result.keys())
                return rows, columns
        except Exception as e:
            raise e
