admitad-python-api [![Build Status](https://travis-ci.org/janitor/admitad-python-api.svg?branch=master)](https://travis-ci.org/janitor/admitad-python-api)
==================

A Python wrapper around the [Admitad API](https://developers.admitad.com/en/)

Install
-------

    pip install admitad-api

Example
-------
```python
from pyadmitad import api

client_id = "[client_id]"
client_secret = "[client_secret]"
scope = ' '.join(set([client.Me.SCOPE]))

client = api.get_oauth_client_client(
    client_id,
    client_secret,
    scope
)

print(client.Me.get())
```

Tests
-----

    python setup.py test

API Items
-------------

### Me ###

```python
res = client.Me.get()
```


### Balance ###

```python
res = client.Balance.get()
res = client.Balance.get(extended=True)
```


### PaymentsSettings ###

```python
res = client.PaymentsSettings.get()
res = client.PaymentsSettings.get(currency='USD')
```


### Types of websites ###

```python
res = client.WebsiteTypes.get()
res = client.WebsiteTypes.get(limit=2, offset=1)
```


### Regions of websites ###

```python
res = client.WebsiteRegions.get()
res = client.WebsiteRegions.get(limit=2, offset=1)
```

### Languages ###

```python
res = client.SystemLanguages.get()
res = client.SystemLanguages.get(limit=2, offset=1)
res = client.SystemLanguages.getOne(code='ru')
```

### Currencies ###

```python
res = client.SystemCurrencies.get()
res = client.SystemCurrencies.get(limit=2, offset=1)
```


### Advertising services ###

```python
res = client.AdvertiserServices.get()
res = client.AdvertiserServices.get(limit=2, offset=1)
res = client.AdvertiserServices.getOne(1)
res = client.AdvertiserServices.getForKind(kind='website')
res = client.AdvertiserServices.getForKindOne(2, kind='website')
```


### Categories of advertising campaigns ###

```python
res = client.CampaignCategories.get()
res = client.CampaignCategories.get(campaign=10, language='en')
res = client.CampaignCategories.get(limit=2, offset=1)
res = client.CampaignCategories.getOne(2)
```

### Coupons ##

###### List of coupons ######

```python
res = client.Coupons.get()
res = client.Coupons.get(order_by=['date_start', '-name'])
res = client.Coupons.get(order_by='-date_end')
res = client.Coupons.get(campaign=1, category=2)
res = client.Coupons.get(campaign=[1, 2], category=[2, 3])
res = client.Coupons.getOne(2)
```

###### List of coupons for a website ######

```python
res = client.CouponsForWebsite.get(2)
res = client.CouponsForWebsite.get(2, order_by=date_start)
res = client.CouponsForWebsite.get(2, campaign=1, category=2)
res = client.CouponsForWebsite.get(2, campaign=[1, 2], category=2)
res = client.CouponsForWebsite.getOne(2, 1)
```

###### List of coupons categories ######

```python
res = client.CouponsCategories.get()
res = client.CouponsCategories.get(limit=10, offset=10)
res = client.CouponsCategories.getOne(2)
```

### Websites ###

##### List of websites #####

```python
res = client.Websites.get(limit=10)
res = client.Websites.get(status='new', campaign_status='active')
res = client.Websites.getOne(2)
```

##### Manage websites #####

###### Create website ######

```python
res = client.WebsitesManage.create(
    name='website1',
    kind='website',
    language='ru',
    adservice=2,
    site_url='http://site.com',
    description='description',
    categories=[1, 2],
    regions=['RU'],
    atnd_hits=20,
    atnd_visits=10,
    mailing_targeting=False
)
```

###### Update website ######

```python
res = client.WebsitesManage.update(50, name='test', language='de')
```

###### Verify website ######

```python
res = client.WebsitesManage.verify(50)
```

###### Delete website ######

```python
res = client.WebsitesManage.delete(50)
```


### Statistics ###

###### Statistics by websites ######

```python
res = client.StatisticWebsites.get(website=1, campaign=1)
res = client.StatisticWebsites.get(subid="ADS778")
res = client.StatisticWebsites.get(limit=2)
res = client.StatisticWebsites.get(date_start='01.01.2013')
```

###### Statistics by campaigns ######

```python
res = client.StatisticCampaigns.get()
res = client.StatisticCampaigns.get(website=1, campaign=1)
res = client.StatisticCampaigns.get(subid="ADS778")
res = client.StatisticCampaigns.get(limit=2)
res = client.StatisticCampaigns.get(date_start='01.01.2013')
```


###### Statistics by days ######

```python
res = client.StatisticDays.get()
res = client.StatisticDays.get(website=1, campaign=1)
res = client.StatisticDays.get(subid="ADS778")
res = client.StatisticDays.get(limit=2)
res = client.StatisticDays.get(date_start='01.01.2013')
```

###### Statistics by months ######

```python
res = client.StatisticMonths.get()
res = client.StatisticMonths.get(website=1, campaign=1)
res = client.StatisticMonths.get(subid="ADS778")
res = client.StatisticMonths.get(limit=2)
res = client.StatisticMonths.get(date_start='01.01.2013')
```


###### Statistics by actions ######

```python
res = client.StatisticActions.get()
res = client.StatisticActions.get(date_start='01.01.2013')
res = client.StatisticActions.get(website=1, campaign=1)
res = client.StatisticActions.get(subid="ADS778")
res = client.StatisticActions.get(subid2="ADS778")
res = client.StatisticActions.get(limit=2)
```

###### Statistics by sub-ids ######

```python
res = client.StatisticSubIds.get()
res = client.StatisticSubIds.get(date_start='01.01.2013')
res = client.StatisticSubIds.get(subid="ADS778")
res = client.StatisticSubIds.get(subid1="ADS778", sub_id_number=2)
res = client.StatisticSubIds.get(limit=2)
```


###### Statistics by sources ######

```python
res = client.StatisticSources.get()
res = client.StatisticSources.get(date_start='01.01.2013')
res = client.StatisticSources.get(limit=2)
```

###### Statistics by keywords ######

```python
res = client.StatisticKeywords.get()
res = client.StatisticKeywords.get(date_start='01.01.2013')
res = client.StatisticKeywords.get(limit=2)
```


### Referrals ###

```python
res = client.Referrals.get()
res = client.Referrals.get(limit=2)
res = client.Referrals.getOne(2)
```


### Banners ###

###### List of banners ######

```python
res = client.Banners.get(2)
res = client.Banners.get(2, mobile_content=False, limit=2)
```

###### List of banners for a website ######

```python
res = client.BannersForWebsite.get(_id=2, w_id=3)
res = client.BannersForWebsite.get(2, 3)
res = client.BannersForWebsite.get(2, 3, uri_scheme='https', limit=5)
```


### Campaigns ###

###### List of campaigns ######

```python
res = client.Campaigns.get()
res = client.Campaigns.get(limit=2)
res = client.Campaigns.getOne(2)
```

###### List of campaigns for a website ######

```python
res = client.CampaignsForWebsite.get(22)
res = client.CampaignsForWebsite.get(limit=2)
res = client.CampaignsForWebsite.getOne(6, 22)
```

###### Manage campaigns ######

```python
res = client.CampaignsManage.connect(6, 22)
res = client.CampaignsManage.connect(c_id=6, w_id=22)
res = client.CampaignsManage.disconnect(6, 22)
res = client.CampaignsManage.disconnect(c_id=6, w_id=22)
```


### Payments ###


###### List of payment ######

```python
res = client.Payments.get()
res = client.Payments.get(limit=2, has_statement=True)
res = client.Payments.getOne(2)
```

###### Payments statement ######

```python
res = client.PaymentsStatement.get(12)
res = client.PaymentsStatement.get(12, detailed=True)
```

###### Manage payments ######

```python
res = client.PaymentsManage.create('USD')
res = client.PaymentsManage.confirm(71)
res = client.PaymentsManage.delete(71)
```

### Broken links ###

###### List of broken links ######

```python
res = client.BrokenLinks.get()
res = client.BrokenLinks.get(website=[10, 20], date_start='01.01.2010')
res = client.BrokenLinks.getOne(10)
```

###### Manage broken links ######

```python
res = client.ManageBrokenLinks.resolve(10)
res = client.ManageBrokenLinks.resolve([10, 11, 12])
```

### Announcements ###

###### List of annouuncements ######

```python
res = client.Announcements.get()
res = client.Announcements.getOne(10)
```

### News ###

###### List of news ######

```python
res = client.News.get()
res = client.News.get(limit=10, offset=20)
res = client.News.getOne(10)
```

### Links validator ###

###### Validate link ######

```python
res = client.LinksValidator.get('https://admitad.com/some_url/')
```

### Landings ###

###### List of landings ######

```python
res = client.Landings.get(10)
res = client.Landings.get(10, limit=100)
```

###### List of landings for website ######

```python
res = client.LandingsForWebsite.get(10, 22)
res = client.LandingsForWebsite.get(10, 22, limit=100)
```

### Deeplinks ###

###### Create deeplink ######

```python
res = client.DeeplinksManage.create(22, 10, ulp='https://admitad.com/some/', subid='AS32djkd31')
```

### Referrals ###

###### List of referrals ######

```python
res = client.Referrals.get()
res = client.Referrals.get(date_start='01.01.2010', date_end=datetime.today())
res = client.Referrals.getOne(181)
```

### Optcodes ###

###### List of opt-codes ######

```python
res = client.OptCodes.get()
res = client.OptCodes.get(campaign=100, order_by=['method', 'desc_mode')
res = client.OptCodes.getOne(11)
```

###### Offer status opt-codes manager ######

```python
res = client.OfferStatusOptCodesManager.create(
    website=10, campaign=100, desc_mode=0, method=l,
    url='https://admitad.com/foobarbaz/'
)
res = client.OfferStatusOptCodesManager.update(
    desc_mode=1, method=1
)
```

###### Action opt-codes manager ######

```python
res = client.ActionOptCodesManager.create(
    website=10, campaign=100, desc_mode=0, method=l,
    url='https://admitad.com/foobarbaz/',
    action_type=0, status=1
)
res = client.ActionOptCodesManager.update(
    desc_mode=1, method=1, action_type=1, status=2
)
```

### Lost orders ###

###### List of lost orders ######

```python
res = client.LostOrders.get()
res = client.LostOrders.get(limit=20, offset=0)
res = client.LostOrders.getOne(76)
```

###### Lost orders manager ######

```python
res = client.LostOrdersManager.create(
    attachments=['/home/user/f.png', '/home/user/s.png'],
    campaign=100, website=10,
    order_id='039NRUHFJEW', order_date='12.08.2016', order_price=345.77,
    comment='some comment'
)
res = client.LostOrdersManager.delete(77)
```

### Arecords ###

###### List of arecords ######

```python
res = client.Arecords.get()
res = client.Arecords.get(limit=50)
res = client.Arecords.getForWebsite(10)
```

### Retag ###

###### List of retag ######

```python
res = client.Retag.get()
res = client.Retag.get(website=10, active=False, limit=50)
res = client.Retag.getOne(54)
res = client.Retag.getLevelsForWebsite(10)
res = client.Retag.getLevelsForCampaign(100)
```

###### Retag manager ######

```python
res = client.RetagManager.create(
    website=10, level=22, active=False,
    script='some js script', comment='some comment'
)
res = client.RetagManager.update(16, level=10, active=True)
res = client.RetagManager.delete(88)
```

### Tickets ###

###### List of tickets ######

```python
res = client.Tickets.get()
res = client.Tickets.get(date_start='01.01.2016', status=0)
res = client.Tickets.getOne(50)
```

###### Ticket manager ######

```python
res = client.TicketsManager.create(
    subject='subject', text='some text',
    campaign=100, category=27, priority=0,
)
res = client.TicketsManager.comment(12, text='some comment')
```

Notes
------

It is possible to override the default response handler by passing handler as
a keyword argument to a client function call. For example:

```python
func = lambda x: (x, x)
result = client.Me.get(handler=func)
```
