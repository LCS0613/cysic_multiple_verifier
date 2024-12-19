# cysic_multiple_verifier
Scripts for building multiple Cysic network(Testnet-Phase2) validator nodes easily and efficiently.

## System Requirements
### Hardware Requirements
- CPU: Single core
- RAM: 8GB / 1 verifier
- Storage: 512 MB / 1 verifier
- Bandwith : 100 kB/s upload/download

### Software Requirements
- Operating System: Ubuntu 20.04 LTS or higher / Debian 11 or higher
- Python 3.8 or higher
- Git
- Screen
- Node.js 16.x or higher
- npm 8.x or higher

### Network Requirements
- Static IP address recommended
- Open ports:
  - Port 80 (or custom port) for monitoring
  - Port 30303 for P2P communication
  - Port 8545 for JSON-RPC (if needed)

### Storage Requirements
- File system: ext4 recommended
- Disk IOPS: 5000+ recommended for optimal performance

## Prerequisites
- Python 3.8 or higher
- Linux operating system (Ubuntu/Debian recommended)
- Git
- Screen

## Key Features
- Automatic generation of multiple Metamask wallets
- Automated validator node setup for each wallet
- Built-in monitoring system

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
# Convert line endings to Linux format and set execute permission
sed -i 's/\r$//' settings.sh
chmod +x settings.sh

# Run the script
./settings.sh
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
# Convert line endings to Linux format and set execute permission (if needed)
sed -i 's/\r$//' settings.sh
chmod +x settings.sh

# Run the script
./settings.sh
```

## Troubleshooting
### Common Issues
1. Screen session not starting
```bash
# Check if screen is installed
which screen

# If not installed, install screen
sudo apt-get install screen
```

2. Permission denied when running settings.sh
```bash
# Set execute permission
chmod +x settings.sh
```

3. Port already in use
```bash
# Check which process is using the port
sudo lsof -i :80
```

## Security Considerations
- Keep your wallet.csv file secure and never share it
- Regularly backup your wallet information
- Use strong passwords for your wallets
- Consider using a firewall to protect your nodes

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Script Details
### metamask.py
Generates multiple Metamask wallets with specified parameters.

### build_yaml.py
Builds configuration file for Cysic verifier nodes using wallet information.

### monitor.py
Provides web-based monitoring interface for all verifier nodes.

### settings.sh
Sets up and launches multiple verifier instances in separate screen sessions.
