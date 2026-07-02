import boto3
from pathlib import Path

BUCKET_NAME = "elt-warehouse-raw-zaynah"   # replace with your bucket name

RAW_DATA_DIR = Path("data/raw")

s3 = boto3.client("s3")


def upload_file(filename):
    file_path = RAW_DATA_DIR / filename

    s3.upload_file(
        str(file_path),
        BUCKET_NAME,
        filename
    )

    print(f"Uploaded {filename} to S3")

if __name__ == "__main__":
    upload_file("products.json")
    upload_file("users.json")
    upload_file("carts.json")