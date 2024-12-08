# cysic_multiple_verifier
Shell scripts for build multiple cysic verifier(for Linux)

## 0. Activate virtual environment
```bash
source .venv/bin/activate
```

## 1. Generate metamask wallets and build yaml file for cysic-verifier
- metamask_import.json : metamask import file(Use for import wallets to metamask in chrome)
- wallet.csv : wallet information (Keeep this file private)
```python
# Generate metamask wallets(ex) number=10)
python metamask.py -num 10

# Build yaml file for cysic-verifier
python build_yaml.py
```

## 2. Modify wallet_address.yaml(if needed)
- Modify EVM names and addresses in the wallet_address.yaml file.
```bash
wallets:
  - name: wallet1
    wallet_address: 0x~
  - name: wallet2
    wallet_address: 0x~
  ...
```
## 3. Build multiple cysic-verifier instances
- Each verifier will be created in a folder named cysic-verifier-{wallet_name} and will start in a screen session named {wallet_name}.
```bash
bash setting.sh
```

## 4. Monitor verifier status
```python
# Default port is 80, if you want to use other port, use -port option
python monitor.py -port 80

# Firewall setting(Ubuntu/Debian)
# ex) Using 80 port
sudo ufw allow 80

# Delete firewall setting(When you don't use 80 port)
sudo ufw delete allow 80 
```
