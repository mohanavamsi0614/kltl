from typing import Dict, Any, List

class SeriesConstructor:
    def construct(self, rows: List[Dict[str, Any]], metrics: List[str]) -> List[Dict[str, Any]]:
        series = []
        for metric in metrics:
            data = [row.get(metric) for row in rows]
            series.append({
                "name": metric,
                "data": data
            })
        return series
