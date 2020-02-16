from config import *
from utils.iml_api import iml_check_balance


def render_main():
    return "<h1>Hello</h1>"


def render_balance_iml():
    balance = iml_check_balance(None, IML_LOGIN, IML_PWD1)
    r = '''
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
