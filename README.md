# cysic_multiple_verifier
Scripts for build multiple cysic verifier(for Linux)

## 0. Update and upgrade packages & download git repository
```bash
# Update and upgrade packages
sudo apt update
sudo apt get-upgrade

# Download git repository
git clone https://github.com/LCS0613/cysic_multiple_verifier.git
```

## 1. Activate Python virtual environment
```bash
cd ~/cysic_multiple_verifier
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Generate metamask wallets and build yaml file for cysic-verifier
- wallet.csv : wallet information (Keep this file private)
```python
# Generate metamask wallets
# Option 1: Generate 10 wallets starting from wallet1
python metamask.py -num 10

# Option 2: Generate 5 wallets starting from wallet6
python metamask.py -num 5 -start 6

# Build yaml file for cysic-verifier(wallet_address.yaml)
python build_yaml.py
```

## 3. Modify wallet_address.yaml(if needed)
- Modify EVM names and addresses in the wallet_address.yaml file.
```bash
wallets:
  - name: wallet1
    wallet_address: 0x~
  - name: wallet2
    wallet_address: 0x~
  ...
```

## 4. Build multiple cysic-verifier instances
- Each verifier will be created in a folder named cysic-verifier-{wallet_name} and will start in a screen session named {wallet_name}.
```bash
bash setting.sh
```

## 5. Monitor verifier status
```python
# Default port is 80, if you want to use other port, use -port option
python monitor.py -port 80

# Firewall setting(Ubuntu/Debian)
# ex) Using 80 port
sudo ufw allow 80

# Delete firewall setting(When you don't use 80 port)
sudo ufw delete allow 80 
```

## 6. Restart verifier instances
```bash
cd ~/cysic_multiple_verifier
bash settings.sh
```
