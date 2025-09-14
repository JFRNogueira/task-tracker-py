from datetime import datetime, timezone

def now_iso() -> str:
    """Return current time in UTC as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()
