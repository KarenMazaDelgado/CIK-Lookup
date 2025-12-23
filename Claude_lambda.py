import json
import boto3
from CIK_Lookup import CIKLookup  # import  helper module

s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

BUCKET_NAME = "sec-tickers"  

def lambda_handler(event, context):
    question = event.get("question")
    company = event.get("company")  
    year = event.get("year")
    request_type = event.get("request_type", "Annual")  # default Annual (10-K) or Quarter (10-Q)
    quarter = event.get("quarter")  # needed if request_type == Quarter

    if not all([question, company, year]):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing question, company, or year"})
        }

    try:
        cik_lookup = CIKLookup()
        cik_record = cik_lookup.name_to_cik(company)
        if not cik_record:
            return {"statusCode": 404, "body": json.dumps({"error": "Company not found"})}
        cik = cik_record[0]

        if request_type == "Annual":
            document_info = cik_lookup.annual_filing(cik, year)
        elif request_type == "Quarter":
            if not quarter:
                return {"statusCode": 400, "body": json.dumps({"error": "Missing quarter for quarterly filing"})}
            document_info = cik_lookup.quarterly_filing(cik, year, quarter)
   
        if document_info and "url" in document_info:
            # Automated document ingestion
            # uses your new helper method to grab the actual text from the SEC
            document_text = cik_lookup.get_filing_content(document_info["url"])
        else:
            return {"statusCode": 404, "body": json.dumps({"error": "Filing URL not found"})}
        
        if not document_text:
            return {"statusCode": 500, "body": json.dumps({"error": "Failed to ingest document text"})}
        
        # document_info should contain the S3 key or path to the filing
        # Let's assume document_info contains the S3 key for the file you want

        # s3_key = document_info.get("s3_key") 

        # # Fallback: If CIKLookup returns raw text instead of path, adjust accordingly
        # if not s3_key:
        #     # Maybe document_info is the document text directly
        #     document_text = document_info.get("text") or document_info
        # else:
        #     obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        #     document_text = obj['Body'].read().decode('utf-8')

        prompt = (
            f"You are a financial analyst. Use the following SEC filing "
            f"for {company} in {year} to answer the question.\n\n"
            f"--- SEC Filing Start ---\n"
            f"{document_text[:15000]}\n"
            f"--- SEC Filing End ---\n\n"
            f"Question: {question}"
        )

        messages = [{"role": "user", "content": prompt}]
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages
        }

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())
        generated_text = ''.join(
            block.get('text', '') for block in response_body.get('content', [])
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": generated_text,
                "source_s3_key": s3_key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
