from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

VANCOUVER_TZ = ZoneInfo("America/Vancouver")


def get_vancouver_date_context():
    now = datetime.now(VANCOUVER_TZ)
    return {
        "today": now.strftime("%Y-%m-%d"),
        "week_ago": (now - timedelta(days=7)).strftime("%Y-%m-%d"),
        "year": now.year,
        "month": now.month,
    }
