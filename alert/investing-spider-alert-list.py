import os
from scrapy.item import Item, Field
from scrapy import Spider
from scrapy.http import Request

class MyAlert(Item):
    alertId = Field()
    pairName = Field() 
    pairId = Field()
    threshold = Field()
    value = Field()

class InvestingComAlertSpider(Spider):
    """
    Set your env-var INVESTING_COM_SID
    """
    name = 'alert-center'

    def start_requests(self):
        request = Request('https://www.investing.com/members-admin/alert-center',
                          headers={'Origin': 'https://www.investing.com/',
                                   'Referer': 'https://www.investing.com/',
                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'},
                          cookies={'ses_id': os.environ.get('INVESTING_COM_SID', "")})
        return [request]

    def parse(self, response):
        for res in response.xpath('//tr[@class="js-alert-item"]'):
            """
            {'class': 'js-alert-item', 'data-name': 'US 500 Futures', 'data-alert-id': '50726333', 'data-trigger': 'price', 'data-threshold': 'under', 'data-value': '3335.00', 
            'data-frequency': 'Once', 'data-price-fixed': '2', 'data-change-fixed': '2', 'data-email-notification': '0', 'data-status': '1', 'data-type': 'instrument', 'data-pair-id': '8839'}
            """
            if res.attrib.get('data-type', '') == 'instrument':
                alert = MyAlert()
                alert['alertId'] = int(res.attrib.get('data-alert-id', ''))
                alert['pairName'] = res.attrib.get('data-name', '')
                alert['pairId'] = int(res.attrib.get('data-pair-id', ''))
                alert['threshold'] = res.attrib.get('data-threshold', '')
                alert['value'] = float(res.attrib.get('data-value', ''))
                yield alert

