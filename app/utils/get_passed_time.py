from datetime import datetime, timedelta

from app.constants import months


class TimeFormat:
    time_passed = True
    time_format = 'LLL'

    def __init__(self, time_passed, time_format):
        self.time_passed = time_passed
        self.time_format = time_format


def get_time_passed(time_passed):
    time_past = datetime.now() - time_passed

    if time_past < timedelta(minutes=1):
        return f'{time_past.seconds}s'

    elif time_past < timedelta(hours=1):
        return f'{time_past.seconds // 60}m'

    elif time_past < timedelta(days=1):
        return f'{time_past.seconds // 3600}h'

    elif time_past < timedelta(days=365):
        return f' {months.get(time_passed.month, "undefined")} {time_passed.day}'
    else:
        return f' {time_passed.year} {months.get(time_passed.month, "undefined")} {time_passed.day}'


def get_time_format(time_passed):
    time_past = datetime.now() - time_passed

    if time_past < timedelta(minutes=1):
        return TimeFormat(time_passed=True, time_format='ss')

    elif time_past < timedelta(hours=1):
        return TimeFormat(time_passed=True, time_format='mm')
        return f'{time_past.seconds // 60}m'

    elif time_past < timedelta(days=1):
        return TimeFormat(time_passed=True, time_format='hh')

    elif time_past < timedelta(days=365):
        return TimeFormat(time_passed=False, time_format='MMM D')
    else:
        return TimeFormat(time_passed=False, time_format='YYYY MMM D')

