import time
import streamlit as st
import requests, redis
import config, json

from iex import IEXStock
from helpers import format_number
from recoModule import recoClass

from datetime import datetime, timedelta

st.title("Stock Screener")

symbol = st.sidebar.text_input("Symbol", value='MSFT')

stock = IEXStock(config.IEX_API_KEY, symbol)
reco = recoClass()

client = redis.Redis(host="localhost", port=6379)

screen = st.sidebar.selectbox("View", ('Overview', 'Fundamentals', 'Technicals', 'Recent News', 'Share Holding Pattern', 'Recommendation'), index=0)

st.sidebar.info("The information provided on this site does not, and is not intended to, constitute investment advice; instead, all information, content, and materials available on this site are general purposes only. Content on this website may not constitute the most up-to-date information. The material is neither investment research, nor investment advice.")

st.title(screen)

if screen == 'Overview':
    logo_cache_key = f"{symbol}_logo"
    cached_logo = client.get(logo_cache_key)

    if cached_logo is not None:
        print("found logo in cache")
        logo = json.loads(cached_logo)
    else:
        print("getting logo from api, and then storing it in cache")
        logo = stock.get_logo()
        client.set(logo_cache_key, json.dumps(logo))
        client.expire(logo_cache_key, timedelta(hours=24))
    
    company_cache_key = f"{symbol}_company"
    cached_company_info = client.get(company_cache_key)

    if cached_company_info is not None:
        print("found company news in cache")
        company = json.loads(cached_company_info)
    else:
        print("getting company from api, and then storing it in cache")
        company = stock.get_company_info()
        client.set(company_cache_key, json.dumps(company))
        client.expire(company_cache_key, timedelta(hours=24))

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("https://storage.googleapis.com/iexcloud-hl37opg/api/logos/IBM.png")
        # st.image(logo["url"])
        

    with col2:
        st.subheader(company['companyName'])
        st.write(company['industry'] + " ➡️ " + company['sector'])
        st.subheader('Description')
        st.write(company['description'])
        st.subheader('CEO')
        st.write(company['CEO'])

if screen == 'Recent News':
    st.warning("NOTE: Since API in test-mode doesnot provide news data. This feature mught not work!!")
    news_cache_key = f"{symbol}_news"

    news = client.get(news_cache_key)

    if news is not None:
        news = json.loads(news)
    else:
        news = stock.get_company_news()
        client.set(news_cache_key, json.dumps(news))

    for article in news:
        st.subheader(article['headline'])
        dt = datetime.utcfromtimestamp(article['datetime']/1000).isoformat()
        st.write(f"Posted by {article['source']} at {dt}")
        st.write(article['url'])
        st.write(article['summary'])
        st.image(article['image'])

if screen == 'Fundamentals':
    stats_cache_key = f"{symbol}_stats"
    stats = client.get(stats_cache_key)
    
    if stats is None:
        stats = stock.get_stats()
        client.set(stats_cache_key, json.dumps(stats))
    else:
        stats = json.loads(stats)

    st.header('Ratios')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('P/E')
        st.write(stats['peRatio'])
        st.subheader('Forward P/E')
        st.write(stats['forwardPERatio'])
        st.subheader('PEG Ratio')
        st.write(stats['pegRatio'])
        st.subheader('Price to Sales')
        st.write(stats['priceToSales'])
        st.subheader('Price to Book')
        st.write(stats['priceToBook'])
    with col2:
        st.subheader('Revenue')
        st.write(format_number(stats['revenue']))
        st.subheader('Cash')
        st.write(format_number(stats['totalCash']))
        st.subheader('Debt')
        st.write(format_number(stats['currentDebt']))
        st.subheader('200 Day Moving Average')
        st.write(stats['day200MovingAvg'])
        st.subheader('50 Day Moving Average')
        st.write(stats['day50MovingAvg'])

    fundamentals_cache_key = f"{symbol}_fundamentals"
    fundamentals = client.get(fundamentals_cache_key)

    if fundamentals is None:
        fundamentals = stock.get_fundamentals('quarterly')
        client.set(fundamentals_cache_key, json.dumps(fundamentals))
    else:
        fundamentals = json.loads(fundamentals)

    with col1:
        st.header("Quarterly Results")
        for quarter in fundamentals:
            st.subheader(f"Q{quarter['fiscalQuarter']} {quarter['fiscalYear']}")
            st.caption('Filing Date')
            st.write(quarter['filingDate'])
            st.caption('Revenue')
            st.write(format_number(quarter['revenue']))
            st.caption('Net Income')
            st.write(format_number(quarter['incomeNet']))

    with col2:
        st.header("Dividends")

        dividends_cache_key = f"{symbol}_dividends"
        dividends = client.get(dividends_cache_key)

        if dividends is None:
            dividends = stock.get_dividends()
            client.set(dividends_cache_key, json.dumps(dividends))
        else:
            dividends = json.loads(dividends)

        for dividend in dividends:
            st.write(dividend['paymentDate'])
            st.write(dividend['amount'])

if screen == 'Share Holding Pattern':
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Institutional Ownership")

        institutional_ownership_cache_key = f"{symbol}_institutional"
        institutional_ownership = client.get(institutional_ownership_cache_key)

        if institutional_ownership is None:
            institutional_ownership = stock.get_institutional_ownership()
            client.set(institutional_ownership_cache_key, json.dumps(institutional_ownership))
        else:
            print("getting inst ownership from cache")
            institutional_ownership = json.loads(institutional_ownership)
        
        for institution in institutional_ownership:
            st.write(institution['date'])
            st.write(institution['entityProperName'])
            st.write(institution['reportedHolding'])

    with col2:
        st.subheader("Insider Transactions")

        insider_transactions_cache_key = f"{symbol}_insider_transactions"

        insider_transactions = client.get(insider_transactions_cache_key)
        if insider_transactions is None:
            insider_transactions = stock.get_insider_transactions()
            client.set(insider_transactions_cache_key, json.dumps(insider_transactions))
        else:
            print("getting insider transactions from cache")
            insider_transactions = json.loads(insider_transactions)
        
        for transaction in insider_transactions:
            st.write(transaction['filingDate'])
            st.write(transaction['fullName'])
            st.write(transaction['transactionShares'])
            st.write(transaction['transactionPrice'])
        
if screen == 'Recommendation':
    
    def funcmain():
        aum = st.text_input("Enter the total value for AUM - used for providing recommendation", help="Don't use currency symbol only int/float")
        aum = (aum,)
        
        # def getrecoqms(arg1):
        #     # subprocess.run([f"{sys.executable}", "quantitativeMomentumStrategy.py"])
        #     os.system("python quantitativeMomentumStrategy.py --counter" + arg1)
        
        # def getrecoewi(arg1):
        #     os.system("python equalWeightIndex.py --counter" + arg1)

        # st.button("GET RECO QMS",help="Quantitative Momentum Strategy", on_click= getrecoqms, args=aum)
        # st.button("GET RECO EWI",help="Equal Weight Index", on_click= getrecoewi, args=aum)

        # st.write("returns a portfolio of companies having best momentum in recent past")
        st.button("GET RECO QMS",help="Quantitative Momentum Strategy", on_click= callfuncqms, args=aum)
        # st.write("returns no of stocks to buy for each company to have an equal weight portfolio")
        st.button("GET RECO EWI",help="Equal Weight Index", on_click= callfunc, args=aum)
    
    def callfuncqms(aum):
        def getrecoqms(aum):
            with st.spinner('Processing necessory data...'):
                time.sleep(10)
            stock_dataframe = reco.qmsfunc(aum)
            st.dataframe(stock_dataframe)
        getrecoqms(aum)    

    def callfunc(aum):
        def getrecoewi(aum):
            with st.spinner('Processing necessory data...'):
                time.sleep(10)
            stock_dataframe = reco.ewifunc(aum)
            st.dataframe(stock_dataframe)
        getrecoewi(aum)

    funcmain()

if screen == 'Technicals':
    st.info("N0_DATA ERROR")
# ***** footer *****

footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: grey;
color: black;
text-align: center;
}
</style>

<div class="footer">
<p>Made with ❤️ ﹠ 📈 by Priyam</p>
<p>(Random data is used for test purposes) 
</div>"""
st.markdown(footer,unsafe_allow_html=True)

