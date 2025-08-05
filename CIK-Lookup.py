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
    
    # Get subsmissions from JSON data 
    def get_submissions(cik):
        cik = str(cik).zfill(10) # Make sure the CIK num has leading zeros with 10 total digits
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        headers = {
            "User-Agent": "Karen Maza karenmaza20300@gmail.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "data.sec.gov"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    # Build the URL to the HTML filing document
    def build_filing_url(cik, accession, document):
        cik = str(int(cik))  # strip leading zeros
        accession = accession.replace("-", "")
        return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
    
    
    # Look for latest 10-K given the year
    def annual_filing(cik, year):
        data = get_submissions(cik)
        filings = data["filings"]["recent"] # Isolate recent section from JSON

        # Index is important because lists are parallel (tabular data) where for ex, 0th form goes with 0th filingData, 0th accessionNumber and 0th primaryDocument, like pulling data from the same row(i) across different columns
        for i, form_type in enumerate(filings["form"]): # Get both the index and the form type string in filings["form"]
            if form_type == "10-K":
                filing_year = filings["filingDate"][i][:4] # Get filing date for the same index and take first 4 characters (year)
                if filing_year == str(year):
                    accession = filings["accessionNumber"][i]
                    document = filings["primaryDocument"][i]
                    filing_date = filings["filingDate"][i]
                    url = build_filing_url(cik, accession, document) # Create url
                    return {
                        "accession": accession,
                        "filing_date": filing_date,
                        "url": url,
                        "document": document
                    }
        return None  # If no 10-K found for that year
    
    # Look for 10-Q filing for specific quarter of the year
    def quarterly_filing(cik, year, quarter):
        data = get_submissions(cik)
        filings = data["filings"]["recent"]

        #Dictionary that maps quarters (1-4) to their start and end dates within a given year
        q_ranges = {
            1: ("01-01", "03-31"),
            2: ("04-01", "06-30"),
            3: ("07-01", "09-30"),
            4: ("10-01", "12-31")   #Key : quarter and Value : start,end dates
        }

        start, end = q_ranges[quarter]
        start_date = f"{year}-{start}"   # e.g., "2024-01-01"
        end_date = f"{year}-{end}"       # e.g., "2024-03-31"

        for i, form_type in enumerate(filings["form"]):
            if form_type == "10-Q":
                date = filings["filingDate"][i]
                if start_date <= date <= end_date: # Filters filings by which quarter they were submitted in
                    accession = filings["accessionNumber"][i]
                    document = filings["primaryDocument"][i]
                    url = build_filing_url(cik, accession, document)
                    return {
                        "accession": accession,
                        "filing_date": date,
                        "url": url,
                        "document": document
                    }
        return None  # If no 10-Q found in that quarter
