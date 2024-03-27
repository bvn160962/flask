import logging


USER = 102

HOME_DIR = 'c:\\tsh_home\\'
LOG_DIR = HOME_DIR + 'logs\\'
LOG_FILE_NAME = LOG_DIR + 'app_server.log'
LOG_FILE_MODE = 'w' # 'a' - append, 'w' - rewrite
LOG_FILE_LEVEL = logging.DEBUG
LOG_FILE_FORMAT = '%(asctime)s %(funcName)s, line %(lineno)s: %(message)s'

# Регистрация модулей
#
M_TIMESHEETS = 'Timesheets'
M_APPROVEMENT = 'Approvement'
M_USERS = 'Users'
M_PROJECTS = 'Projects'

MODULES = {
    M_TIMESHEETS: {'name': 'Табель', 'url': '/timesheets'},
    M_APPROVEMENT: {'name': 'Согласование', 'url': '/approvemnet'},
    M_USERS: {'name': 'Пользователи', 'url': '/users'},
    M_PROJECTS: {'name': 'Проекты', 'url': '/projects'}
}

# Стили для тэгов
#
TAG_TEXT = 'a class=a-head'

TAG_BUTTON_TABLE = f'button class="btn-t"'
# TAG_BUTTON_TABLE_SELECTED = f'button class="btn-t btn-t-sel"'
TAG_BUTTON_TABLE_EDIT = f'button class="btn-t btn-t-edit"'
TAG_BUTTON_TABLE_IN_APPROVE = f'button class="btn-t btn-t-in_approve"'
TAG_BUTTON_TABLE_APPROVED = f'button class="btn-t btn-t-approved"'
TAG_BUTTON_TABLE_REJECTED = f'button class="btn-t btn-t-rejected"'

TAG_TD_CENTER = 'td align=center'
TAG_TD_SELECTED = 'td align=center class=td-selected'
TAG_TD_BTN_HEADER = f'td align="center" class=td-header'
TAG_TD_A_HEADER_P = 'a class=a-prj-head'
TAG_TD_A_HEADER = f'a'


SPLITTER = '#'
ENTER_DISABLE = 'onkeydown="if(event.keyCode==13){return false;}"'

# Типы информационных сообщений
#
INFO_TYPE_INFORMATION = 'Информация'
INFO_TYPE_WARNING = 'Предупреждение'
INFO_TYPE_ERROR = 'Ошибка'

# Переменные кэша
#
C_USER_ID = 'p_user_id'
C_PROJECT_ID = 'p_project_id'
C_TIMESHEET_ID = 'p_timesheet_id'
C_DATE = 'p_date'
C_WEEK = 'p_week'

TABLE_BUTTON = 'table_cell_btn'
SAVE_BUTTON = 'submit_btn'
NEW_BUTTON = 'new_btn'
DELETE_BUTTON = 'delete_btn'
DELETE_BUTTON_YES = 'delete_btn_yes'
DELETE_BUTTON_NO = 'delete_btn_no'
WEEK_BUTTON = 'week_btn'
WEEK_BUTTON_NEXT = 'next_week_btn'
WEEK_BUTTON_PREV = 'prev_week_btn'
WEEK_BUTTON_CURRENT = 'current_week_btn'
UPDATE_BUTTON = 'update_btn'
LOGOFF_BUTTON = 'logoff_btn'

# Атрибуты таблицы Projects
#
F_PRJ_ID = 'prj_id'
F_PRJ_MANAGER_ID = 'prj_manager_id'
F_PRJ_NAME = 'prj_name'
F_PRJ_START_DATE = 'prj_start_date'
F_PRJ_END_DATE = 'prj_end_date'
F_PRJ_ALL = f'{F_PRJ_ID}, {F_PRJ_MANAGER_ID}, {F_PRJ_NAME}, {F_PRJ_START_DATE}, {F_PRJ_END_DATE}'

#  Атрибуты таблицыTimesheets
#
F_TSH_ID = 'tsh_id'
F_TSH_USER_ID = 'tsh_user_id'
F_TSH_PRJ_ID = 'tsh_project_id'
F_TSH_HOURS = 'tsh_hours'
F_TSH_NOTE = 'tsh_note'
F_TSH_COMMENT = 'tsh_comment'
F_TSH_STATUS = 'tsh_status'
F_TSH_DATE = 'tsh_date'
F_TSH_ALL = f'{F_TSH_USER_ID}, {F_TSH_PRJ_ID}, {F_TSH_HOURS}, {F_TSH_STATUS}, {F_TSH_NOTE}, {F_TSH_DATE}, {F_TSH_COMMENT}'
F_TSH_ALL_ID = f'{F_TSH_ID}, {F_TSH_ALL}'

# Атрибуты таблицы Users
#
F_USR_ID = 'usr_id'
F_USR_NAME = 'usr_name'
F_USR_ROLE = 'usr_role'
F_USR_PASSWORD = 'usr_password'
F_USR_MAIL = 'usr_mail'
F_USR_INFO = 'usr_info'
F_USR_ALL = f'{F_USR_ID}, {F_USR_NAME}, {F_USR_ROLE}, {F_USR_PASSWORD}, {F_USR_MAIL}, {F_USR_INFO}'

FLD_TSH_DICT = 'data'
EMPTY_ID_KEY = '-'

EDIT_STATUS = 'edit'
IN_APPROVE_STATUS = 'in_approve'
APPROVED_STATUS = 'approved'
REJECTED_STATUS = 'rejected'
LIST_OF_STATUSES = {
    EDIT_STATUS: 'Редактируется',
    IN_APPROVE_STATUS: 'На согласовании',
}


def get_valid_statuses(status=None):
    if status is None:
        return LIST_OF_STATUSES
    if status == '':
        return LIST_OF_STATUSES

    if status == EDIT_STATUS:
        return LIST_OF_STATUSES

    if status == IN_APPROVE_STATUS:
        return {IN_APPROVE_STATUS: 'На согласовании'}

    if status == APPROVED_STATUS:
        return {APPROVED_STATUS: 'Согласован'}

    if status == REJECTED_STATUS:
        return {
            EDIT_STATUS: 'Редактируется',
            REJECTED_STATUS: 'Отклонен',
        }

    return LIST_OF_STATUSES
