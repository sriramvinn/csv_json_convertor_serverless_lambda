import boto3
import pandas as pd
import json
from io import StringIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Download the CSV file from S3
    response = s3.get_object(Bucket=bucket, Key=file_key)
    csv_content = response['Body'].read().decode('utf-8')
    
    # Read the CSV file using pandas
    df = pd.read_csv(StringIO(csv_content))
    
    # Calculate the average of number1 and number2 columns
    df['average'] = (df['number1'] + df['number2']) / 2
    
    # Convert the DataFrame to JSON
    json_content = df.to_json(orient='records')
    
    # Save the JSON file to S3
    s3.put_object(Body=json_content, Bucket=bucket, Key=file_key.replace('.csv', '.json'))
    
    return {
        'statusCode': 200,
        'body': 'CSV to JSON conversion successful'
    }
