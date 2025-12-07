from datetime import datetime, timedelta, timezone


def utc_ms(ds: datetime) -> int:
    """
    datetime перевод в миллисекунды
    """
    return int(ds.timestamp() * 1000)


def get_today_utc_close():
    """
    возвращает start и close мс в utc для сегодняшнего дня
    """
    now_utc = datetime.now(timezone.utc)
    last_close_minute = (now_utc.replace(second=0, microsecond=0) - timedelta(minutes=1))
    start_minutes_day = (now_utc.replace(second=0, microsecond=0, hour=0, minute=0))
    return utc_ms(start_minutes_day), utc_ms(last_close_minute)

if __name__ == '__main__':
    h2h = get_today_utc_close()
    print(h2h)
