import yaml
import csv

def update_wallet_yaml(csv_file='wallets.csv', yaml_file='wallet_address.yaml'):
    """
    Update wallet_address.yaml with addresses from generated wallets CSV file
    
    :param csv_file: Path to the CSV file containing wallet information
    :param yaml_file: Path to the YAML file to update
    """
    # Read existing wallet addresses from YAML if it exists
    existing_wallets = []
    existing_addresses = set()  # 기존 지갑 주소 저장용 set
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data and isinstance(yaml_data, dict) and 'wallets' in yaml_data:
                existing_wallets = yaml_data['wallets']
                # 기존 지갑 주소들을 set에 추가
                existing_addresses = {w['wallet_address'].lower() for w in existing_wallets}
    except FileNotFoundError:
        pass
    except yaml.YAMLError:
        print(f"Warning: {yaml_file} has invalid format. Starting with empty list.")
        pass
    
    # Read new wallet addresses from CSV
    new_wallets = []
    duplicates = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            address = row['Address'].lower()  # 주소를 소문자로 변환하여 비교
            if address not in existing_addresses:
                wallet = {
                    'name': f'wallet{idx}',
                    'wallet_address': row['Address']
                }
                new_wallets.append(wallet)
                existing_addresses.add(address)  # 새로 추가된 주소도 set에 추가
            else:
                duplicates += 1
    
    # Combine existing and new wallets
    all_wallets = existing_wallets + new_wallets
    
    # Create wallet data structure
    wallet_data = {
        'wallets': all_wallets
    }
    
    # Write to YAML file
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(wallet_data, f, default_flow_style=False)
    
    print(f"{len(new_wallets)} new wallet addresses have been added to {yaml_file}")
    if duplicates > 0:
        print(f"{duplicates} duplicate addresses were skipped")
    print(f"Total wallets in {yaml_file}: {len(all_wallets)}")

def main():
    try:
        update_wallet_yaml()
        print("YAML file has been successfully updated")
    except FileNotFoundError:
        print("Error: Please make sure both wallets.csv and wallet_address.yaml exist")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 