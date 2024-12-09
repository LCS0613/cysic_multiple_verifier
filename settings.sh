#!/bin/bash

# 실행 권한 확인 및 부여
chmod +x settings.sh

# yq 설치 확인 및 설치
if ! command -v yq &> /dev/null; then
    echo "Installing yq..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    sudo chmod +x /usr/local/bin/yq
fi

# Check if wallet_address.yaml exists
if [ ! -f "wallet_address.yaml" ]; then
    echo "Error: wallet_address.yaml file not found"
    exit 1
fi

# Read wallet addresses from YAML file
wallets=$(yq eval '.wallets[] | [.name, .wallet_address] | join(" ")' wallet_address.yaml)

# Check if any wallets were found
if [ -z "$wallets" ]; then
    echo "No wallets found in wallet_address.yaml"
    exit 1
fi

# Process each wallet
echo "$wallets" | while read -r name wallet_address; do
    echo "Setting up verifier for $name with address $wallet_address"
    
    # Check if screen session already exists
    if screen -ls | grep -q "$name"; then
        echo "Screen session '$name' already exists. Terminating existing session..."
        screen -S "$name" -X quit
    fi
    
    # Create unique directory for this verifier
    verifier_dir="$HOME/cysic-verifier-$name"
    rm -rf "$verifier_dir"
    mkdir -p "$verifier_dir"
    
    # Download necessary files
    wget -O "$verifier_dir/verifier" https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/verifier_linux
    wget -O "$verifier_dir/libdarwin_verifier.so" https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/libdarwin_verifier.so
    
    # Create config.yaml
    cat > "$verifier_dir/config.yaml" << EOF
# Not Change
chain:
  # Not Change
  # endpoint: "node-pre.prover.xyz:80"
  endpoint: "grpc-testnet.prover.xyz:80"
  # Not Change
  chain_id: "cysicmint_9001-1"
  # Not Change
  gas_coin: "CYS"
  # Not Change
  gas_price: 10
  # Modify Here：! Your Address (EVM) submitted to claim rewards
claim_reward_address: "$wallet_address"

server:
  # don't modify this
  # cysic_endpoint: "https://api-pre.prover.xyz"
  cysic_endpoint: "https://api-testnet.prover.xyz"
EOF
    
    # Set up start script
    cat > "$verifier_dir/start.sh" << EOF
#!/bin/bash
cd "$verifier_dir"
chmod +x verifier
LD_LIBRARY_PATH=. CHAIN_ID=534352 ./verifier
EOF
    
    # Make scripts executable
    chmod +x "$verifier_dir/verifier"
    chmod +x "$verifier_dir/start.sh"
    
    # Create screen session with logging
    screen -dmS "$name" -L -Logfile "$verifier_dir/screen.log" bash "$verifier_dir/start.sh"
    
    echo "Verifier for $name started in screen session"
    sleep 2  # 각 지갑 설정 사이에 약간의 딜레이 추가
done

echo "All verifiers have been set up and started"