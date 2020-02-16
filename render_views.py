import datetime
from config import *
from utils.iml_api import iml_check_balance


def render_main():
    r = '''
        <h1>Hello this is main page</h1>
        <p>Choose what you need:</p>
        <ul>
            <li><a href="/balance_iml">getting the balances from IML API</a></li>
        </ul>
    '''
    return r


def render_balance_iml():
    get_balance_from_file = False
    balance = []
    b = {}

    try:
        with open('utils/balance.csv', 'r') as f:
            dt = f.readline().split(';')[2]
            if dt[:-1] == datetime.datetime.now().strftime(format='%Y-%m-%d'):
                f.seek(0)
                for line in f:
                    _ = line.split(';')
                    balance.append({
                        'sim_type': _[0],
                        'iml_balance': _[1],
                        'dt': _[2][:-1],
                    })
                get_balance_from_file = True
                print('From file')

    except Exception as err:
        print(err)

    if not get_balance_from_file:
        print('From API')
        balance = iml_check_balance(None, IML_LOGIN, IML_PWD1)
        with open('utils/balance.csv', 'w') as f:
            for b in balance:
                f.write(';'.join([b['sim_type'], b['iml_balance'], b['dt']]))
                f.write('\n')

    r = '''
    <a href="/"><-- back</a><br>
    <table border="1">
        <tr>
            <th>sim_type</th>
            <th>iml_balance</th>
        </tr>
    '''

    for b in balance:
        r += '<tr><td>{}</td><td>{}</td></tr>'.format(b['sim_type'], b['iml_balance'])

    r += '</table>'
    return r
