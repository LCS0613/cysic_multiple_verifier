#!/bin/bash

# yq 설치 확인 및 설치
if ! command -v yq &> /dev/null; then
    echo "Installing yq..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    sudo chmod +x /usr/local/bin/yq
fi

# wallet_address.yaml 파일 존재 확인
if [ ! -f "wallet_address.yaml" ]; then
    echo "Error: wallet_address.yaml file not found"
    exit 1
fi

# YAML 파일에서 지갑 주소 읽기
wallets=$(yq eval '.wallets[] | [.name, .wallet_address] | join(" ")' wallet_address.yaml)

# 지갑 정보 확인
if [ -z "$wallets" ]; then
    echo "No wallets found in wallet_address.yaml"
    exit 1
fi

# 각 지갑 처리
echo "$wallets" | while read -r name wallet_address; do
    # screen 세션 존재 여부 확인
    if screen -ls | grep -q "$name"; then
        echo "Screen session '$name' is already running. Skipping..."
        continue  # 다음 지갑으로 넘어감
    fi
    
    echo "Setting up verifier for $name with address $wallet_address"
    
    # verifier 디렉토리 생성
    verifier_dir="$HOME/cysic-verifier-$name"
    rm -rf "$verifier_dir"
    mkdir -p "$verifier_dir"
    
    # 필요한 파일 다운로드
    wget -O "$verifier_dir/verifier" https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/verifier_linux
    wget -O "$verifier_dir/libdarwin_verifier.so" https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/libdarwin_verifier.so
    
    # config.yaml 생성
    cat > "$verifier_dir/config.yaml" << EOF
chain:
  endpoint: "grpc-testnet.prover.xyz:80"
  chain_id: "cysicmint_9001-1"
  gas_coin: "CYS"
  gas_price: 10
claim_reward_address: "$wallet_address"

server:
  cysic_endpoint: "https://api-testnet.prover.xyz"
EOF
    
    # start.sh 스크립트 생성
    cat > "$verifier_dir/start.sh" << EOF
#!/bin/bash
cd "$verifier_dir"
chmod +x verifier
LD_LIBRARY_PATH=. CHAIN_ID=534352 ./verifier
EOF
    
    # 실행 권한 부여
    chmod +x "$verifier_dir/verifier"
    chmod +x "$verifier_dir/start.sh"
    
    # screen 세션 생성
    screen -dmS "$name" -L -Logfile "$verifier_dir/screen.log" bash "$verifier_dir/start.sh"
    
    echo "Verifier for $name started in screen session"
    sleep 2
done

echo "All verifiers have been processed"