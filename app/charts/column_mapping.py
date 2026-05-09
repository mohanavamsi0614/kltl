from typing import List

class ColumnMapper:
    def resolve_indices(self, columns: List[str], targets: List[str]) -> List[int]:
        return [columns.index(t) for t in targets]
