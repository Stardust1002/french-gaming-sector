import scrapy
from scraper.items import EntityItem
from bs4 import  BeautifulSoup
import re
import logging


logger = logging.Logger(__name__)

class EntitySpider(scrapy.Spider):
    name = "afjv"
    start_urls = [
            'http://www.afjv.com/annuaires_jeux_video.php',
        ]

    def parse(self, response):
        urls = response.css('.anu_col > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            logger.debug(url)
            yield scrapy.Request(url=url, callback=self.parse_entity)

    def parse_entity(self, response):
        item = EntityItem()
        item['nom'] = response.css('h1[itemprop=name]::text').extract_first()
        item['url'] = response.url
        item['categorie'] = response.css('.arian > span[itemprop=name]::text').extract()[1]
        item['description'] = BeautifulSoup(response.css('#anu_lef > p').extract_first(), 'html.parser').getText()
        item['description'] = item['description'].replace("\n", "").replace("\r", "").replace("\t", "")
        item['logo'] = response.urljoin(response.css('img[itemprop=logo]::attr(src)').extract_first())
        item['ville'] = response.css('span[itemprop=addressLocality]::text').extract_first()
        item['codePostal'] = response.css('span[itemprop=postalCode]::text').extract_first()
        item['rue'] = response.css('span[itemprop=streetAddress]::text').extract_first()
        item['adresse'] = " ".join([item['rue'], item['codePostal'], item['ville']])
        item['telephone'] = response.css('span[itemprop=telephone]::text').extract_first()
        item['fax'] = response.css('span[itemprop=faxNumber]::text').extract_first()
        item['website'] = response.css('#anu_rig > p > a[itemprop=url]::attr(href)').extract_first()
        item['email'] = []
        for paraf in response.css('#anu_rig > p').extract():
            paraf = paraf.replace('<i class="at"></i>', '@').replace('<br>', ' ')
            paraf = BeautifulSoup(paraf, 'html.parser').getText().split(" ")
            for x in paraf:
                tmp = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(x)
                if tmp:
                    print(tmp.string)
                    item['email'].append(tmp.string)
                    break
        item['email'] = ' - '.join(item['email'])
        item['contacts'] = " \n ".join([BeautifulSoup(x.replace('<i class="at"></i>','@'), 'html.parser').getText().replace('  ',' - ') \
                            for x in response.css('.anu_con').extract()])

        item['anneeCreation'] = int(response.css('span[itemprop=foundingDate]::text').extract_first())

        blocDroit = response.css('#anu_rig').extract_first()
        statut = re.findall("div\>Statut : (.*?)\<\/div", blocDroit)
        item['statut'] = statut[0] if len(statut)>0 else ""

        effectifs = re.findall("div\>Effectifs : (.*?)\<\/div", blocDroit)
        item['effectifs'] = effectifs[0] if len(effectifs)>0 else ""

        chiffreAffaire = re.findall("div\>Chiffre d'affaire : (.*?)€", blocDroit)
        item['chiffreAffaire'] = int(chiffreAffaire[0].replace(",","")) if len(chiffreAffaire)>0 else ""

        rcs = re.findall("div\>RCS : (.*?)\<\/div", blocDroit)
        item['RCS'] = rcs[0] if len(rcs)>0 else ""

        naf = re.findall("div\>Code NAF : (.*?)\<\/div", blocDroit)
        item['NAF'] = naf[0] if len(naf)>0 else ""

        item['actualite'] = " \n ".join([BeautifulSoup(x, 'html.parser').getText() for x in response.css('.anu_act').extract()])

        #blocMilieu = response.css("#anu_lef").extract_first()
        #datesClefs = re.findall("h3\>Dates clefs.*?\<li\>(.*?)\<\/li\>", blocMilieu)
        #item['NAF'] = naf[0] if len(naf)>0 else ""

        yield item
