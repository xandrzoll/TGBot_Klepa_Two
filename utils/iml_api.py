import requests
import datetime
import re

from requests.auth import HTTPBasicAuth


urls = {
    'status': 'http://api.iml.ru/Json/GetStatuses',
    'create': 'http://api.iml.ru/Json/CreateOrder',
    'orders': 'http://api.iml.ru/Json/GetOrders',
    'balance': 'http://wmse.iml.ru/API-BZ/API_BZ_IML_Main3PL.asmx?WSDL',
}


def iml_check_balance(dt=None, login='', pwd=''):
    url = urls['balance']

    if not dt:
        dt = datetime.datetime.now()
        dt = dt.strftime(format='%Y-%m-%d')

    xml_data = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetRest xmlns="http://api-bz/">
          <Rest xmlns="http://API_BZ_SOAP.Rest">
            <SKU xmlns=""></SKU>
            <Description xmlns=""></Description>
            <Barcode xmlns=""></Barcode>
            <BarcodeIncome xmlns=""></BarcodeIncome>
            <CheckShippingZone xmlns="">true</CheckShippingZone>
            <Date xmlns="">{}</Date>
          </Rest>
        </GetRest>
      </soap:Body>
    </soap:Envelope>
    '''
    xml_data = xml_data.format(dt)
    xml_data = xml_data.encode('utf-8')

    # headers = {'Content-type': 'application/soap+xml'}
    session = requests.session()
    session.headers = {"Content-Type": "text/xml; charset=utf-8"}
    session.headers.update({"Content-Length": str(len(xml_data))})
    r = session.post(url=url, data=xml_data, auth=HTTPBasicAuth(login, pwd), verify=False)

    pattern = '<kkRestsLine ([^>]+)'
    rests = re.findall(pattern, r.text)
    pattern = 'SKU="([^\"]+)"'
    pattern2 = 'FreeQuantity="([^\"]+)"'

    res = []
    for rest in rests:
        res.append({
            'sim_type': re.findall(pattern, rest)[0],
            'iml_balance': re.findall(pattern2, rest)[0],
        })

    return res
