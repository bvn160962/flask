import traceback

from flask import Flask, request

import data_module
import ui_module

FLD_HOURS = 'hours'
FLD_NOTE = 'note'

TABLE_BUTTON_VALUE = 'table_cell_btn'
SAVE_BUTTON_VALUE = 'submit_btn'
WEEK_BUTTON_VALUE = 'week_btn'

app = Flask(__name__)

# Creating a route that has both GET and POST request methods
@app.route('/', methods=['GET', 'POST'])
def message():
    # POST
    #
    html = 'HTML страница не сгенерирована!'

    values = request.form
    print(f'values: {values}')

    if request.method == 'POST':
        print(f'POST: ...')

        try:
            for value in values:
                if value == TABLE_BUTTON_VALUE:  # Если нажата одна из кнопок в таблице
                    print('Нажата кнопка в Таблице')
                    val = values[value]
                    s = val.split('#')
                    if s is None: raise Exception('Ошибка при парсинге values: None')
                    else:
                        if len(s) != 2:
                            raise Exception(f'Ошибка при парсинге values: {len(s)}')
                    project_id = s[0]
                    tsh_id = s[1]
                    tsh_entry = data_module.get_entry(project_id, tsh_id)
                    if tsh_entry is None:
                        raise Exception(f'Timesheet {project_id}, {tsh_id} не найден')
                    print(f'tsh_entry: {tsh_entry}')

                    html = ui_module.create_html_etree(project_id, tsh_id, tsh_entry)
                    if html is None:
                        raise Exception('Не удалось сформировать HTML')


                if value == SAVE_BUTTON_VALUE:
                    print('Нажата кнопка Save')
                    print(f'form: {request.form}')

                    prj_id = ''
                    tsh_id = ''
                    inp_hours = ''
                    inp_note = ''
                    for value in values:
                        if value == ui_module.PROJECT_ID_NAME: prj_id = values[value]
                        if value == ui_module.TIMESHEET_ID_NAME: tsh_id = values[value]
                        if value == ui_module.INPUT_HOURS_NAME: inp_hours = values[value]
                        if value == ui_module.INPUT_NOTE_NAME: inp_note = values[value]

                    if prj_id == '' or tsh_id == '':
                        raise Exception(f'Пустые значения идентификаторов project={prj_id}, timesheet={tsh_id}')
                    data_module.update_entry(prj_id, tsh_id, {FLD_HOURS: inp_hours, FLD_NOTE: inp_note})
                    html = ui_module.create_html_etree()


        except Exception as ex:
            traceback.print_exc()
            print(f'**error: {ex}')
            return 'Error'

        return html #'nothing', 204

    # GET
    #
    if request.method == 'GET':
        print(f'GET: ...')
        # return ui_module.create_html_jinja()
        # return ui_module.create_html_static()
        # return ui_module.create_html_minidom()
        return ui_module.create_html_etree()


# @app.route('/upload')
# def upload():
#     print('upload')


# @app.route('/background_process_test')
# def background_process_test_():
#     print('Test.OnClick(...)')
#
#     form = request.form
#     print(f'form: {form.listvalues()}')
#
#     return 'nothing'


# start the application
#
if __name__ == '__main__':
    # Running the application and leaving the debug mode ON
    app.run(debug=True, port=1000, host='0.0.0.0')
