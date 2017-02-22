# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EntityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nom = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    logo = scrapy.Field()
    email = scrapy.Field()
    categorie = scrapy.Field()
    telephone = scrapy.Field()
    adresse = scrapy.Field()
    rue = scrapy.Field()
    codePostal = scrapy.Field()
    ville = scrapy.Field()
    effectifs = scrapy.Field()
    fax = scrapy.Field()
    contacts = scrapy.Field()
    anneeCreation = scrapy.Field()
    statut = scrapy.Field()
    chiffreAffaire = scrapy.Field()
    administratif = scrapy.Field()
    NAF = scrapy.Field()
    RCS = scrapy.Field()
    actualite = scrapy.Field()
    titresEnCours = scrapy.Field()
    titresMajeurs = scrapy.Field()
    datesClefs = scrapy.Field()
    recrutement = scrapy.Field()
