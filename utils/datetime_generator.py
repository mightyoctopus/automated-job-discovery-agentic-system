from datetime import datetime, timezone


def generate_current_datetime():
    time_now = datetime.now(timezone.utc).date().isoformat()
    return time_now