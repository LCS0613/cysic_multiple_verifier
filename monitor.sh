#!/bin/bash

# Read Telegram configuration
BOT_TOKEN=$(yq e '.bot_token' telegram_config.yaml)
CHAT_ID=$(yq e '.chat_id' telegram_config.yaml)
UPDATE_INTERVAL=$(yq e '.update_interval' telegram_config.yaml)

# Read wallet addresses
wallets=$(yq e '.wallets[] | [.name] | join(" ")' wallet_address.yaml)

# Function to generate status message
generate_status() {
    current_time=$(date '+%Y-%m-%d %H:%M:%S')
    status_msg="🕒 Update Time: ${current_time}\n"
    status_msg+="⏱️ Next Update: in ${UPDATE_INTERVAL} minutes\n\n"
    
    for name in $wallets; do
        # Check screen session status
        if screen -list | grep -q "$name"; then
            status="✅"
            # Get last log line (requires screen log file)
            last_log=$(tail -n 1 ~/cysic-verifier-"$name"/screen.log 2>/dev/null || echo "No logs available")
        else
            status="🔴"
            last_log="Not running"
        fi
        
        status_msg+="${status} ${name}: ${last_log}\n"
    done
    
    echo -e "$status_msg"
}

# Send message to Telegram
send_telegram_message() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${message}" \
        -d parse_mode="HTML"
}

# Note: settings.sh modification required
# Add log file configuration when creating screen session