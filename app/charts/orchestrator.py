from typing import Dict, Any
from app.charts.input_extraction import InputExtractor
from app.charts.validation import ChartValidator
from app.charts.category_extraction import CategoryExtractor
from app.charts.series_construction import SeriesConstructor
from app.charts.chart_kind_resolution import ChartKindResolver
from app.charts.output_builder import OutputBuilder

class ChartOrchestrator:
    def __init__(self):
        self.extractor = InputExtractor()
        self.validator = ChartValidator()
        self.category_extractor = CategoryExtractor()
        self.series_constructor = SeriesConstructor()
        self.kind_resolver = ChartKindResolver()
        self.output_builder = OutputBuilder()

    def generate_chart_payload(self, analytics_payload: Dict[str, Any], chart_instructions: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Extraction
        data = self.extractor.extract(analytics_payload, chart_instructions)
        payload = data['payload']
        instructions = data['instructions']

        # 2. Validation
        self.validator.validate(data)

        # 3. Resolution & Transformation
        kind = self.kind_resolver.resolve(instructions.chart_kind)
        
        # Use first dimension for x-axis categories
        primary_dim = instructions.dimensions[0]
        categories = self.category_extractor.extract(payload.rows, primary_dim)
        
        # Construct series for each metric
        series = self.series_constructor.construct(payload.rows, instructions.metrics)

        # 4. Output Assembly
        return self.output_builder.build(
            kind=kind,
            x=primary_dim,
            categories=categories,
            series=series,
            row_count=len(payload.rows),
            meta=payload.meta
        )
