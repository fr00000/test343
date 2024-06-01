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

def read_existing_miner_ids(ids_file):
    if os.path.exists(ids_file):
        with open(ids_file, 'r') as file:
            miner_ids = [line.strip() for line in file]
        return miner_ids
    return []

def create_and_save_miner_ids(addresses, total_miner_ids, ids_file, env_file, existing_miner_ids):
    miner_ids = existing_miner_ids

    # Ensure each address has at least one miner ID
    for address in addresses:
        if not any(miner_id.startswith(address) for miner_id in miner_ids):
            miner_id = generate_miner_id(address)
            miner_ids.append(miner_id)

    remaining_miner_ids = total_miner_ids - len(miner_ids)
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

eth_addresses = read_addresses_from_file(wallet_file, NUM_ADDRESSES)
existing_miner_ids = read_existing_miner_ids(ids_file)

create_and_save_miner_ids(eth_addresses, TOTAL_MINER_IDS, ids_file, env_file, existing_miner_ids)

print(f"Miner IDs saved to {ids_file} and {env_file}")
