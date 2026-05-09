from typing import Dict, Any, List

class QueryBuilder:
    def build(self, validated_params: Dict[str, Any]) -> str:
        schema = validated_params['schema']
        table = validated_params['table']
        dimensions = validated_params['dimensions']
        metrics = validated_params['metrics']
        metric_names = validated_params['metric_names']
        filters = validated_params['filters']
        limit = validated_params['limit']

        select_parts = dimensions + [f"{expr} AS {name}" for expr, name in zip(metrics, metric_names)]
        select_clause = f"SELECT {', '.join(select_parts)}"

        from_clause = f"FROM {schema}.{table}"

        where_clause = ""
        params = {}
        if filters:
            filter_strings = []
            for i, f in enumerate(filters):
                field = f['field']
                op = f['operator']
                val = f['value']
                param_name = f"val_{i}"
                
                if op == 'IN':
                    placeholders = [f":val_{i}_{j}" for j in range(len(val))]
                    filter_strings.append(f"{field} IN ({', '.join(placeholders)})")
                    for j, v in enumerate(val):
                        params[f"val_{i}_{j}"] = v
                elif op == 'BETWEEN':
                    filter_strings.append(f"{field} BETWEEN :val_{i}_start AND :val_{i}_end")
                    params[f"val_{i}_start"] = val[0]
                    params[f"val_{i}_end"] = val[1]
                else:
                    filter_strings.append(f"{field} {op} :{param_name}")
                    params[param_name] = val
            
            where_clause = f"WHERE {' AND '.join(filter_strings)}"

        # Construct GROUP BY clause
        group_by_clause = ""
        if dimensions:
            group_by_clause = f"GROUP BY {', '.join(dimensions)}"

        # Construct LIMIT clause
        limit_clause = f"LIMIT {limit}"

        # Combine
        sql = f"{select_clause}\n{from_clause}\n{where_clause}\n{group_by_clause}\n{limit_clause}".strip()
        
        if not sql.upper().startswith("SELECT"):
            raise ValueError("Safety check failed: Query does not start with SELECT")

        return sql, params
