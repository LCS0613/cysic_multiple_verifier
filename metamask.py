import os
import csv
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
    Appends to existing file if it exists.
    """
    # 기존 파일이 있는지 확인하고 마지막 wallet number 찾기
    last_wallet_number = 0
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                wallet_num = int(row['Wallet Number'].replace('Wallet ', ''))
                last_wallet_number = max(last_wallet_number, wallet_num)
    except FileNotFoundError:
        pass

    # 파일이 존재하는지 확인
    file_exists = os.path.isfile(filename)
    mode = 'a' if file_exists else 'w'
    
    with open(filename, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Wallet Number', 'Address', 'Private Key', 'Mnemonic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 새 파일인 경우에만 헤더 작성
        if not file_exists:
            writer.writeheader()
        
        # 기존 번호 이후부터 시작
        for wallet in wallets:
            writer.writerow({
                'Wallet Number': f"Wallet {wallet['wallet_number']}",
                'Address': wallet['address'],
                'Private Key': wallet['private_key'],
                'Mnemonic': wallet['mnemonic']
            })
    
    print(f"\n{len(wallets)} wallet(s) information has been added to {filename}")
    print("You can import these wallets to MetaMask using either:")
    print("1. Import Account > Private Key (one by one)")
    print("2. Import Account > Seed Phrase (using mnemonic)")

def main():
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
    
    # Save to CSV file
    save_wallets_to_csv(wallets)
    
    print("\nGenerated Wallet Information:")
    for wallet in wallets:
        print(f"Wallet Number: {wallet['wallet_number']}")
        print(f"Address: {wallet['address']}")
        print(f"Private Key: {wallet['private_key']}")
        print(f"Mnemonic: {wallet['mnemonic']}")
        print("-" * 50)

if __name__ == "__main__":
    main()