import json
from CIK_Lookup import CIKLookup # import helper module

def lambda_handler(event, context):

    # Get correspondig event keys
    request_type = event['request_type'] # Either annual or quarter
    company = event['company']
    year = event['year']
    
    cik_lookup = CIKLookup() # Create instance of helper class
    cik_record = cik_lookup.name_to_cik(company) # Uses helper module to convert company name to CIK eg. "Apple Inc." -> "0000320193" 
    if not cik_record: # Handles if compay is not found
        return {"statusCode": 404, "body": json.dumps({"error": "Company not found"})}
    
    cik = cik_record[0] # name_to_cik returs list of matches
    
    if request_type == 'Annual':
        document = cik_lookup.annual_filing(cik, year)
    elif request_type == 'Quarter':
        quarter = event['quarter']
        document = cik_lookup.quarterly_filing(cik, year, quarter)
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid request type"})}
    
    return {"statusCode": 200, "body": json.dumps(document)}
