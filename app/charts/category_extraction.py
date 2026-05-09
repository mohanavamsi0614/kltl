from typing import Dict, Any, List

class ColumnMapper:
    def resolve_indices(self, columns: List[str], targets: List[str]) -> List[int]:
        return [columns.index(t) for t in targets]

class CategoryExtractor:
    def extract(self, rows: List[Dict[str, Any]], dimension: str) -> List[Any]:
        """
        Extracts categories from the first dimension.
        """
        return [row.get(dimension) for row in rows]
        