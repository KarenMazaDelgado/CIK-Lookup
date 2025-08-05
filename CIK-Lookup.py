import requests

class CIKLookup:
    def __init__(self):
        url = "https://www.sec.gov/files/company_tickers.json"
        headers = {
            "User-Agent": "Karen Maza karenmaza20300@gmail.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov"
        }

        # Sends HTTP GET request to url using requests Python library
        response = requests.get(url, headers=headers)
        data = response.json() # Converts JSON data from HTTP request to dictionary, keys are numbers value is company name, ticker and cik

        # Create dictionaries
        self.name_dict = {} # Company name is key
        self.ticker_dict = {} # Stock ticker is key

        # Get the data for each company (item is a dictionary and keys are labels like 'cik_str', 'ticker', and 'title' meanwhile values are actual data)
        for item in data.values():
            cik = str(item['cik_str']).zfill(10)  # Zero-pad to 10 digits
            name = item['title'].upper()
            ticker = item['ticker'].upper()


            record = (cik, name, ticker) # e.g. ('0000320193', 'APPLE INC.', 'AAPL')


            self.name_dict[name] = record # e.g. Key: 'APPLE INC.' VALUE: ('0000320193', 'APPLE INC.', 'AAPL')

            self.ticker_dict[ticker] = record # e.g. Key: 'AAPL.' VALUE: ('0000320193', 'APPLE INC.', 'AAPL')

    def name_to_cik(self, name):
        return self.name_dict.get(name.upper(), None) # If key exists get value, otherwise return None

    def ticker_to_cik(self, ticker):
        return self.ticker_dict.get(ticker.upper(), None)