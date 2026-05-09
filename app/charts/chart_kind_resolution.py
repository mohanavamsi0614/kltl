class ChartKindResolver:
    def resolve(self, requested_kind: str) -> str:
        if requested_kind == "auto":
            return "bar"
        return requested_kind
