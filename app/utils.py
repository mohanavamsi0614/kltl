import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder that handles Decimal types by converting them to floats.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
