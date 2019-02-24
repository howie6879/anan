#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/24.
 Target url: https://m.120ask.com/jibing/class/c3/
"""

import aiofiles

from urllib.parse import urljoin

from ruia import AttrField, TextField
from ruia import Item, Response, Spider


class DiseaseItem(Item):
    disease_name = TextField(css_select='div.keshi_list>a', many=True)
    disease_url = AttrField(css_select='div.keshi_list>a', attr='href', many=True)

    async def clean_disease_url(self, disease_url):
        domain = 'https://m.120ask.com'
        return [urljoin(domain, i) for i in disease_url]


class DiseaseSpider(Spider):
    start_urls = ['https://m.120ask.com/jibing/class/c3/']

    async def parse(self, response: Response):
        item = await DiseaseItem.get_item(html=response.html)
        urls = [urljoin(url, 'zhiliao') for url in item.disease_url]
        async for resp in self.multiple_request(urls=urls):
            pass
        # await self.process_item(item)

    async def process_item(self, item: DiseaseItem):
        # 将疾病名称导出
        async with aiofiles.open('./type_of_disease.txt', 'a') as f:
            for index, value in enumerate(item.disease_url):
                await f.write(f'{item.disease_name[index]}  {value}' + '\n')


if __name__ == '__main__':
    DiseaseSpider.start()
