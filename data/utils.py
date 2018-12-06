import datetime

def transform_date(str_date, date_style):
    if str_date == 'NaN':
        return str_date
    else:
        if date_style == 1:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:00:00.000Z').strftime('%d/%m/%Y %H:00')
        elif date_style == 2:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:00+00:00').strftime('%d/%m/%Y %H:%M')
    return date

def add_hours(str_date, hours):
    date = datetime.datetime.strptime(str_date, "%d/%m/%Y %H:00")
    date += datetime.timedelta(hours=hours)
    return(date.strftime("%d/%m/%Y %H:00"))