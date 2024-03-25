import traceback

import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime

import data_module
import settings
import util_module as util

DB_CONNECT = None
PG_HOST = 'localhost'
PG_PORT = '54321'
PG_DATABASE = 'postgres'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'


# Соединение с БД
#
def get_connect():
    global DB_CONNECT

    try:
        if DB_CONNECT is None:
            DB_CONNECT = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DATABASE, user=PG_USER, password=PG_PASSWORD)
            # util.log_debug(f'Connected to database: <{PG_DATABASE}> on <{PG_HOST}>')
        # else:
        #     util.log_debug(f'Use existing connect {DB_CONNECT}')
        return DB_CONNECT

    except Exception as ex:
        util.log_error(f'Can`t establish connection to database {ex}: host={PG_HOST}, port={PG_PORT}, dbname={PG_DATABASE}, user={PG_USER}')
        raise ex
    # finally:
    #     return DB_CONNECT


class Entries:

    SQL_ONE_ENTRY = 'Select id, user_id, project_id, hours, status, note, date, comment From ts_entries Where id = '

    SQL_INSERT_ENTRY = 'Insert INTO ts_entries (user_id, project_id, hours, status, note, date, comment) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s)\
                       '

    SQL_DELETE_ENTRY = 'Delete From ts_entries Where id = '

    SQL_ALL_ENTRIES = 'Select e.id, e.user_id, e.project_id, e.hours, e.status, e.note, e.date, e.comment, p.name \
                       From ts_entries as e, ts_projects as p \
                       Where e.date >= %s and e.date <= %s \
                       And e.user_id = %s \
                       And e.project_id = p.id \
                       Order by p.name\
                      '

    SQL_UPDATE_ENTRY = 'Update ts_entries \
                        Set hours = %s, note = %s, status = %s, comment = %s \
                        Where id = %s\
                       '

    SQL_FOR_APPROVAL_ENTRIES = f'Select distinct e.id, e.user_id, e.project_id, e.date, e.hours, e.status, e.note, e.comment, p.name as prj_name, u.name as usr_name \
                                From ts_entries e, ts_projects p, ts_users u \
                                Where e.status = \'{settings.IN_APPROVE_STATUS}\' \
                                And e.project_id = p.id \
                                And e.user_id = u.id \
                                And p.manager_id = '

    SQL_UPDATE_STATUS = 'Update ts_entries \
                        Set status = %s \
                        Where id in %s\
                       '

    # def __init__(self):
    #     util.log_debug("__init__")

    @classmethod
    def get_entries(cls, s_date=None, e_date=None, user_id=None):
        try:
            # sql = "select *, to_char(date, 'YYYY-MM-DD') as d from ts_entries"
            if s_date is None:
                raise Exception('s_date is None')
            if e_date is None:
                raise Exception('e_date is None')
            if user_id is None:
                raise Exception('user_id is None')

            # util.log_debug(f'select: for user_id={user_id} in ({s_date}, {e_date})')
            conn = get_connect()

            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_ALL_ENTRIES, (s_date, e_date, user_id))
                return curs.fetchall()

        except Exception as ex:
            util.log_error(f'Error on Select Entries for user id: {user_id} ({ex})')

    @classmethod
    def update_entry(cls, tsh_id=None, data=None):
        try:
            if tsh_id is None:
                raise Exception('entry id is None')
            if data is None:
                raise Exception(f'data for entry {tsh_id} is None')

            # parsing data
            #
            hours = data.get(settings.F_TSH_HOURS)
            note = data.get(settings.F_TSH_NOTE)
            status = data.get(settings.F_TSH_STATUS)
            comment = data.get(settings.F_TSH_COMMENT)

            util.log_debug(f'update entry: {tsh_id}')
            conn = get_connect()

            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_UPDATE_ENTRY, (hours, note, status, comment, tsh_id))
                curs.execute('commit')

        except Exception as ex:
            util.log_error(f'Error on Update Entry for id {tsh_id}: ({ex})')

    @classmethod
    def get_entry_by_id(cls, tsh_id=None):
        try:
            if tsh_id is None:
                raise Exception('entry id is None')

            # util.log_debug(f'get entry by id: {tsh_id}')

            conn = get_connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_ONE_ENTRY + tsh_id)
                return curs.fetchall()

        except Exception as ex:
            util.log_error(f'Error on Select Entry for id {tsh_id}: ({ex})')


    @classmethod
    def add_entry(cls, user_id=None, prj_id=None, data=None):
        try:
            # util.log_debug(f'add_entry {prj_id}, {user_id}, {data}')

            hours = data.get(settings.F_TSH_HOURS)
            status = data.get(settings.F_TSH_STATUS)
            note = data.get(settings.F_TSH_NOTE)
            date = data.get(settings.F_TSH_DATE)
            comment = data.get(settings.F_TSH_COMMENT)

            conn = get_connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_INSERT_ENTRY, (user_id, prj_id, hours, status, note, date, comment))
                curs.execute('commit')

        except Exception as ex:
            util.log_error(f'Error on Insert Entry for prj_id "{prj_id}": ({ex})')


    @classmethod
    def delete_entry(cls, tsh_id=None):
        try:
            util.log_debug(f'delete_entry: {tsh_id}')
            if tsh_id is None:
                raise Exception('tsh_id is None')

            if tsh_id == '':
                raise Exception('tsh_id is Empty')

            conn = get_connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_DELETE_ENTRY + tsh_id)
                curs.execute('commit')

        except Exception as ex:
            util.log_error(f'Error on Delete Entry for tsh_id "{tsh_id}": ({ex})')

    @classmethod
    def get_for_approval_entries(cls, user_id=None):
        try:
            util.log_debug(f'get_for_approval_entries: for user_id={user_id}')
            if user_id is None:
                raise Exception('user_id is None')

            i_user_id = int(user_id)

            conn = get_connect()
            sql = f'{cls.SQL_FOR_APPROVAL_ENTRIES}{user_id}'
            # util.log_debug(f'get_for_approval_entries: sql={sql}')
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(sql)
                return curs.fetchall()

        except Exception as ex:
            util.log_error(f'Error on Select for approval Entries for user_id={user_id}: ({ex})')


    @classmethod
    def update_for_approval_status(cls, e_list, verdict):
        try:
            util.log_debug(f'get_for_approval_entries: for list={e_list} with verdict={verdict}')
            if e_list is None:
                raise Exception('list of entries is None')

            if verdict:
                status = f'{settings.APPROVED_STATUS}'
            else:
                status = f'{settings.REJECTED_STATUS}'

            conn = get_connect()
            # sql = f'{cls.SQL_FOR_APPROVAL_ENTRIES}{user_id}'
            util.log_debug(f'get_for_approval_entries: list={list}, status={status}')
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_UPDATE_STATUS, (status, e_list))
                curs.execute('commit')

        except Exception as ex:
            util.log_error(f'Error on Select for approval Entries for list={e_list}, verdict={verdict}: ({ex})')



class Projects:

    SQL_ALL_PROJECTS = 'Select id, manager_id, name, start_date, end_date From ts_projects Order by name'

    @classmethod
    def get_all_projects(cls):
        try:
            # util.log_debug(f'get_all_projects')

            conn = get_connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(cls.SQL_ALL_PROJECTS)
                return curs.fetchall()

        except Exception as ex:
            util.log_error(f'Error on getting all projects: ({ex})')











# Реализация (отладка)
#
if __name__ == '__main__':
    util.log_debug(f'{__name__}')
    try:
        # date = datetime.datetime.strptime('05012010', "%d%m%Y").date()
        # date = datetime.datetime.now()
        # week = util.get_week_by_date(date)
        # util.log_debug(f'week={week}')
        #
        # # w = '2024-W53'
        # w = '2024-W11'
        # usr_id = 102
        #
        # d = data_module.get_all_entries(user_id=usr_id, week=w)
        # util.log_debug(f'd: {d}')
        # exit(1)

        entr = Entries()
        c = entr.get_for_approval_entries(102)
        print(f'=={c}')

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'Exception: {ex}')
