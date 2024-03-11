import app

time_sheets_data = {
    'project_id_1': {
        '20': {'time_sheet_id1': {app.FLD_HOURS: '5', app.FLD_NOTE: 'note 1'}},
        '21': {'time_sheet_id2': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
        '22': {'time_sheet_id3': {app.FLD_HOURS: '8', app.FLD_NOTE: 'note 3'}},
        '23': {'time_sheet_id4': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
        '24': {'time_sheet_id5': {app.FLD_HOURS: '8', app.FLD_NOTE: 'note 5'}},
        '25': {'time_sheet_id6': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
        '26': {'time_sheet_id7': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
    },
    'project_id_2': {
        '20': {'time_sheet_id10': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
        '21': {'time_sheet_id20': {app.FLD_HOURS: '5', app.FLD_NOTE: 'note 2'}},
        '22': {'time_sheet_id30': {app.FLD_HOURS: '8', app.FLD_NOTE: 'note 3'}},
        '23': {'time_sheet_id40': {app.FLD_HOURS: '1', app.FLD_NOTE: 'note 4'}},
        '24': {'time_sheet_id50': {app.FLD_HOURS: '8', app.FLD_NOTE: 'note 5'}},
        '25': {'time_sheet_id60': {app.FLD_HOURS: '3', app.FLD_NOTE: 'note 6'}},
        '26': {'time_sheet_id70': {app.FLD_HOURS: '-', app.FLD_NOTE: ''}},
    },
}


def get_data():
    return time_sheets_data


def get_entry(project_id, tsh_id):
    p_dict = time_sheets_data[project_id]

    for i_dict in p_dict.values():
        for k in i_dict.keys():
            if k == tsh_id:
                # print(f'i_dict={i_dict[k]}')
                return i_dict[k]

    return None

def update_entry(project_id, tsh_id, data):
    # print(f'update_entry({project_id}, {tsh_id}, {data})')

    for entry in time_sheets_data:
        if entry == project_id:
            for v in time_sheets_data[entry].values():
                if list(v.keys())[0] == tsh_id:
                    v[tsh_id] = data

    return None


