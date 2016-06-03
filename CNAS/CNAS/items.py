import scrapy


class CNASItem(scrapy.Item):
    url = scrapy.Field()
    register_id = scrapy.Field()
    name = scrapy.Field()
    other_name = scrapy.Field()
    contacts = scrapy.Field()
    tel = scrapy.Field()
    postalcode = scrapy.Field()
    fax = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    effective_date = scrapy.Field()
    
    pass

