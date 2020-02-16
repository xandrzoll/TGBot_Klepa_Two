import datetime
from config import *
from utils.iml_api import iml_check_balance


def render_page(title='', body=''):
    r = '''
        <!DOCTYPE html>
        <html>
         <head>
          <meta charset="utf-8">
          <title>{0}</title>
         </head>
         <body>
          {1}
         </body>
        </html>
    '''
    return r.format(title, body)


def render_main():
    title = 'Главная страница'
    body = '''
        <h1>Добрый день!</h1>
        <p>Выберите необходимое:</p>
        <ul>
            <li><a href="/balance_iml">Остатки сим-карт в IML</a></li>
        </ul>
    '''
    return render_page(title, body)


def render_balance_iml():
    get_balance_from_file = False
    balance = []
    b = {}

    try:
        with open(SAVE_BALANCE_IML, 'r') as f:
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
                print('get balance from file')

    except Exception as err:
        print(err)

    if not get_balance_from_file:
        print('get balance from API')
        balance = iml_check_balance(None, IML_LOGIN, IML_PWD1)
        with open(SAVE_BALANCE_IML, 'w') as f:
            for b in balance:
                f.write(';'.join([b['sim_type'], b['iml_balance'], b['dt']]))
                f.write('\n')

    title = 'Остатки сим-карт на складе IML'
    body = '''
    <a href="/"><-- back</a><br>
    <table border="1">
        <tr>
            <th>sim_type</th>
            <th>iml_balance</th>
        </tr>
    '''

    for b in balance:
        body += '<tr><td>{}</td><td>{}</td></tr>'.format(b['sim_type'], b['iml_balance'])

    body += '</table>'
    return render_page(title, body)
