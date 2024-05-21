import requests
import logging
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://d2hfhz0c37x28y.cloudfront.net/prod/stats?minerId={}"

def get_points(session, wallet_address):
    try:
        response = session.get(URL.format(wallet_address))
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        return data["totalLlamaPoints"], data["totalWaifuPoints"], data["totalTextCount"], data["totalImageCount"]
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

wallet_file_path = 'wal.txt'
wallet_addresses = read_wallet_addresses_from_file(wallet_file_path)

total_llama, total_waifu, total_text, total_image = calculate_total_points(wallet_addresses)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"Timestamp: {timestamp}")
print(f"Total Llama Points: {total_llama}")
print(f"Total Waifu Points: {total_waifu}")
print(f"Total Text Count: {total_text}")
print(f"Total Image Count: {total_image}")
