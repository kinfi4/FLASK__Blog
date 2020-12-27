from datetime import datetime, timedelta

from app.constants import months


def get_time_passed(time_passed):
    time_past = datetime.now() - time_passed

    if time_past < timedelta(minutes=1):
        return f'{time_past.seconds}s ago'

    elif time_past < timedelta(hours=1):
        return f'{time_past.seconds // 60}m ago'

    elif time_past < timedelta(days=1):
        return f'{time_past.seconds // 3600}h ago'

    elif time_past < timedelta(days=365):
        return f' {months.get(time_passed.month, "undefined")} {time_passed.day}'
    else:
        return f' {time_passed.year} {months.get(time_passed.month, "undefined")} {time_passed.day}'
