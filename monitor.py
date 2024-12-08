from flask import Flask, render_template
import yaml
import subprocess
import datetime
import os
import argparse

app = Flask(__name__)

def get_wallet_status():
    # Read wallet addresses from yaml
    with open('wallet_address.yaml', 'r') as file:
        wallet_data = yaml.safe_load(file)
    
    wallets_status = []
    running_count = 0
    stopped_wallets = []
    
    for wallet in wallet_data['wallets']:
        name = wallet['name']
        is_running = is_screen_running(name)
        
        if is_running:
            running_count += 1
        else:
            stopped_wallets.append(name)
            
        status_info = {
            'name': name,
            'status': 'RUNNING' if is_running else 'STOPPED',
            'last_log': get_last_log(name),
            'resources': get_resource_usage(name)
        }
        wallets_status.append(status_info)
    
    total_count = len(wallet_data['wallets'])
    stopped_count = total_count - running_count
    
    summary = {
        'total': total_count,
        'running': running_count,
        'stopped': stopped_count,
        'stopped_wallets': stopped_wallets
    }
    
    return wallets_status, summary

def is_screen_running(name):
    """Check if the screen session is running and syncing blocks"""
    if not screen_exists(name):
        return False
    
    last_log = get_last_log(name)
    return "sync to block:" in last_log

def screen_exists(name):
    """Check if the screen session exists"""
    result = subprocess.run(['screen', '-ls'], capture_output=True, text=True)
    return name in result.stdout

def get_last_log(name):
    """Get the last log line from the screen log file"""
    log_path = os.path.expanduser(f'~/cysic-verifier-{name}/screen.log')
    try:
        # Get last 5 lines to find the most recent sync message
        result = subprocess.run(['tail', '-n', '5', log_path], 
                              capture_output=True, text=True)
        log_lines = result.stdout.strip().split('\n')
        
        # Search for the most recent "sync to block:" message
        for line in reversed(log_lines):
            if "sync to block:" in line:
                return line
        
        return log_lines[-1] if log_lines else "No logs available"
    except:
        return "No logs available"

def get_resource_usage(name):
    """Get detailed CPU and RAM usage for the screen session"""
    if not screen_exists(name):
        return {'cpu': '0', 'memory': '0', 'memory_mb': '0'}
    
    try:
        # Get screen session PID
        ps_cmd = f"screen -ls | grep {name} | awk '{{print $1}}' | cut -d'.' -f1"
        pid = subprocess.check_output(ps_cmd, shell=True).decode().strip()
        
        if pid:
            # Get detailed CPU and memory information
            cmd = f"ps -p {pid} -o %cpu,%mem,rss | tail -n 1"
            usage = subprocess.check_output(cmd, shell=True).decode().strip().split()
            
            # Convert RSS (Resident Set Size) from KB to MB
            memory_mb = float(usage[2]) / 1024
            
            return {
                'cpu': usage[0],
                'memory': usage[1],
                'memory_mb': f'{memory_mb:.1f}'
            }
    except:
        pass
    
    return {'cpu': '0', 'memory': '0', 'memory_mb': '0'}

@app.route('/')
def index():
    wallets_status, summary = get_wallet_status()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('monitor.html', 
                         wallets=wallets_status,
                         summary=summary,
                         current_time=current_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wallet Monitor Web Server')
    parser.add_argument('-port', type=int, default=80,
                       help='Port number for the web server (default: 80)')
    
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)