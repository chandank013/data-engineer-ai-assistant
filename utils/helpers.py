# utils/helpers.py

def format_size(bytes: int) -> str:
    if bytes < 1024: return f"{bytes} B"
    if bytes < 1024**2: return f"{bytes/1024:.1f} KB"
    return f"{bytes/1024**2:.1f} MB"

def safe_json(obj):
    import math
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj