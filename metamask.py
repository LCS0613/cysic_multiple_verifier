import os
import csv
import json
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic
import argparse

def generate_wallets(num_wallets, start_number=1):
    """
    Generate EVM wallets
    
    :param num_wallets: number of wallets to generate
    :param start_number: starting wallet number (default: 1)
    :return: information about EVM wallets
    """
    Account.enable_unaudited_hdwallet_features()
    mnemo = Mnemonic("english")
    wallets = []
    
    for i in range(start_number, start_number + num_wallets):
        mnemonic_phrase = mnemo.generate(strength=128)
        seed = mnemo.to_seed(mnemonic_phrase)
        account = Account.from_key(seed[:32])
        
        wallet_info = {
            'wallet_number': i,
            'address': account.address,
            'private_key': account.key.hex(),
            'mnemonic': mnemonic_phrase
        }
        wallets.append(wallet_info)
    
    return wallets

def save_wallets_to_csv(wallets, filename='wallets.csv'):
    """
    Save generated wallet information to a CSV file.
    """
    # Windows에서 파일 핸들링 이슈 방지
    mode = 'w' if os.name != 'nt' else 'w+'
    
    with open(filename, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Wallet Number', 'Address', 'Private Key', 'Mnemonic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for wallet in wallets:
            writer.writerow({
                'Wallet Number': wallet['wallet_number'],
                'Address': wallet['address'],
                'Private Key': wallet['private_key'],
                'Mnemonic': wallet['mnemonic']
            })
    
    print(f"{len(wallets)} wallet(s) information has been saved to {filename}")

def create_metamask_import(wallets, json_file='metamask_import.json'):
    """
    Create JSON file for MetaMask import with consistent wallet naming
    """
    metamask_accounts = []
    
    for wallet in wallets:
        account = {
            "name": f"wallet{wallet['wallet_number']}",
            "mnemonic": wallet['mnemonic'],
            "numberOfAccounts": 1,
            "hdPath": "m/44'/60'/0'/0"
        }
        metamask_accounts.append(account)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(metamask_accounts, f, indent=2)
    
    print(f"{len(metamask_accounts)} accounts have been saved to {json_file}")

def main():
    # 커맨드 라인 인자 파서 설정
    parser = argparse.ArgumentParser(description='Generate EVM wallets')
    parser.add_argument('-num', '--number', 
                       type=int, 
                       required=True,
                       help='Number of wallets to generate')
    parser.add_argument('-start', '--start_number',
                       type=int,
                       default=1,
                       help='Starting wallet number (default: 1)')
    
    args = parser.parse_args()
    
    # Generate wallets using command line arguments
    wallets = generate_wallets(args.number, args.start_number)
    
    # Save to CSV file (for backup)
    save_wallets_to_csv(wallets)
    
    # Create JSON file for MetaMask import
    create_metamask_import(wallets)
    
    print("\nGenerated Wallet Information:")
    for wallet in wallets:
        print(f"Wallet Number: {wallet['wallet_number']}")
        print(f"Address: {wallet['address']}")
        print(f"Private Key: {wallet['private_key']}")
        print(f"Mnemonic: {wallet['mnemonic']}")
        print("-" * 50)

if __name__ == "__main__":
    main()