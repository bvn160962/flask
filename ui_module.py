from flask import render_template
from xml.etree import ElementTree as et
from xml.dom.minidom import getDOMImplementation
import jinja2

import data_module
import app

PROJECT_ID_NAME = 'project_id'
TIMESHEET_ID_NAME = 'tsh_id'
INPUT_HOURS_NAME = 'inp_hours'
INPUT_NOTE_NAME = 'inp_note'


def create_html_static():
    html = render_template('home.html')
    return html


def create_html_etree(prj_id='', tsh_id='', tsh_entry=None):
    hours = ''
    note = ''
    if tsh_entry is not None:
        hours = tsh_entry.get(app.FLD_HOURS)
        note = tsh_entry.get(app.FLD_NOTE)

    html = et.Element('html', attrib={'lang': 'en'})
    body = et.SubElement(html, 'body')

    form = et.SubElement(body, 'form', attrib={'name': 'form_time_sheets', 'action': '', 'method': 'POST'})

    p_hidden = et.SubElement(form, 'p hidden')
    p_week = et.SubElement(form, 'p')
    p1 = et.SubElement(form, 'p')

    et.SubElement(p_hidden, 'input', attrib={'type': 'text', 'name': PROJECT_ID_NAME, 'value': prj_id})
    et.SubElement(p_hidden, 'input', attrib={'type': 'text', 'name': TIMESHEET_ID_NAME, 'value': tsh_id})

    et.SubElement(p_week, 'input', attrib={'type': 'week', 'name': 'week', 'value': ''})
    btn_week = et.SubElement(p_week, 'button',
                             attrib={'type': 'submit', 'name': app.WEEK_BUTTON_VALUE, 'value': 'week'})
    btn_week.text = 'set'

    # time sheet info area
    #

    l_hours = et.SubElement(p1, 'label', attrib={'for': 'hours'})
    l_hours.text = ' Hours:'
    et.SubElement(p1, 'input', attrib={'type': 'text', 'name': INPUT_HOURS_NAME, 'placeholder': '-', 'value': hours})
    l_note = et.SubElement(p1, 'label', attrib={'for': 'note'})
    l_note.text = ' Note:'
    et.SubElement(p1, 'input',
                  attrib={'type': 'text', 'name': INPUT_NOTE_NAME, 'placeholder': 'Заметка', 'value': note})
    btn_submit = et.SubElement(p1, 'button',
                               attrib={'type': 'submit', 'name': app.SAVE_BUTTON_VALUE, 'value': 'submit'})
    btn_submit.text = 'Save'
    btn_clear = et.SubElement(p1, 'button', attrib={'type': 'reset', 'name': 'btn_reset', 'value': 'clear'})
    btn_clear.text = 'Clear'

    # time sheets table area
    #
    p2 = et.SubElement(form, 'p')
    table = et.SubElement(p2, 'table')

    # head of table (project + dates)
    #
    time_sheets_data = data_module.get_data()
    days_1 = list(time_sheets_data.values())[0]
    print(f'1: {days_1}')
    dates_node = et.SubElement(table, 'tr')
    dates_col_node = et.SubElement(dates_node, 'td')
    lab_project = et.SubElement(dates_col_node, 'label')
    lab_project.text = 'PROJECTS'
    for day in days_1:
        dates_cell_node = et.SubElement(dates_node, 'td')
        btn_day = et.SubElement(dates_cell_node, 'button disabled', attrib={'type': 'submit', 'name': 'btn_' + day, 'value': day})
        btn_day.text = day

    # table rows (project + hours)
    #
    row = 0
    for project in time_sheets_data:
        # projects
        #
        row += 1
        days = time_sheets_data[project]
        col = 0
        row_node = et.SubElement(table, 'tr')
        project_ceil = et.SubElement(row_node, 'td')
        lab_project = et.SubElement(project_ceil, 'label')
        lab_project.text = project
        for day in days:
            col += 1
            time_sheets = days[day]
            for tsh in time_sheets:
                uid = project + '#' + tsh
                hours = time_sheets[tsh][app.FLD_HOURS]
                # note = time_sheets[tsh][f_note]
                # c_name = str(row)+'_'+str(col)
                # print(f'{uid}:: {hours}')
                day_node = et.SubElement(row_node, 'td')
                btn_node = et.SubElement(day_node, 'button',
                                         attrib={'type': 'submit', 'name': app.TABLE_BUTTON_VALUE, 'value': uid})
                btn_node.text = hours

    str_html = et.tostring(html).decode()
    print(f'str_html: {str_html}')
    return str_html


def create_html_jinja():
    env = jinja2.Environment()

    html_doctype = '<!DOCTYPE html>'
    html_head = \
        '\
        <head>\
            <meta charset = "UTF-8">\
            <meta http - equiv = "X-UA-Compatible" content = "IE=edge">\
            <meta name = "viewport" content = "width=device-width, initial-scale=1.0">\
            <title > Document </title>\
        </head> \
        '
    html_html = '<html lang = "en" xmlns = "http://www.w3.org/1999/html">'

    str_html_body = \
        '\
    <body>\
        <p>\
            <label for="hours">Hours:</label>\
            <input type="text" id="hours" name="hours" placeholder="-">\
        </p>\
    </body>\
    '
    str_html = html_doctype
    str_html += html_head
    str_html += html_html
    str_html += str_html_body
    str_html += '</html>'

    html = env.from_string(str_html)
    return html.render()


def create_html_minidom():
    uls = ["1. first item", "2. second item", "3. third item"]
    str = create_uls(uls)
    print(f'str: {str}')
    return str


def create_uls(items):
    dom = get_dom()
    html = dom.documentElement
    ul = dom.createElement("ul")
    for item in items:
        li = dom.createElement("li")
        li.appendChild(dom.createTextNode(item))
        ul.appendChild(li)
    html.appendChild(ul)
    return dom.toxml()


def get_dom():
    impl = getDOMImplementation()
    doc_type = impl.createDocumentType(
        "html",
        "-//W3C//DTD XHTML 1.0 Strict//EN",
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
    )
    return impl.createDocument("http://www.w3.org/1999/xhtml", "html", doc_type)
