import requests

class IEXStock:

    def __init__(self, token, symbol, environment='notproduction'):
        
        if environment == 'production':
            self.BASE_URL = 'https://cloud.iexapis.com/stable'
        else:
            self.BASE_URL = 'https://sandbox.iexapis.com/stable'
        self.token = token
        self.symbol = symbol

    def get_logo(self):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()

    def get_company_info(self):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()
    
    def get_company_news(self, last=10):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()

    def get_stats(self):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/advanced-stats?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()

    def get_fundamentals(self, period='quarterly', last=4):
        api_url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()

    def get_dividends(self, range='5y'):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/dividends/{range}?token={self.token}"
        api_data = requests.get(api_url)

        return api_data.json()

    def get_institutional_ownership(self):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()

    def get_insider_transactions(self):
        api_url = f"{self.BASE_URL}/stock/{self.symbol}/insider-transactions?token={self.token}"
        api_data = requests.get(api_url)
        return api_data.json()        