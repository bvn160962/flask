import traceback

from flask import Flask, request

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

        values = request.form
        util.log_debug(f'timesheets: FORM={values}')

        host = request.environ.get('REMOTE_ADDR')
        user_id = util.get_current_user_id(host)  # set user_id in cache if None!!!
        util.set_cache(host)

        # Установить неделю в кэш
        #
        week = util.get_current_week(host)
        if week is None or week == '':
            current_week = util.get_week()
            util.set_cache_property(host, settings.C_WEEK, current_week)

        html = ui_module.create_info_html(i_type=settings.INFO_TYPE_ERROR, msg='Empty HTML. Возможно, не задан обработчик кнопки.', host=host)
        # return html

        # GET
        #
        if request.method == 'GET':
            util.log_info(f'GET: ...')
            html = app.timesheets_get(host)

        # POST
        #
        if request.method == 'POST':
            util.log_info(f'POST: ...')
            html = app.timesheets_post(values, host)

            if html is None or html == '':
                html = ui_module.create_info_html(i_type=settings.INFO_TYPE_ERROR, host=host, msg='Не удалось сформировать HTML. \nВозможно, не задан обработчик кнопки.')

        return html #'nothing', 204

    except Exception as ex:
        traceback.print_exc()
        util.log_error(f'{ex}')
        return ui_module.create_info_html(msg=str(ex), url=settings.MODULES[settings.M_TIMESHEETS]['url'], i_type=settings.INFO_TYPE_ERROR, host=host)


#
# APPLICATION
#
if __name__ == '__main__':

    # util.log_info(f'root url: {app}')
    application.run(debug=True, port=1000, host='0.0.0.0')

