import pg_module
import util_module as util
import settings
import ui_module
import data_module


# TIMESHEETS BLOCK
#
def timesheets_table_button(host=None, value=''):
    util.log_debug(f'Нажата кнопка в Таблице: {value}')

    # Разбор значения value (prj_id#tsh_id#date)
    #
    s = value.split(settings.SPLITTER)
    if s is None:
        raise Exception('Ошибка при парсинге values: None')

    if len(s) != 3:
        raise Exception(f'Ошибка при парсинге values: len={len(s)}')

    # Set cache
    #
    util.set_cache_property(host, settings.C_PROJECT_ID, s[0])
    util.set_cache_property(host, settings.C_TIMESHEET_ID, s[1])
    util.set_cache_property(host, settings.C_DATE, s[2])

    return ui_module.create_timesheet_html(host=host)


def timesheets_delete_button(host=None, values=None):

    tsh_id = util.get_current_timesheet_id(host)
    util.log_debug(f'pressed_delete_button: Delete entry: tsh_id={tsh_id}')

    if tsh_id is not None and tsh_id != '':
        data_module.delete_entry(tsh_id=tsh_id)
        util.set_cache_property(host, settings.C_TIMESHEET_ID, '')  # убрать tsh_id из кэша
    else:
        util.log_error('Попытка удалить запись с пустым tsh_id')


def timesheets_week_button(values=None, host=None):
    util.log_debug(f'Нажата кнопка "Week": {values}')

    week = values[ui_module.INPUT_WEEK_NAME]
    util.set_cache_property(host, settings.C_WEEK, week)
    util.log_debug(f'Week: "{week}"')


def current_week_pressed(host):
    util.set_cache_property(host, settings.C_WEEK, util.get_week())
    return ui_module.create_timesheet_html(host=host)


def next_week_pressed(host):
    week = util.get_current_week(host)
    util.set_cache_property(host, settings.C_WEEK, util.shift_week(week, True))
    return ui_module.create_timesheet_html(host=host)


def prev_week_pressed(host):
    week = util.get_current_week(host)
    util.set_cache_property(host, settings.C_WEEK, util.shift_week(week, False))
    return ui_module.create_timesheet_html(host=host)


def timesheets_update_button(host):
    util.log_debug(f'Нажата кнопка Update Timesheets')
    util.clear_cache(host)
    pg_module.DB_CONNECT = None
    return ui_module.create_timesheet_html(host=host)


def timesheets_save_button(host=None, values=None):
    util.log_info(f'Нажата кнопка Save: {values}')

    html = ''
    tsh_id = util.get_current_timesheet_id(host)
    # Прочитать значения из формы (values = request.form)
    #
    prj_id, inp_hours, inp_note, inp_status, current_date, comment = '', '', '', '', '', ''
    for value in values:
        if value == ui_module.SELECT_PROJECT_NAME:
            prj_id = values[value]
        if value == ui_module.INPUT_HOURS_NAME:
            inp_hours = values[value]
        if value == ui_module.INPUT_NOTE_NAME:
            inp_note = values[value]
        if value == ui_module.SELECT_STATUS_NAME:
            inp_status = values[value]
        if value == ui_module.CURRENT_DATE:
            current_date = values[value]
        if value == ui_module.INPUT_COMMENT_NAME:
            comment = values[value]

    if tsh_id == '':
        # Новая запись timeshhets (Insert)
        #
        if prj_id == '' or current_date == '' or inp_hours == '':
            msg = f'Не задано одно из обязательных значений атрибутов (prj_id={prj_id}, date={current_date}, hours={inp_hours}) при попытке создать новую запись!'
            util.log_debug(msg)
            html = ui_module.create_info_html(settings.INFO_TYPE_WARNING, msg, settings.MODULES[settings.M_TIMESHEETS]['url'], host=host)
        else:
            data_module.insert_entry(
                user_id=util.get_current_user_id(host),
                prj_id=prj_id,
                data={
                    settings.F_TSH_DATE: current_date,
                    settings.F_TSH_HOURS: inp_hours,
                    settings.F_TSH_NOTE: inp_note,
                    settings.F_TSH_STATUS: inp_status,
                    settings.F_TSH_COMMENT: comment
                }
            )
    else:
        # Существующая запись timeshhets (Update)
        #
        data_module.update_entry(
            tsh_id=tsh_id,
            data={
                settings.F_TSH_HOURS: inp_hours,
                settings.F_TSH_NOTE: inp_note,
                settings.F_TSH_STATUS: inp_status,
                settings.F_TSH_COMMENT: comment
            }
        )

    return html


# POST
#
def timesheets_post(values, host):
    html = ''
    for value in values:
        # util.log_debug(f'value={value}')
        # Нажата одна из кнопок в таблице
        #
        if value == settings.TABLE_BUTTON:
            html = timesheets_table_button(host=host, value=values[value])

        # Нажата кнопка SAVE Entry
        #
        if value == settings.SAVE_BUTTON:
            html_e = timesheets_save_button(host=host, values=values)
            if html_e != '':
                return html_e
            html = ui_module.create_timesheet_html(host=host)

        # Нажата кнопка DELETE YES
        #
        if value == settings.DELETE_BUTTON_YES:
            timesheets_delete_button(host=host, values=values)
            html = ui_module.create_timesheet_html(host=host)

        # Нажата кнопка DELETE NO
        #
        if value == settings.DELETE_BUTTON_NO:
            html = ui_module.create_timesheet_html(host=host)

        # Нажата кнопка DELETE Entry
        #
        if value == settings.DELETE_BUTTON:
            # Show confirmation dialog
            html = ui_module.create_delete_confirm_html(host=host)

        # Нажата кнопка WEEK
        #
        if value == settings.WEEK_BUTTON:
            timesheets_week_button(host=host, values=values)
            html = ui_module.create_timesheet_html(host=host)

        # Нажата кнопка REFRESH Timesheets
        #
        if value == settings.UPDATE_TIMESHEET_BUTTON:
            html = timesheets_update_button(host)

        # Нажата кнопка NEW Entry
        #
        if value == settings.NEW_BUTTON:
            util.set_cache_property(host, settings.C_TIMESHEET_ID, '')
            html = ui_module.create_timesheet_html(host=host)

        # Нажата кнопка LOGOFF
        #
        if value == settings.LOGOFF_BUTTON:
            data_module.get_entries_for_approval(102)
            # data_module.update_status((157, 167), True)

            html = ui_module.create_info_html(settings.INFO_TYPE_INFORMATION, 'Нажата кнопка Sign off', host=host)

        # Нажата кнопка CURRENT WEEK
        #
        if value == settings.WEEK_BUTTON_CURRENT:
            html = current_week_pressed(host)

        # Нажата кнопка NEXT WEEK
        #
        if value == settings.WEEK_BUTTON_NEXT:
            html = next_week_pressed(host)

        # Нажата кнопка PREV WEEK
        #
        if value == settings.WEEK_BUTTON_PREV:
            html = prev_week_pressed(host)

    # util.log_debug(f'timesheets.POST: Не задан обработчик кнопки {value}')
    return html


# GET
#
def timesheets_get(host):
    return ui_module.create_timesheet_html(host=host)


# PROJECTS BLOCK
#

# USERS BLOCK
#

# APPROVE BLOCK
#
