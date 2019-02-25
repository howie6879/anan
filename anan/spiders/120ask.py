#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/24.
 Target url: https://m.120ask.com/jibing/class/c3/
 mongoexport -d anan -c disease -o disease.json --type json -f "disease_name,disease_url,disease_subject,ask_dict,treatment,symptom"
 mongo 127.0.0.1/anan --quiet --eval "db.disease.find({}, {_id:0}).forEach(printjson);" > disease.json
"""

import aiofiles

from urllib.parse import urljoin

from ruia import AttrField, TextField
from ruia import Item, Response, Spider
from ruia_motor import RuiaMotor
from ruia_ua import middleware as ua_middleware

from anan.config import Config


class DiseaseItem(Item):
    disease_name = TextField(css_select='div.keshi_list>a', many=True)
    disease_url = AttrField(css_select='div.keshi_list>a', attr='href', many=True)

    async def clean_disease_url(self, disease_url):
        domain = 'https://m.120ask.com'
        return [urljoin(domain, i) for i in disease_url]


class DiseaseHomeItem(Item):
    disease_name = TextField(css_select='h1.ti')
    disease_subject = TextField(css_select='div.table>div:nth-child(1)>span')
    disease_ask_lists = TextField(css_select='div.ask_lists div.lists a', many=True)
    disease_ask_link_lists = AttrField(css_select='div.ask_lists div.lists a', attr='href', many=True)

    async def clean_disease_ask_link_lists(self, disease_ask_link_lists):
        return ['http:' + i for i in disease_ask_link_lists]


class DiseaseIntroItem(Item):
    intro = TextField(css_select='div.intro_cont')


class DiseaseSpider(Spider):
    concurrency = 3
    start_urls = ['https://m.120ask.com/jibing/class/c3/']

    async def parse(self, response: Response):
        item = await DiseaseItem.get_item(html=response.html)
        async for resp in self.multiple_request(urls=item.disease_url):
            yield self.parse_disease(response=resp)
        # await self.process_item(item)

    async def parse_disease(self, response: Response):
        item = await DiseaseHomeItem.get_item(html=response.html)
        ask_dict = {}
        for index, value in enumerate(item.disease_ask_lists):
            ask_dict = {
                'question': value,
                'question_href': item.disease_ask_link_lists[index],
            }
        metadata = {
            'disease_name': item.disease_name,
            'disease_url': response.url,
            'disease_subject': item.disease_subject,
            'ask_dict': ask_dict
        }
        yield self.request(url=urljoin(response.url, 'zhiliao'),
                           callback=self.parse_treatment,
                           metadata=metadata)

    async def parse_treatment(self, response: Response):
        item = await DiseaseIntroItem.get_item(html=response.html)
        response.metadata['treatment'] = item.intro
        yield self.request(url=urljoin(response.metadata['disease_url'], 'zhengzhuang'),
                           callback=self.parse_symptom,
                           metadata=response.metadata)

    async def parse_symptom(self, response: Response):
        item = await DiseaseIntroItem.get_item(html=response.html)
        response.metadata['symptom'] = item.intro
        yield RuiaMotor(collection='disease', data=response.metadata)

    async def process_item(self, item: DiseaseItem):
        # 将疾病名称导出
        async with aiofiles.open('./type_of_disease.txt', 'a') as f:
            for index, value in enumerate(item.disease_url):
                await f.write(f'{item.disease_name[index]}  {value}' + '\n')


async def init_plugins_after_start(spider_ins):
    spider_ins.mongodb_config = Config.mongodb_config
    RuiaMotor.init_spider(spider_ins=spider_ins)


if __name__ == '__main__':
    DiseaseSpider.start(middleware=[ua_middleware], after_start=init_plugins_after_start)
