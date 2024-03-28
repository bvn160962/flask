import datetime
import logging
import os
import settings
from app import app_cache


# Логирование
#
logger = None

def log_info(msg):
    print('++'+msg)
    logger.info(msg)


def log_debug(msg):
    print('++'+msg)
    logger.debug(msg)


def log_error(msg):
    print('**'+msg)
    logger.error(msg)


def logger_init():
    # Создать лог папку если ее нет
    #
    if not os.path.isdir(settings.LOG_DIR):
        os.makedirs(settings.LOG_DIR)

    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(level=settings.LOG_FILE_LEVEL)

        file_handler = logging.FileHandler(settings.LOG_FILE_NAME, mode=settings.LOG_FILE_MODE)

        formatter = logging.Formatter(settings.LOG_FILE_FORMAT)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # return logger


# Внутренний кэш по ip-address
#
def clear_cache(host):
    set_cache_property(host, settings.C_WEEK, get_week())
    set_cache_property(host, settings.C_DATE, get_date())
    set_cache_property(host, settings.C_TIMESHEET_ID, '')
    set_cache_property(host, settings.C_PROJECT_ID, '')


def print_cache():
    log_debug(f'set_cache_property: app_cache={app_cache}')

def validate_cache(host):
    if get_current_project_id(host) is None:
        set_cache_property(host=host, prop=settings.C_PROJECT_ID, value='')
    if get_current_timesheet_id(host) is None:
        set_cache_property(host=host, prop=settings.C_TIMESHEET_ID, value='')
    if get_current_date(host) is None:
        set_cache_property(host=host, prop=settings.C_DATE, value='')



def get_cache_property(host=None, prop=None):
    if host is None:
        raise Exception('host is None')

    cache = app_cache.get(host)  # {...}

    if cache is None:
        value = ''
    else:
        value = cache.get(prop)

    log_debug(f'get_cache_property: get for {host}, {prop}="{value}"')
    return value


def set_cache_property(host=None, prop=None, value=None):
    if host is None:
        raise Exception('host is None')

    cache = app_cache.get(host)  # {...}
    try:
        if cache is None:  # new
            log_debug(f'set_cache_property: new {host}, {prop}={value}')
            app_cache[host] = {prop: value}
        else:
            v = cache.get(prop)
            if v is not None:  # change
                if v != value:
                    log_debug(f'set_cache_property: change {prop}: old={v}, new={value}')
                    cache[prop] = value
                else:
                    log_debug(f'set_cache_property: skip {prop}: old={v}, new={value}')

            else:  # set
                log_debug(f'set_cache_property: set {prop}={value}')
                cache[prop] = value

        # print_cache()
        return value

    except Exception as ex:
        log_error(f'Error on set cache property: {ex}')
        return ''


# get user_id from cache
#
def get_current_user_id(host):
    u_id = get_cache_property(host=host, prop=settings.C_USER_ID)

    # if u_id is None or u_id == '':
    #     log_debug(f'show login HTML {host}')
    #     u_id = set_cache_property(host=host, prop=settings.C_USER_ID, value=settings.USER)

    return u_id


# get tsh_id from cache
#
def get_current_timesheet_id(host):
    return get_cache_property(host=host, prop=settings.C_TIMESHEET_ID)


# get project_id from cache
#
def get_current_project_id(host):
    return get_cache_property(host=host, prop=settings.C_PROJECT_ID)


def get_current_date(host):
    return get_cache_property(host=host, prop=settings.C_DATE)


def get_current_week(host):
    return get_cache_property(host=host, prop=settings.C_WEEK)


# Вспомогательные функции
#
def get_week():
    return get_week_by_date(datetime.datetime.now())


def get_date():
    return datetime.datetime.now().date()


def get_week_by_date(date):

    year, i_week, day = date.isocalendar()
    s_week = f'{i_week:0{2}}'  # 1 -> 01, 12 -> 12
    out = str(year) + '-W' + s_week

    # log_debug(f'{year}, {week}, {w}, {out}')
    return out


def date_to_day(date):
    s_date = str(date).split('-')
    return f'{s_date[2]}.{s_date[1]}'


def list_dates_in_week(week=None):
    s_date = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w").date()
    date_str = s_date.isocalendar()

    out = []
    for i in range(1, 8):
        date = datetime.datetime.fromisocalendar(year=date_str[0], week=date_str[1], day=i).date()
        # o_date = date_to_day(date)
        # out.append(o_date)
        out.append(str(date))

    # log_debug(f'out: {out}')
    return out


# Начальная и конечная даты в неделе
#
def get_dates_by_week(week=None):

    s_date = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w").date()
    date_str = s_date.isocalendar()
    e_date = datetime.datetime.fromisocalendar(year=date_str[0], week=date_str[1], day=7).date()

    # log_debug(f'week: {week}: from {s_date} to {e_date}')

    return s_date, e_date


def shift_week(week='', next=True):
    s = week.split('-')
    if next:
        i = int(s[1][1:]) + 1
    else:
        i = int(s[1][1:]) - 1

    year = s[0]
    last_week = datetime.date(int(year), 12, 28).isocalendar().week
    # last_week = last_week.isocalendar().week

    if i == 0:
        i = 1
    if i > last_week:
        i = last_week

    return f'{year}-W{i:0{2}}'
    # return s[0] + '-W' + str(i)



logger_init()
