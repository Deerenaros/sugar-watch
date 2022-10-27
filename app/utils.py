def get_date(form):
    from datetime import datetime
    return datetime(year=int(form.get("year")),
                    month=int(form.get("month")),
                    day=int(form.get("day")),
                    hour=int(form.get("hours")),
                    minute=int(form.get("minutes")))