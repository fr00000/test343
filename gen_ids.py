import os
import random
import string

NUM_ADDRESSES = 20
TOTAL_MINER_IDS = 120
wallet_file = '.wal'
ids_file = '.ids'
env_file = '.env'

def generate_miner_id(address):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{address}-{random_string}"

def read_addresses_from_file(file_path, num_addresses):
    with open(file_path, 'r') as file:
        addresses = [next(file).strip() for _ in range(num_addresses)]
    return addresses

def create_and_save_miner_ids(addresses, total_miner_ids, ids_file, env_file):
    miner_ids = []

    for address in addresses:
        miner_id = generate_miner_id(address)
        miner_ids.append(miner_id)

    remaining_miner_ids = total_miner_ids - len(addresses)
    for _ in range(remaining_miner_ids):
        address = random.choice(addresses)
        miner_id = generate_miner_id(address)
        miner_ids.append(miner_id)

    with open(ids_file, 'w') as file:
        for miner_id in miner_ids:
            file.write(miner_id + '\n')

    with open(env_file, 'w') as file:
        for i, address in enumerate(addresses):
            file.write(f"MINER_ID_{i}={address}\n")

if os.path.exists(ids_file) or os.path.exists(env_file):
    print(f"One or both output files already exist. Exiting the program.")
    exit()

eth_addresses = read_addresses_from_file(wallet_file, NUM_ADDRESSES)

create_and_save_miner_ids(eth_addresses, TOTAL_MINER_IDS, ids_file, env_file)

print(f"Miner IDs saved to {ids_file} and {env_file}")
