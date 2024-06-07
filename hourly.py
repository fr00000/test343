import requests
import logging
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import schedule

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://d2hfhz0c37x28y.cloudfront.net/prod/stats?minerId={}"

def get_points(session, wallet_address):
    try:
        response = session.get(URL.format(wallet_address))
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        # Ensure all keys exist in the data dictionary, default to 0 if not found
        llama_points = data.get("totalLlamaPoints", 0)
        waifu_points = data.get("totalWaifuPoints", 0)
        text_count = data.get("totalTextCount", 0)
        image_count = data.get("totalImageCount", 0)
        return llama_points, waifu_points, text_count, image_count
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get points for {wallet_address}: {e}")
        return 0, 0, 0, 0

def calculate_total_points(addresses):
    total_llama_points = 0
    total_waifu_points = 0
    total_text_count = 0
    total_image_count = 0
    unique_addresses = list(set(addresses))

    with requests.Session() as session, ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_points, session, address) for address in unique_addresses]
        for future in tqdm(futures, desc="Processing addresses", unit="address"):
            result = future.result()
            if result:
                llama_points, waifu_points, text_count, image_count = result
                if llama_points is not None:
                    total_llama_points += llama_points
                if waifu_points is not None:
                    total_waifu_points += waifu_points
                if text_count is not None:
                    total_text_count += text_count
                if image_count is not None:
                    total_image_count += image_count
            else:
                logging.error("Received None result for a future, expected tuple of points and counts.")
                # Optionally, initialize to zero if None to avoid breaking the sum calculations
                llama_points, waifu_points, text_count, image_count = 0, 0, 0, 0

    return total_llama_points, total_waifu_points, total_text_count, total_image_count

def read_wallet_addresses_from_file(file_path):
    with open(file_path, 'r') as file:
        addresses = file.read().splitlines()
    return addresses

def job():
    wallet_file_path = '.wal'
    wallet_addresses = read_wallet_addresses_from_file(wallet_file_path)

    current_llama, current_waifu, current_text, current_image = calculate_total_points(wallet_addresses)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Timestamp: {timestamp}")
    print(f"Current Llama Points: {current_llama}")
    print(f"Current Waifu Points: {current_waifu}")
    print(f"Current Text Count: {current_text}")
    print(f"Current Image Count: {current_image}")

    global total_llama, total_waifu, total_text, total_image
    if total_llama == 0 and total_waifu == 0:
        hourly_llama, hourly_waifu, hourly_text, hourly_image ,daily_waifu ,daily_llama = 0, 0, 0, 0, 0, 0
    else:     
        hourly_llama = current_llama - total_llama
        hourly_waifu = current_waifu - total_waifu
        hourly_text = current_text - total_text
        hourly_image = current_image - total_image
        daily_waifu = hourly_waifu * 24
        daily_llama = hourly_llama * 24
     

    total_llama = current_llama
    total_waifu = current_waifu
    total_text = current_text
    total_image = current_image

    print(f"Hourly Llama Points: {hourly_llama} (Daily: {daily_llama})")
    print(f"Hourly Waifu Points: {hourly_waifu} (Daily: {daily_waifu})")
    print(f"Hourly Text Count: {hourly_text}")
    print(f"Hourly Image Count: {hourly_image}")
    print("---")

total_llama = 0
total_waifu = 0
total_text = 0
total_image = 0

schedule.every().hour.at(":00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
