from flask import render_template
from xml.etree import ElementTree as et

import data_module
import settings
import util_module as util

PROJECT_ID_NAME = 'project_id'
TIMESHEET_ID_NAME = 'tsh_id'

DATE_NAME = 'current_date'
INPUT_WEEK_NAME = 'inp_week'
INPUT_HOURS_NAME = 'inp_hours'
INPUT_NOTE_NAME = 'inp_note'
INPUT_COMMENT_NAME = 'inp_comment'
INPUT_STATUS_NAME = 'inp_status'
SELECT_STATUS_NAME = 'selected_status'
SELECT_PROJECT_NAME = 'selected_project'
CURRENT_DATE = 'current_date'

I_PRJ_NAME = 'inp_prj_name'


class BaseHTML:

    def __init__(self, title, module, host):
        util.log_debug(f'BaseHTML: New(title={title})')
        self.__html = et.Element('html', attrib={'lang': 'ru'})
        # self.c_module = module


        # HEAD
        self.__head = et.SubElement(self.__html, 'head')
        et.SubElement(self.__head, 'link', attrib={"rel": "stylesheet", "type": "text/css", "href": 'static/css/style.css'})
        et.SubElement(self.__head, 'link', attrib={"rel": "stylesheet", "href": 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})

        t_title = et.SubElement(self.__head, 'title')
        t_title.text = title

        # BODY
        self.__body = et.SubElement(self.__html, 'body')

        # FORM
        self.__form = et.SubElement(self.__body, 'form', attrib={'name': 'form', 'method': 'POST'})

        p = et.SubElement(self.__form, 'p class="b2_gray"')
        # MODULE
        m = et.SubElement(p, 'a style="margin:10px;"')

        if host is None or module is None:
            m.text = ''
        else:
            m.text = module['name'] + ': ' + f'user: {str(util.get_cache_property(host, settings.C_USER_ID))}, url={module["url"]}'

        # LOGOFF button
        log_off = et.SubElement(p,
                                'button title="Завершить работу"',
                                attrib={
                                    'type': 'submit',
                                    'name': settings.LOGOFF_BUTTON,
                                    'style': 'margin-right: 7px;',
                                    'class': 'right btn-hxw'
                                })
        i = et.SubElement(log_off, 'i', {'class': 'fa fa-user-circle-o fa-lg'})  # fa-user-o
        i.text = '\n'  # !!!Обязательно!!! Иначе, создает одиночный тэг <i .... />, вместо парного <i> ... </i>

        # REFRESH button
        log_off = et.SubElement(p,
                                'button title="Обновить"',
                                attrib={
                                    'type': 'submit',
                                    'name': settings.UPDATE_TIMESHEET_BUTTON,
                                    'style': 'margin-right: 7px;',
                                    'class': 'right btn-hxw'
                                })
        i = et.SubElement(log_off, 'i', {'class': 'fa fa-refresh fa-lg'})
        i.text = '\n'

    def get_html(self):
        return et.tostring(self.__html).decode()

    def get_body(self):
        return self.__body

    def get_head(self):
        return self.__head

    def get_form(self):
        return self.__form



def _create_html_static():
    html = render_template('test.html')
    return html


def add_timesheets_info_area(host=None, form=None, tsh_entry=None):

    tsh_id = util.get_current_timesheet_id(host)
    week = util.get_current_week(host)

    # parsing attributes
    #
    hours = ''
    note = ''
    status = ''
    date = ''
    comment = ''
    if tsh_entry is not None:
        hours = tsh_entry.get(settings.F_TSH_HOURS)
        note = tsh_entry.get(settings.F_TSH_NOTE)
        status = tsh_entry.get(settings.F_TSH_STATUS)
        date = str(tsh_entry.get(settings.F_TSH_DATE))
        comment = str(tsh_entry.get(settings.F_TSH_COMMENT))


    p = et.SubElement(form, 'p')

    # TABLE
    table = et.SubElement(p, 'table')

    # WEEK ROW
    #
    row = et.SubElement(table, 'tr')
    col = et.SubElement(row, 'td colspan="5" align="center"')  # Объединенная ячейка

    # Кнопка Текущая неделя
    btn = et.SubElement(col, 'button title="Текущая неделя" class="btn-hxw"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_CURRENT})
    i = et.SubElement(btn, 'i class="fa fa-calendar" aria-hidden="true"')
    i.text = '\n'

    # Кнопка Назад
    btn = et.SubElement(col, 'button title="Предыдущая неделя" class="btn-hxw"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_PREV})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-left fa-lg" aria-hidden="true"')
    i.text = '\n'

    # Кнопка Вперед
    btn = et.SubElement(col, 'button title="Следующая неделя" class="btn-hxw"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_NEXT})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-right fa-lg" aria-hidden="true"')
    i.text = '\n'

    # Календарь
    et.SubElement(col, 'input ' + settings.ENTER_DISABLE, attrib={'type': 'week', 'name': INPUT_WEEK_NAME, 'value': week, 'style': 'margin:2px; padding:2px; border: 2px solid black; border-radius: 10px;'})

    # Кнопка Применить
    btn = et.SubElement(col, 'button title="Выбрать неделю" class="btn-hxw"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-down fa-lg" aria-hidden="true"')
    i.text = '\n'

    # HEADERS ROW
    #
    row = et.SubElement(table, 'tr', {'style': 'border: 2px solid green'})
    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL)
    lab.text = 'Дата:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL)
    lab.text = 'Проект:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL)
    lab.text = 'Часы:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL + ' title="Дополнительная информация"')
    lab.text = 'Описание:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL + ' title="Комментарий согласования с руководителем"')
    lab.text = 'Комментарий:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_LABEL)
    lab.text = 'Статус:'

    # FIELDS ROW
    #
    row = et.SubElement(table, 'tr', {'style': 'border: 2px solid green'})
    # ДАТА
    col = et.SubElement(row, 'td')
    et.SubElement(col, 'input ' + settings.ENTER_DISABLE, attrib={'type': 'date', 'name': DATE_NAME, 'value': date})

    # ПРОЕКТЫ
    col = et.SubElement(row, 'td')
    prj_id = util.get_current_project_id(host)
    prj_dict = data_module.get_all_projects_dict()
    p_list = et.SubElement(col, 'select style="max-width:200px;"', attrib={'name': SELECT_PROJECT_NAME})

    if prj_dict is None:
        raise Exception(f'Список проектов не сформирован. Возможно, нет подключения к базе данных!')

    for value in prj_dict:
        p_dict = prj_dict[value]
        # util.log_debug(f'=={value}={p_dict}')
        if value == prj_id:
            opt = et.SubElement(p_list, 'option selected', attrib={'value': value})
        else:
            opt = et.SubElement(p_list, 'option', attrib={'value': value})
        opt.text = p_dict[settings.F_PRJ_NAME]

    # ЧАСЫ
    col = et.SubElement(row, 'td')
    et.SubElement(col, 'input size="3" ' + settings.ENTER_DISABLE, attrib={'type': 'text', 'name': INPUT_HOURS_NAME, 'value': hours})

    # ЗАМЕТКИ
    col = et.SubElement(row, 'td')
    et.SubElement(col, 'input size="20" ' + settings.ENTER_DISABLE, attrib={'type': 'text', 'name': INPUT_NOTE_NAME, 'placeholder': '', 'value': note, 'title': note})

    # КОММЕНТАРИЙ
    col = et.SubElement(row, 'td')
    et.SubElement(col, 'input size="10" ' + settings.ENTER_DISABLE, attrib={'type': 'text', 'name': INPUT_COMMENT_NAME, 'value': comment, 'title': comment})

    # СТАТУСЫ
    col = et.SubElement(row, 'td')
    select_status = et.SubElement(col, 'select style="max-width:150px;"', attrib={'name': SELECT_STATUS_NAME})
    valid_statuses = settings.get_valid_statuses(status)
    for value in valid_statuses:
        if value == status:
            opt = et.SubElement(select_status, 'option selected', attrib={'value': value})
        else:
            opt = et.SubElement(select_status, 'option', attrib={'value': value})
        opt.text = valid_statuses[value]

    # TABLE & BUTTONS ROW
    #
    row_1 = et.SubElement(table, 'tr')
    col_table = et.SubElement(row_1, 'td colspan=5 rowspan=3 align=center', {'style': 'border: 2px solid'})  # Объединенная ячейка для таблицы
    col = et.SubElement(row_1, 'td', {'align': 'center', 'valign': 'top', 'width': '50'})
    # Кнопка СОХРАНИТЬ
    btn_save = et.SubElement(col, 'button', attrib={'type': 'submit', 'name': settings.SAVE_BUTTON, 'value': 'submit'})
    btn_save.text = 'сохранить'

    et.SubElement(table, 'tr')
    # Кнопка УДАЛИТЬ
    if tsh_id == '':
        b_tag_name = 'button disabled'
    else:
        b_tag_name = 'button'
    btn_delete = et.SubElement(col, b_tag_name, attrib={'type': 'submit', 'name': settings.DELETE_BUTTON, 'value': 'delete'})
    btn_delete.text = 'удалить'

    et.SubElement(table, 'tr')
    # Кнопка СОЗДАТЬ
    # btn_new = et.SubElement(col, settings.TAG_BUTTON, attrib={'type': 'submit', 'name': settings.NEW_BUTTON, 'value': 'new'})
    # btn_new.text = 'создать'

    # Кнопка ОБНОВИТЬ (зачитать из БД) - нужно перенести в HEADER
    #
    # btn_refresh = et.SubElement(col_btn, settings.TAG_BUTTON, attrib={'type': 'submit', 'name': settings.UPDATE_TIMESHEET_BUTTON})
    # btn_refresh.text = 'обновить'

    # TABLE AREA
    #
    time_sheets_data = data_module.get_data(user_id=util.get_current_user_id(host=host), week=week)
    add_timesheet_table_area(host=host, form=form, data=time_sheets_data, column=col_table)


def add_timesheet_table_area(host=None, form=None, data=None, column=None):

    curr_tsh_id = util.get_current_timesheet_id(host)
    p = et.SubElement(column, 'p')
    # p = et.SubElement(form, 'p')
    table = et.SubElement(p, 'table')

    # HEAD ROW (project + dates)
    #
    dates_node = et.SubElement(table, 'tr')
    dates_col_node = et.SubElement(dates_node, settings.TAG_TD_BTN_HEADER_CENTER)
    lab_project = et.SubElement(dates_col_node, settings.TAG_TD_A_HEADER_P)
    lab_project.text = 'Проекты'

    days = util.list_dates_in_week(week=util.get_current_week(host))
    for day in days:
        dates_cell_node = et.SubElement(dates_node, settings.TAG_TD_BTN_HEADER_CENTER)
        btn_day = et.SubElement(dates_cell_node, settings.TAG_TD_A_HEADER, attrib={'type': 'submit', 'name': 'btn_' + day, 'value': day})
        btn_day.text = util.date_to_day(day)

    # TABLE ROWS (project + hours)
    #
    if data is not None:
        row = 0
        for prj_id in data:
            # projects
            #
            row += 1
            days = data[prj_id][settings.FLD_TSH_DICT]
            col = 0
            row_node = et.SubElement(table, 'tr')
            project_ceil = et.SubElement(row_node, 'td')
            lab_project = et.SubElement(project_ceil, 'a')
            lab_project.text = data[prj_id][settings.F_PRJ_NAME]
            for day in days:
                col += 1
                time_sheets = days[day]
                # util.log_debug(f'time_sheets: {day}={time_sheets}')
                for tsh_id in time_sheets:
                    btn_tag = settings.TAG_BUTTON_TABLE
                    tag_td = settings.TAG_TD_CENTER
                    if tsh_id == settings.EMPTY_ID_KEY:
                        # new timesheet button
                        btn_value = prj_id + settings.SPLITTER + settings.SPLITTER + day
                        hours = '0'
                    else:
                        # existing timesheet button
                        btn_value = prj_id + settings.SPLITTER + tsh_id + settings.SPLITTER
                        hours = time_sheets[tsh_id][settings.F_TSH_HOURS]
                        note = time_sheets[tsh_id][settings.F_TSH_NOTE]

                        # Раскрасить по статусам
                        status = time_sheets[tsh_id][settings.F_TSH_STATUS]
                        if status == settings.EDIT_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_EDIT + f' title="Описание: {note}"'

                        if status == settings.IN_APPROVE_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_IN_APPROVE + f' title="Описание: {note}"'

                        if status == settings.APPROVED_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_APPROVED + f' title="Описание: {note}"'

                        if status == settings.REJECTED_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_REJECTED + f' title="Описание: {note}"'

                        # Выбранная ячейка
                        if curr_tsh_id == tsh_id:
                            tag_td = settings.TAG_TD_CENTER_BORDER
                            # btn_tag = settings.TAG_BUTTON_TABLE_SELECTED


                    day_node = et.SubElement(row_node, tag_td)
                    btn_node = et.SubElement(day_node, btn_tag, attrib={'type': 'submit', 'name': settings.TABLE_BUTTON, 'value': btn_value})
                    btn_node.text = hours

    else:  # Показать доступные проекты с пустыми кнопками
        prj_dict = data_module.get_all_projects_dict()
        for prj_id in prj_dict:
            prj_data = prj_dict[prj_id]
            prj_name = prj_data[settings.F_PRJ_NAME]

            row_node = et.SubElement(table, 'tr')
            project_ceil = et.SubElement(row_node, 'td')
            lab_project = et.SubElement(project_ceil, 'label')
            lab_project.text = prj_name
            util.log_debug(f'add_timesheet_table_area: {prj_id}={prj_name}')
            for day in days:
                day_node = et.SubElement(row_node, 'td')
                btn_value = prj_id + settings.SPLITTER + settings.SPLITTER + day
                btn_node = et.SubElement(day_node, settings.TAG_BUTTON_TABLE, attrib={'type': 'submit', 'name': settings.TABLE_BUTTON, 'value': btn_value})
                btn_node.text = '0'


def create_info_html(i_type='', msg='', url='', host=None):
    if msg == '':
        msg = 'Информация'

    if i_type == '':
        i_type = settings.INFO_TYPE_INFORMATION

    base_html = BaseHTML(i_type, settings.MODULES[settings.M_TIMESHEETS], host)
    p = base_html.get_form()

    # RETURN
    if url != '':
        ret_url = et.SubElement(p, 'a', attrib={'href': url, 'type': 'submit'})
        ret_url.text = 'Возврат...'

    # MESSAGE
    h = et.SubElement(p, 'H3')
    h.text = i_type + ':'

    div = et.SubElement(p, 'div')
    div.text = msg

    return base_html.get_html()


def create_delete_confirm_html(host=None):

    tsh_id = util.get_current_timesheet_id(host)

    entry = data_module.get_timesheet_dict(tsh_id)

    # FORM
    #
    base_html = BaseHTML('Подтверждение', settings.MODULES[settings.M_TIMESHEETS], host)
    form = base_html.get_form()

    # INFO AREA
    #
    p_msg = et.SubElement(form, 'p')

    msg = 'Вы действительно хотите удалить запись?\n'
    msg += f'   - Дата: {entry[settings.F_TSH_DATE]}\n'
    msg += f'   - Часы: {entry[settings.F_TSH_HOURS]}\n'
    msg += f'   - Статус: {entry[settings.F_TSH_STATUS]}\n'
    msg += f'   - Замечание: {entry[settings.F_TSH_NOTE]}\n'
    msg += f'   - Комментарий: {entry[settings.F_TSH_COMMENT]}\n'

    text = et.SubElement(p_msg, 'textarea cols="40" rows="7" readonly')  # style="background-color:LightGray"
    text.text = msg

    # CONFIRM AREA
    #
    p_confirm = et.SubElement(form, 'p')

    btn_yes = et.SubElement(p_confirm, 'button', attrib={'type': 'submit', 'name': settings.DELETE_BUTTON_YES, 'style': 'margin-left:100px; width: 60px;'})  #   style="margin-left:150px;"
    btn_yes.text = 'Да'

    btn_no = et.SubElement(p_confirm, 'button', attrib={'type': 'submit', 'name': settings.DELETE_BUTTON_NO, 'style': 'width: 60px;'})
    btn_no.text = 'Нет'

    return base_html.get_html()


def create_timesheet_html(host=None):
    # util.log_debug(f'create_timesheet_html week: {week}, user_id: {user_id}')
    week = util.get_current_week(host)

    # Распечатать кэш
    util.print_cache()

    tsh_id = util.get_current_timesheet_id(host)
    tsh_date = util.get_current_date(host)

    if tsh_id == '':  # пустая кнопка на дату
        tsh_entry = {
                settings.F_TSH_HOURS: '',
                settings.F_TSH_NOTE: '',
                settings.F_TSH_COMMENT: '',
                settings.F_TSH_STATUS: settings.EDIT_STATUS,
                settings.F_TSH_DATE: tsh_date
            }

    else:  # кнопка на дату с данными
        tsh_entry = data_module.get_entry(tsh_id=tsh_id)
        if tsh_entry is None:
            msg = f'create_timesheet_html: Запись tsh_id="{tsh_id}" не найдена в базе данных'
            html_i = create_info_html(settings.INFO_TYPE_ERROR, msg, settings.MODULES[settings.M_TIMESHEETS]['url'])
            return html_i


    # HTML
    #
    base_html = BaseHTML('TimeSheets', settings.MODULES[settings.M_TIMESHEETS], host)
    form = base_html.get_form()

    # INFO AREA
    #
    # util.log_debug(f'tsh_entry: {tsh_entry}')
    if tsh_id != '' and tsh_entry is None:  # Зачитать и отобразить INFO запись если tsh_id есть в кэше
        tsh_entry = data_module.get_entry(tsh_id=tsh_id)

    add_timesheets_info_area(host=host, form=form, tsh_entry=tsh_entry)

    # util.log_debug(f'str_html: {base_html.get_html()}')

    return base_html.get_html()


def t_html():
    html = et.Element('html', attrib={'lang': 'ru'})
    head = et.SubElement(html, 'head')
    et.SubElement(head, 'link', attrib={"rel": "stylesheet", "type": "text/css", "href": 'static/css/style.css'})
    et.SubElement(head, 'link', attrib={"rel": "stylesheet",
                                               "href": 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})

    t_title = et.SubElement(head, 'title')
    t_title.text = 'x'

    body = et.SubElement(html, 'body')
    form = et.SubElement(body, 'form', attrib={'name': 'form', 'method': 'POST'})
    p = et.SubElement(form, 'p class="b2_gray"')
    b = et.SubElement(p, 'textarea placeholder="123"')
    b.text = '\n'
    b = et.SubElement(p, 'button')
    b.text = '2'

    s_html = et.tostring(html).decode()
    util.log_debug(f'=={s_html}')

    return s_html


