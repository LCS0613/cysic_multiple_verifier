import yaml
import csv

def update_wallet_yaml(csv_file='wallets.csv', yaml_file='wallet_address.yaml'):
    """
    Update wallet_address.yaml with addresses from generated wallets CSV file
    
    :param csv_file: Path to the CSV file containing wallet information
    :param yaml_file: Path to the YAML file to update
    """
    # Read wallet addresses from CSV
    wallets_list = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            wallet = {
                'name': f'wallet{idx}',
                'wallet_address': row['Address']
            }
            wallets_list.append(wallet)
    
    # Create wallet data structure
    wallet_data = {
        'wallets': wallets_list
    }
    
    # Write to YAML file
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(wallet_data, f, default_flow_style=False)
    
    print(f"{len(wallets_list)} wallet addresses have been updated in {yaml_file}")

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