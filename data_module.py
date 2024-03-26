import traceback

import pg_module
import settings
import util_module as util


def get_data(user_id=None, week=None):
    time_sheets_data = get_all_entries(user_id=user_id, week=week)
    return time_sheets_data


def get_entry(tsh_id=None):
    # util.log_debug(f'{prj_id}, {tsh_id}')

    tsh_dict = get_timesheet_dict(tsh_id=tsh_id)
    # util.log_debug(f'tsh_dict: {tsh_dict}')
    return tsh_dict


def update_entry(tsh_id=None, data=None):
    # util.log_debug(f'update_entry({project_id}, {tsh_id}, {data})')

    entries = pg_module.Entries()
    entries.update_entry(tsh_id=tsh_id, data=data)


def update_status(e_list, verdict):
    entries = pg_module.Entries()
    entries.update_for_approval_status(e_list, verdict)


def insert_entry(user_id=None, prj_id=None, data=None):
    entries = pg_module.Entries()
    entries.add_entry(user_id=user_id, prj_id=prj_id, data=data)


def delete_entry(tsh_id=None):
    entries = pg_module.Entries()
    entries.delete_entry(tsh_id=tsh_id)


def get_timesheet_dict(tsh_id):
    util.log_debug(f'get_timesheet_dict: tsh_id={tsh_id}')

    entry = pg_module.Entries()
    tsh_entry = entry.get_entry_by_id(tsh_id)
    comment = getattr(tsh_entry[0], settings.F_TSH_COMMENT)
    if comment is None:
        comment = ''

    if tsh_entry is None or len(tsh_entry) == 0:
        util.log_error(f'get_timesheet_dict: Запись id={tsh_id} не найдена в базе данных')
        return None

    return {
            settings.F_TSH_ID: tsh_id,
            settings.F_TSH_HOURS: getattr(tsh_entry[0], settings.F_TSH_HOURS),
            settings.F_TSH_NOTE: getattr(tsh_entry[0], settings.F_TSH_NOTE),
            settings.F_TSH_STATUS: getattr(tsh_entry[0], settings.F_TSH_STATUS),
            settings.F_TSH_DATE: getattr(tsh_entry[0], settings.F_TSH_DATE),
            settings.F_TSH_COMMENT: comment
            }

def get_all_entries(user_id=None, week=None):
    try:
        range_dates = util.get_dates_by_week(week=week)

        # Выполняем поиск тймшитов в БД
        #
        entries = pg_module.Entries()
        if entries is None:
            raise Exception('entries is None')

        entries_data = entries.get_entries(s_date=range_dates[0], e_date=range_dates[1], user_id=user_id)

        if entries_data is None:
            util.log_error(f'Data Base is not available')
            exit(0)

        if len(entries_data) == 0:
            util.log_debug(f'Where are no entries for user_id: "{user_id}", dates between "{range_dates[0]}" and "{range_dates[1]}"')
            return None

        # util.log_debug(f'select: {entries_data}')

        # Возвращаем словарь
        #
        return get_all_timesheet_dict(week=week, entries=entries_data)

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'Exception: {ex}')

def get_entries_for_approval(user_id=None):
    try:
        # Выполняем поиск тймшитов в БД
        #
        entries = pg_module.Entries()
        if entries is None:
            raise Exception('entries is None')

        entries_data = entries.get_for_approval_entries(user_id)

        if entries_data is None:
            util.log_error(f'Data Base is not available')
            exit(0)

        if len(entries_data) == 0:
            util.log_debug(f'Нет записей для утверждения пользоватялем user_id={user_id}')
            return None

        # util.log_debug(f'select: {entries_data}')

        # Формируем словарь
        #
        data = {}
        for e in entries_data:
            tsh_id = str(getattr(e, settings.F_TSH_ID))
            data[tsh_id] = {
                settings.F_USR_NAME: str(getattr(e, settings.F_USR_NAME)),
                settings.F_TSH_DATE: str(getattr(e, settings.F_TSH_DATE)),
                settings.F_PRJ_NAME: str(getattr(e, settings.F_PRJ_NAME)),
                settings.F_TSH_HOURS: str(getattr(e, settings.F_TSH_HOURS)),
                settings.F_TSH_NOTE: str(getattr(e, settings.F_TSH_NOTE))
            }

        util.log_debug(f'get_entries_for_approval: data={data}')

        # return get_all_timesheet_dict(week=week, entries=entries_data)

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'Exception: {ex}')



# Формирует словарь из курсора entries (для таблицы)
#
def get_all_timesheet_dict(week=None, entries=None):
    dates = util.list_dates_in_week(week=week)

    # Сформировать словарь дат
    #
    dates_dict = {}
    for d in dates:
        dates_dict[d] = {settings.EMPTY_ID_KEY: {}}

    # сформировать список проектов
    #
    time_sheets_dict = {}
    for e in entries:
        prj_id = str(getattr(e, settings.F_TSH_PRJ_ID))
        prj_name = str(getattr(e, settings.F_PRJ_NAME))

        prj_dict = {settings.F_PRJ_NAME: prj_name, settings.FLD_TSH_DICT: dates_dict.copy()}
        time_sheets_dict[prj_id] = prj_dict

    # Заполнить словари 'data': {...} для каждого проекта
    #
    for e in entries:
        tsh_id = str(getattr(e, settings.F_TSH_ID))
        prj_id = str(getattr(e, settings.F_TSH_PRJ_ID))
        status = getattr(e, settings.F_TSH_STATUS)
        note = getattr(e, settings.F_TSH_NOTE)
        if note is None: note = '-'
        hours = getattr(e, settings.F_TSH_HOURS)
        date = getattr(e, settings.F_TSH_DATE)
        comment = getattr(e, settings.F_TSH_COMMENT)
        if comment is None: comment = '-'

        tsh_dict = {tsh_id:
                        {
                            settings.F_TSH_HOURS: hours,
                            settings.F_TSH_NOTE: note,
                            settings.F_TSH_STATUS: status,
                            settings.F_TSH_COMMENT: comment
                        }
        }

        p_dict = time_sheets_dict[prj_id]
        p_dict = p_dict[settings.FLD_TSH_DICT]
        p_dict[str(date)] = tsh_dict

    # util.log_debug(f'time_sheets_dict fin: {time_sheets_dict}')
    return time_sheets_dict

def get_all_projects_dict():
    projects = pg_module.Projects()
    all_projects = projects.get_all_projects()
    if all_projects is None:
        util.log_error(f'get_all_projects: не удалось сформировать список проектов из Базы Данных')
        return None

    projects = {}
    for prj in all_projects:
        prj_id = str(getattr(prj, settings.F_PRJ_ID))
        manager_id = str(getattr(prj, settings.F_PRJ_MANAGER_ID))
        prj_name = str(getattr(prj, settings.F_PRJ_NAME))
        start_date = str(getattr(prj, settings.F_PRJ_START_DATE))
        end_date = str(getattr(prj, settings.F_PRJ_END_DATE))
        p_dict = {
            settings.F_PRJ_MANAGER_ID: manager_id,
            settings.F_PRJ_NAME: prj_name,
            settings.F_PRJ_START_DATE: start_date,
            settings.F_PRJ_END_DATE: end_date
        }
        projects[prj_id] = p_dict

    return projects

