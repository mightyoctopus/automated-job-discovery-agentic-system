from datetime import datetime, timezone, timedelta


def generate_current_datetime():
    time_now = datetime.now(timezone.utc).date().isoformat()
    return time_now


def generate_search_offset_time():
    """
    Generate datetime used for the offset time of search range
    """
    current_time = datetime.now(timezone.utc)
    five_weeks_ago = current_time - timedelta(weeks=5)

    return five_weeks_ago.isoformat()