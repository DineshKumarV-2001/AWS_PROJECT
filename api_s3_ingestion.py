import json
import os
import boto3
import requests

# 1. Configuration
API_URL = "https://dummyjson.com/products?limit=50"
BUCKET_NAME = "my-ecom-aws-etl-project"
S3_KEY = "bronze/api-data/raw_products.json"

# 2. Define local folder and file path
LOCAL_DIR = "./data"
LOCAL_FILE = os.path.join(LOCAL_DIR, "raw_products.json")
os.makedirs(LOCAL_DIR, exist_ok=True)

# 3. Fetching Data from the API
print("Fetching Data From API...")
try:
  response = requests.get(API_URL)

  if response.status_code == 200:
    data = response.json()

    # 4. Saving Data Locally
    with open(LOCAL_FILE, "w") as f:
      json.dump(data, f, indent=2)
    print(f"File Saved Successfully to {LOCAL_FILE}")

    # 5. Upload to S3
    print("Uploading Data to AWS S3 Bronze Bucket...")
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
    print(f"Successfully uploaded raw API data to s3://{BUCKET_NAME}/{S3_KEY}")

  else:
    print(f"API returned non-200 status code: {response.status_code}")

except Exception as e:
  print(f"An error occurred during execution: {e}")
