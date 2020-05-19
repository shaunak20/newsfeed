from django.shortcuts import render
import bs4
import requests
from newsapi import NewsApiClient
from .models import *
from datetime import date,datetime,timedelta
import re
from forex_python.converter import CurrencyRates
import yfinance as yf
import pandas_market_calendars as mcal
import investpy


# Create your views here.
def index(request):
    n=""
    price=0.0
    pnl=0.0
    pnlper=0.0

    n2=""
    price2=0.0
    pnl2=0.0
    pnlper2=0.0

    # FX Live Data
    res=requests.get('https://finance.yahoo.com/currencies')
    soup=bs4.BeautifulSoup(res.text,"lxml")
    tables=soup.select('table')
    for row in tables[0].find_all('tr'):
        for ch in row.find_all('td')[1:2]:
            if((ch.text=='EUR/USD') | (ch.text=='EUR/GBP')| (ch.text=='USD/JPY')| (ch.text=='AUD/USD')| (ch.text=='USD/CNY')| (ch.text=='GBP/USD')):
                for cell in row.find_all('td')[1:2]:
                    n=cell.text
                for cell in row.find_all('td')[2:3]:
                    price=cell.text
                for cell in row.find_all('td')[3:4]:
                    pnl=cell.text
                for cell in row.find_all('td')[4:5]:
                    pnlper=cell.text
                    pnlper=float(pnlper[:len(pnlper)-1])

                a = currency(name=n,price=price,pnl=pnl,pnlper=pnlper)
                a.save()

    query_results1= currency.objects.all().order_by('-id')[:6]





    # FX News

    head3=[]
    head4=[]
    imglink3=[]
    pairs=[]
    context=[]

    res2=requests.get('https://www.fxstreet.com/news?q=&hPP=17&idx=FxsIndexPro&p=0&dFR%5BTags%5D%5B0%5D=EURUSD&dFR%5BTags%5D%5B1%5D=GBPUSD')
    soup=bs4.BeautifulSoup(res2.text,"lxml")
    link=soup.find_all("div",{"class":"fxs_col editorialhighlight editorialhighlight_medium"})
    if((link[0].h3.a.text).find('/')>0):
        head3.append(link[0].h3.a.text)
        context.append(link[0].div.p.text)
        imglink3.append(link[0].div.a.img['data-src'])

    if((link[1].h3.a.text).find('/')>0):
        head3.append(link[1].h3.a.text)
        context.append(link[1].div.p.text)
        imglink3.append(link[1].div.a.img['data-src'])

    #Other headlines
    res5=requests.get('https://www.dailyfx.com/market-news')
    soup5=bs4.BeautifulSoup(res5.text,"lxml")
    link5=soup5.find_all("a",{"class":"dfx-articleListItem jsdfx-articleListItem d-flex mb-3"})
    for i in range(len(link5)):
        if((len(link5[i].span.text)<73)&((link5[i].span.text).find('/')>=0)&((link5[i].span.text).find('?')<0)&((link5[i].span.text).find('Charts')<0)):
            head4.append(link5[i].span.text)
            # Removing duplicates
    head4 = list(dict.fromkeys(head4))
    head4=head4[len(head4)-4:len(head4)];

    img_url_fx = ['https://currencylive.com/news/wp-content/uploads/2019/08/100859-gbp-usd-pound-rises-may-brussels.jpg','https://responsive.fxempire.com/cover/1845x1230/webp-lossy-70.q50/_fxempire_/2020/01/Pounds-British.jpg','https://images.newindianexpress.com/uploads/user/imagelibrary/2019/9/25/w900X450/australian-2874029_960_720.jpg','https://responsive.fxempire.com/cover/1845x1230/webp-lossy-70.q50/_fxempire_/2019/11/US-Dollars-Yen-Notes.jpg']
    for i in range(len(head4)):
        g = fxnews(headline=head4[i],imgurl=img_url_fx[i])
        g.save()

    query_results6= fxnews.objects.all().order_by('-id')[:4]


    for i in range(len(head3)):
        if(head3[i].find('/')>0):
            arr=head3[i].split('/')
            first=(arr[0])[len(arr[0])-3:len(arr[0])]
            second=arr[1][0:3]
            pairs.append(first+'/'+second)

    for i in range(len(head4)):
        if(head4[i].find('/')>0):
            arr=head4[i].split('/')
            first=(arr[0])[len(arr[0])-3:len(arr[0])]
            second=arr[1][0:3]
            pairs.append(first+'/'+second)

    pairs[0].split('/')
    first=((pairs[0].split('/'))[0])[:3]
    second=((pairs[0].split('/'))[1])[0:3]
    pair1=first+'/'+second

    pairs[0].split('/')
    third=((pairs[1].split('/'))[0])[:3]
    fourth=((pairs[1].split('/'))[1])[0:3]
    pair2=third+'/'+fourth

    imglink3=imglink3[0]
    fxcenter=head3[0]
    context=context[0]






    #Currency Graph
    start_date=date.today()
    end_date=start_date-timedelta(days=21)
    rates=[]
    forexdates=[]
    rates2=[]
    forexdates2=[]
    before=0.0
    before2=0.0
    c = CurrencyRates()
    for i in range(0,21):
        new=c.get_rate(first,second,end_date)
        if(before!=new):
            rates.append(new)
            forexdates.append(end_date.strftime("%Y-%m-%d"))
        before=new
        end_date=end_date+timedelta(days=1)


    end_date=start_date-timedelta(days=21)
    for i in range(0,21):
        new=c.get_rate(third,fourth,end_date)
        if(before2!=new):
            rates2.append(new)
            forexdates2.append(end_date.strftime("%Y-%m-%d"))
        before2=new
        end_date=end_date+timedelta(days=1)


    #Index data
    res3=requests.get('https://finance.yahoo.com/world-indices')
    soup=bs4.BeautifulSoup(res3.text,"lxml")
    tables2=soup.select('table')

    for row in tables2[0].find_all('tr'):
        for ch in row.find_all('td')[1:2]:
            if((ch.text=='S&P 500') | (ch.text=='Dow Jones Industrial Average')| (ch.text=='NASDAQ Composite')| (ch.text=='HANG SENG INDEX')| (ch.text=='Nikkei 225')| (ch.text=='S&P BSE SENSEX')):
                for cell in row.find_all('td')[1:2]:
                    if(ch.text=='Dow Jones Industrial Average'):
                            n2='Dow Jones'
                    elif(ch.text=='S&P BSE SENSEX'):
                            n2='BSE SENSEX'
                    else:
                        n2=cell.text
                for cell in row.find_all('td')[2:3]:
                    price2=cell.text
                for cell in row.find_all('td')[3:4]:
                    pnl2=cell.text
                for cell in row.find_all('td')[4:5]:
                    pnlper2=cell.text
                    pnlper2=float(pnlper2[:len(pnlper2)-1])
                b = indexes(name=n2,price=price2,pnl=pnl2,pnlper=pnlper2)
                b.save()

    query_results2= indexes.objects.all().order_by('-id')[:6]





    # Index Graph

    #Dow Graph
    end=date.today()
    start=(end-timedelta(days=21))
    end=end.strftime('%d/%m/%Y')
    start=start.strftime('%d/%m/%Y')
    dataframe2=investpy.get_index_historical_data(index='Dow 30', country='united states', from_date=start, to_date=end)
    dprice=(round(dataframe2['Close'],3))
    dow=list((round(dataframe2['Close'],3)))

    dumvar2=dprice.index
    dates=[]
    for i in range(len(dprice)):
        dates.append(dumvar2[i].strftime('%d-%m-%Y'))



    #BSE Sensex graph
    end2=date.today()
    start2=(end2-timedelta(days=21))
    end2=end2.strftime('%d/%m/%Y')
    start2=start2.strftime('%d/%m/%Y')
    dataframe=investpy.get_index_historical_data(index='BSE Sensex', country='india', from_date=start2, to_date=end2)
    dprice2=(round(dataframe['Close'],3))
    bse=list((round(dataframe['Close'],3)))

    dumvar=dprice2.index
    bsedates=[]
    for i in range(len(dprice2)):
        bsedates.append(dumvar[i].strftime('%d-%m-%Y'))


    #Index News
    index_title=[]
    index_description=[]
    index_imgurl=[]
    newsapi = NewsApiClient(api_key = '3de8090563454aadbd116bb099718ded')
    string = ['Nifty', 'Sensex', 'S&P', 'Dow']
    y = re.compile('<[^>]+>')
    x = date.today()
    z = x
    x = x-timedelta(days=1)
    for i in string:
        if i == 'Sensex' or i == 'Nifty':
            start_date = z
        else:
            start_date = x
        all_articles = newsapi.get_everything(q = i, from_param = start_date.strftime("%Y-%m-%d"), language = "en", sort_by = "relevancy", page_size = 5)
        articles = all_articles['articles']
        for j in range(2):
            if ((articles[j]['title'] not in index_title) &(articles[j]['title'].find('?')==-1)) :
                index_title.append(articles[j]['title'])
                index_description.append(y.sub('', articles[j]['description']))
                index_imgurl.append(articles[j]['urlToImage'])
            else:
                pass
    for i in range(1,5):
        if index_imgurl[i] != None and index_title[i] != None and index_description[i] != None:
            f=stocknews(headline=index_title[i],imgurl=index_imgurl[i])
            f.save()

    index_centertitle=index_title[0]
    index_centerdescription=index_description[0]
    index_centerimgurl=index_imgurl[0]

    query_results3= stocknews.objects.all().order_by('-id')[:4]



    #Equities Graph

    end=date.today()
    start=end-timedelta(days=7)
    diff=[]
    aapl=yf.download("AAPL",start, end)
    nflx=yf.download("NFLX",start, end)
    msft=yf.download("MSFT",start, end)
    amzn=yf.download("AMZN",start, end)
    tsla=yf.download("TSLA",start, end)
    fb=yf.download("FB",start, end)

    comp=[aapl,nflx,msft,amzn,tsla,fb]
    for i in comp:
        dprice=(round(i['Close'],3))
        diff.append(round(dprice[-1]-dprice[-2],3))

    # Indian Equities
    end3=date.today()
    start3=end3-timedelta(days=7)
    diff3=[]
    end3=end3.strftime('%d/%m/%Y')
    start3=start3.strftime('%d/%m/%Y')
    tcs=investpy.get_stock_historical_data(stock='TCS', country='india', from_date=start3, to_date=end3)
    icbk=investpy.get_stock_historical_data(stock='ICBK', country='india', from_date=start3, to_date=end3)
    hdbk=investpy.get_stock_historical_data(stock='HDBK', country='india', from_date=start3, to_date=end3)
    infy=investpy.get_stock_historical_data(stock='INFY', country='india', from_date=start3, to_date=end3)
    lart=investpy.get_stock_historical_data(stock='LART', country='india', from_date=start3, to_date=end3)
    reli=investpy.get_stock_historical_data(stock='RELI', country='india', from_date=start3, to_date=end3)

    comp2=[tcs,icbk,hdbk,infy,lart,reli]
    for i in comp2:
        ghe=(round(i['Close'],3))
        diff3.append(round(ghe[-1]-ghe[-2],3))


    #Equities data

    res4=requests.get('https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/')
    soup4=bs4.BeautifulSoup(res4.text,"lxml")
    tables4=soup4.select('table')

    rows4=tables4[0].find_all('tr')
    for i in range(1,50):
        cells4=rows4[i].find_all('td')
        name4=cells4[0].div.a.text
        price4=cells4[1].text
        pnlper4=cells4[2].text
        pnl4=cells4[3].text
        pnlper4=float(pnlper4[:len(pnlper4)-1])

        if((name4=='AAPL')|(name4=='MSFT')|(name4=='NFLX')|(name4=='AMZN')|(name4=='FB')|(name4=='TSLA')):
            d = equities(name=name4,price=price4,pnl=pnl4,pnlper=pnlper4)
            d.save()

    query_results4= equities.objects.all().order_by('-id')[:6]


    streq = ["Trending stocks"]
    headeq=[]
    imgurleq=[]
    for j in range(len(streq)):
        top_headlineseq = newsapi.get_everything(q=streq[j],
                                                   from_param=(date.today()-timedelta(days=1)).strftime('%Y-%m-%d'),
                                                   sort_by='relevancy',
                                                    language='en',
                                                )

        articleseq = top_headlineseq['articles']
        for i in range(len(articleseq)):
            if(articleseq[i]['title'].find('Trending stocks')!=-1):
                e = eqnews(headline=articleseq[i]['title'],imgurl=articleseq[i]['urlToImage'])
                e.save()


    query_results5= eqnews.objects.all().order_by('-id')[:4]

    # newsapi = NewsApiClient(api_key='082157f2d57c4560878f51cc05ace5ea')

    streq2 = ["Trending stocks"]
    for j in range(len(streq2)):
        top_headlineseq2 = newsapi.get_everything(q=streq2[j],
                                                   from_param=(date.today()-timedelta(days=1)).strftime('%Y-%m-%d'),
                                                   sort_by='relevancy',
                                                    language='en',
                                                )

        articleseq2 = top_headlineseq2['articles']
        title_center_eq = articleseq2[1]['title']
        imgURL_center_eq = articleseq2[1]['urlToImage']
        desc_center_eq = articleseq2[1]['description']
        desc_center_eq = desc_center_eq.split(".")
        desc_center_eq=desc_center_eq[0]




    return render(request, 'news/index.html',{'query_results1':query_results1,'query_results2':query_results2,'query_results3':query_results3,'query_results4':query_results4,'query_results5':query_results5,'query_results6':query_results6,'fxcenter':fxcenter,'head3':head3,'head4':head4,'context':context,'imglink3':imglink3,'pairs':pairs,'dow':dow,'dates':dates,'rates':rates,'forexdates':forexdates,'pair1':pair1,'rates2':rates2,'forexdates2':forexdates2,'pair2':pair2,'diff':diff,'bse':bse,'bsedates':bsedates,'diff3':diff3,'headeq':headeq,'imgurleq':imgurleq,'index_centertitle':index_centertitle,'index_centerdescription':index_centerdescription,'index_centerimgurl':index_centerimgurl,'title_center_eq':title_center_eq,'imgURL_center_eq':imgURL_center_eq,'desc_center_eq':desc_center_eq,'img_url_fx':img_url_fx})
