from google.cloud import storage
import os
import logging
import sys

# Set credentials path (Windows-friendly)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\sachi\Downloads\lateral-spirit-461213-n9-7358aa85b741.json"

RAW_FILE_PATH = "Hotel_Reservations.csv"  # set to your preferred save path

def download_csv_from_gcp(bucket_name, file_name):
    try:
        logging.info(f"Starting download from bucket: {bucket_name}, file: {file_name}")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.download_to_filename(RAW_FILE_PATH)

        logging.info(f"CSV file is successfully downloaded to {RAW_FILE_PATH}")
    except Exception as e:
        logging.error(f"Error while downloading the csv file: {e}")
        raise Exception(f"Failed to download csv file: {e}")

# Example usage
download_csv_from_gcp("my_bucket_6202", "Hotel_Reservations.csv")
