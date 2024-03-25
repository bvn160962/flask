import logging


HOME_DIR = 'c:\\tsh_home\\'
LOG_DIR = HOME_DIR + 'logs\\'
LOG_FILE_NAME = LOG_DIR + 'app_server.log'
LOG_FILE_MODE = 'w' # 'a' - append, 'w' - rewrite
LOG_FILE_LEVEL = logging.DEBUG
LOG_FILE_FORMAT = '%(asctime)s %(funcName)s, line %(lineno)s: %(message)s'

M_TIMESHEETS = 'Timesheets'
MODULES = {
    M_TIMESHEETS: {'name': 'Табель', 'url': '/timesheets'}
}

# WEEK = '2024-W11'
USER = 102

TABLE_BUTTON_WIDTH = '50px'
TAG_LABEL = 'label style="color: black; font-weight: bold;"'
TAG_BUTTON = 'button style="color: #008B8B; font-weight: bold; width: 100%; margin:2px;"'

TAG_BUTTON_TABLE = f'button class="btn-t btn-cursor"'
TAG_BUTTON_TABLE_SELECTED = f'button class="btn-t btn-t-sel btn-cursor"'
TAG_BUTTON_TABLE_EDIT = f'button class="btn-t btn-t-edit btn-cursor"'
TAG_BUTTON_TABLE_IN_APPROVE = f'button class="btn-t btn-t-in_approve btn-cursor"'
TAG_BUTTON_TABLE_APPROVED = f'button class="btn-t btn-t-approved btn-cursor"'
TAG_BUTTON_TABLE_REJECTED = f'button class="btn-t btn-t-rejected btn-cursor"'

TAG_TD_CENTER = 'td align="center"'
TAG_TD_CENTER_BORDER = 'td align="center" style="border: 2px solid #0000FF;"'
TAG_TD_BTN_HEADER_CENTER = f'td align="center" style="background-color: #C0C0C0; font-weight: bold; width:{TABLE_BUTTON_WIDTH};"'
TAG_TD_A_HEADER = f'a style="display: inline-block; max-width: {TABLE_BUTTON_WIDTH};"'
TAG_TD_A_HEADER_P = 'a style="display: inline-block; width:300px"'


SPLITTER = '#'
ENTER_DISABLE = 'onkeydown="if(event.keyCode==13){return false;}"'

INFO_TYPE_INFORMATION = 'Информация'
INFO_TYPE_WARNING = 'Предупреждение'
INFO_TYPE_ERROR = 'Ошибка'

C_USER_PROP = 'p_user_id'
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
UPDATE_TIMESHEET_BUTTON = 'update_timesheet_btn'
LOGOFF_BUTTON = 'logoff_btn'

# Projects
F_PRJ_ID = 'id'
F_PRJ_MANAGER_ID = 'manager_id'
F_PRJ_NAME = 'name'
F_PRJ_START_DATE = 'start_date'
F_PRJ_END_DATE = 'end_date'

F_TSH_ID = 'id'
F_TSH_PRJ_ID = 'project_id'
F_TSH_HOURS = 'hours'
F_TSH_NOTE = 'note'
F_TSH_COMMENT = 'comment'
F_TSH_STATUS = 'status'
F_TSH_DATE = 'date'
F_TSH_USER_NAME = 'usr_name'
F_TSH_PRJ_NAME = 'prj_name'

# FLD_PROJECT = 'name'
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
