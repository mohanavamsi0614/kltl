from typing import Dict, Any, List
from pydantic import BaseModel

class ChartInstructions(BaseModel):
    table_id: str
    dimensions: List[str]
    metrics: List[str]
    chart_kind: str = "auto"

class AnalyticsPayload(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    meta: Dict[str, Any] = {}

class InputExtractor:
    def extract(self, analytics_payload: Dict[str, Any], chart_instructions: Dict[str, Any]):
        return {
            "payload": AnalyticsPayload(**analytics_payload),
            "instructions": ChartInstructions(**chart_instructions)
        }
