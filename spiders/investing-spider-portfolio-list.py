import os
from scrapy.item import Item, Field
from scrapy import Spider
from scrapy.http import Request

class MyPair(Item):
    pairId = Field()
    pairName = Field() 
    pairSymbol = Field()
    priceLast = Field()
    pricePrev = Field()
    priceOpen = Field()
    priceHigh = Field()
    priceLow = Field()
    priceChange = Field()
    priceChangePercent = Field()
    volume = Field()

class InvestingComPortfolioSpider(Spider):
    """
    Set your env-var INVESTING_COM_TOKEN
    """
    name = 'alert-center'

    def start_requests(self):
        request = Request('https://www.investing.com/portfolio/?portfolioID=' + os.environ.get('INVESTING_COM_PORTFOLIO', ''),
                          headers={'Origin': 'https://www.investing.com/',
                                   'Referer': 'https://www.investing.com/',
                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'},
                          cookies={'ses_id': os.environ.get('INVESTING_COM_TOKEN', "")})
        return [request]

    def parse(self, response):
        """
        data-column-name:
          + symbol
          + name
          + 
        """
        for row in response.xpath('//div[@class="js-watchlist-content"]/table/tbody/tr'):
            pair = MyPair()
            pair['pairId'] = int(row.attrib.get('data-pair-id', 0))
            for el in row.xpath('.//td'):
                content = ''.join(el.xpath('.//text()').extract()).strip()
                if el.attrib.get('data-column-name', '') == 'symbol':
                    pair['pairSymbol'] = content
                elif el.attrib.get('data-column-name', '') == 'name':
                    pair['pairName'] = content
                elif el.attrib.get('data-column-name', '') == 'prev':
                    pair['pricePrev'] = content
                elif el.attrib.get('data-column-name', '') == 'last':
                    pair['priceLast'] = content
                elif el.attrib.get('data-column-name', '') == 'high':
                    pair['priceHigh'] = content
                elif el.attrib.get('data-column-name', '') == 'low':
                    pair['priceLow'] = content
                elif el.attrib.get('data-column-name', '') == 'open':
                    pair['priceOpen'] = content
                elif el.attrib.get('data-column-name', '') == 'chg':
                    pair['priceChange'] = content
                elif el.attrib.get('data-column-name', '') == 'chgpercent':
                    pair['priceChangePercent'] = content
                elif el.attrib.get('data-column-name', '') == 'vol':
                    pair['volume'] = content
            yield pair

