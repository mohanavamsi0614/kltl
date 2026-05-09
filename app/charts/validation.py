from typing import Dict, Any, List

class ChartValidator:
    def validate(self, extracted_data: Dict[str, Any]):
        payload = extracted_data['payload']
        instructions = extracted_data['instructions']

        # 1. Column Validation
        available_columns = set(payload.columns)
        for dim in instructions.dimensions:
            if dim not in available_columns:
                raise ValueError(f"Chart dimension '{dim}' not found in analytics results.")
        
        for metric in instructions.metrics:
            if metric not in available_columns:
                raise ValueError(f"Chart metric '{metric}' not found in analytics results.")

        # 2. Row Width Validation
        for row in payload.rows:
            if len(row) != len(payload.columns):
                # Since we use RealDictCursor, row is a dict. 
                # We should check if keys match columns.
                if set(row.keys()) != available_columns:
                     raise ValueError("Row keys do not match payload columns.")

        # 3. Chart Kind Validation
        allowed_kinds = {"bar", "line", "auto"}
        if instructions.chart_kind not in allowed_kinds:
            raise ValueError(f"Unsupported chart kind: {instructions.chart_kind}")
        
        return True