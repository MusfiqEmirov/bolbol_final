class TimeIntervals:
    """Class containing time intervals in seconds."""
    ONE_MIN_IN_SEC = 60                         # 1 minute in seconds
    ONE_HOUR_IN_SEC = ONE_MIN_IN_SEC * 60       # 1 hour in seconds
    ONE_DAY_IN_SEC = ONE_HOUR_IN_SEC * 24       # 1 day in seconds
    ONE_WEEK_IN_SEC = ONE_DAY_IN_SEC * 7        # 1 week in seconds
    ONE_MONTH_IN_SEC = ONE_DAY_IN_SEC * 30      # 1 month (30 days) in seconds
    ONE_YEAR_IN_SEC = ONE_MONTH_IN_SEC * 12     # 1 year (12 months) in seconds
    ONE_MONTH_IN_DAYS = 30                      # 1 month in days

    WEEKDAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    WEEKDAY_NAMES = [day[0] for day in WEEKDAYS]