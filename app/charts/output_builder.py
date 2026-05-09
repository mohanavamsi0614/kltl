from typing import Dict, Any, List

class OutputBuilder:
    def build(self, kind: str, x: str, categories: List[Any], series: List[Dict[str, Any]], row_count: int, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "kind": kind,
            "x": x,
            "categories": categories,
            "series": series,
            "row_count": row_count,
            "meta": meta
        }
