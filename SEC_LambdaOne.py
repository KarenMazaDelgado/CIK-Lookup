import boto3 # Uses boto3library to upload the file to S3
import requests #Uses requests library to fownload the file

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {
        "User-Agent": "Karen Maza karenmaza20300@gmail.com",
        "Accept-Encoding": "gzip, deflate"
    }
    response = requests.get(url, headers=headers)
    
    s3.put_object(
        Bucket='your-bucket-name',
        Key='company_tickers.json',
        Body=response.content
    )
    
    return {"statusCode": 200, "body": "File uploaded to S3"}
