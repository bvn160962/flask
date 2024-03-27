import traceback

from flask import Flask, request

import app_module
import pg_module
import ui_module
import settings
import util_module as util
import app_module as app

app_cache = {}
application = Flask(__name__)


def _test():
    # return ui_module.create_html_static()
    return ui_module.t_html()
    # s = settings.MODULES[settings.M_TIMESHEETS]['url']
    # print(f'=={s}')

#
# TIMESHEETS
#
@application.route(settings.MODULES[settings.M_TIMESHEETS]['url'], methods=['GET', 'POST'])
def timesheets():
    try:
        # _test()
        # return ui_module.t_html()

        host, values, html_test_db, user_id = app_module.init_module(request)
        if html_test_db != '':
            return html_test_db

        # Установить неделю в кэш
        #
        week = util.get_current_week(host)
        if week is None or week == '':
            current_week = util.get_week()
            util.set_cache_property(host, settings.C_WEEK, current_week)

        html = ui_module.create_info_html(
            i_type=settings.INFO_TYPE_ERROR,
            module=settings.M_TIMESHEETS,
            msg='Empty HTML. Возможно, не задан обработчик кнопки.',
            host=host
        )
        # return html

        # GET
        #
        if request.method == 'GET':
            util.log_info(f'timesheetsGET: ...')
            html = app.timesheets_get(host)

        # POST
        #
        if request.method == 'POST':
            util.log_info(f'timesheetsPOST: ...')
            html = app.timesheets_post(values, host)

            if html is None or html == '':
                msg = 'Не удалось сформировать HTML. \nВозможно, не задан обработчик кнопки.'
                html = ui_module.create_info_html(module=settings.M_TIMESHEETS, i_type=settings.INFO_TYPE_ERROR, host=host, msg=msg)

        return html #'nothing', 204

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'{ex}')
        return ui_module.create_info_html(msg=str(ex), module=settings.M_TIMESHEETS, i_type=settings.INFO_TYPE_ERROR, host=host)


@application.route(settings.MODULES[settings.M_APPROVEMENT]['url'], methods=['GET', 'POST'])
def approvement():
    try:
        host = request.environ.get('REMOTE_ADDR')

        return 'nothing', 204

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'{ex}')
        return ui_module.create_info_html(msg=str(ex), module=settings.M_TIMESHEETS, i_type=settings.INFO_TYPE_ERROR, host=host)


#
# USERS
#
@application.route(settings.MODULES[settings.M_USERS]['url'], methods=['GET', 'POST'])
def users():
    try:
        host, values, html_test_db, user_id = app_module.init_module(request)
        if html_test_db != '':
            return html_test_db
        # util.log_debug(f'users: host={host}, user_id={user_id}, values={values}, html_test_db={html_test_db}')

        # GET
        #
        if request.method == 'GET':
            util.log_info(f'users.GET: ...')
            return app.users_get(host)

        # POST
        #
        if request.method == 'POST':
            util.log_info(f'users.POST: ...')
            return app.users_post(values, host)

        # raise Exception('Users...')
        # return 'nothing'  #, 204

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'{ex}')
        return ui_module.create_info_html(msg=str(ex), module=settings.M_USERS, i_type=settings.INFO_TYPE_ERROR, host=host)


#
# APPLICATION
#
if __name__ == '__main__':

    # util.log_info(f'root url: {app}')
    application.run(debug=True, port=1000, host='0.0.0.0')

