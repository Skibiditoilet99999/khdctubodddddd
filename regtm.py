import requests
import json
import random
import time
import sys
import threading
import os
import queue
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_session(proxy=None):
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    if proxy:
        session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    return session

def get_available_domains(session):
    url = "https://api.mail.tm/domains"
    headers = {"Accept": "application/json"}
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        domains = response.json()
        return domains[0]["domain"]
    except requests.exceptions.RequestException:
        return "mail.tm"

def create_mailtm_account(session, account_num, max_retries=3):
    url = "https://api.mail.tm/accounts"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ])
    }
    domain = get_available_domains(session)
    payload = {
        "address": f"phuocdev{random.randint(1000, 9999)}@{domain}",
        "password": f"phuocan{random.randint(1000, 9999)}"
    }
    
    for attempt in range(max_retries):
        try:
            response = session.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            account_data = response.json()
            
            if "address" in account_data:
                return account_data["address"], payload["password"]
            else:
                return None, None
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get('Retry-After', 5 ** attempt)
                wait_time = max(int(retry_after), 5 ** attempt) + random.uniform(0, 2)
                time.sleep(wait_time)
                continue
            else:
                return None, None
        except requests.exceptions.RequestException:
            return None, None
    
    return None, None

def save_to_file(username, password, filename):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{username}|{password}\n")
        return True
    except IOError:
        return False

def create_multiple_accounts(num_accounts, filename):
    clear_screen()
    console.print(Panel.fit("[bold magenta]MAILTM ACCOUNT CREATOR[/]\n[green]Author: PHUOC AN + BVZone[/]", title="🔥 TOOL MAILTM", style="bold blue"))

    accounts_list = []
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Đang tạo tài khoản...", total=num_accounts)

        session = setup_session()
        for i in range(1, num_accounts + 1):
            username, password = create_mailtm_account(session, i)
            if username and password:
                accounts_list.append((username, password))
                save_to_file(username, password, filename)
                console.print(f"[green]✔ Tạo thành công #{i} -> {username} | {password}[/]")
            else:
                console.print(f"[red]✖ Tạo thất bại #{i}[/]")
            progress.update(task, advance=1)
            time.sleep(random.uniform(1, 2))  # Giả lập delay

    # Hiển thị bảng kết quả
    table = Table(title=f"[bold yellow]DANH SÁCH {len(accounts_list)} ACCOUNT MAILTM[/]")
    table.add_column("STT", justify="center", style="cyan")
    table.add_column("USERNAME", style="green")
    table.add_column("PASSWORD", style="magenta")

    for idx, (u, p) in enumerate(accounts_list, start=1):
        table.add_row(str(idx), u, p)

    console.print(table)
    console.print(Panel.fit("[bold green]✅ Hoàn tất! Tài khoản đã lưu vào file mailtm_accounts.txt[/]", style="bold green"))

def main():
    try:
        num_accounts = int(console.input("[yellow]Nhập số lượng tài khoản cần tạo: [bold cyan]"))
    except ValueError:
        console.print("[red]Vui lòng nhập số hợp lệ![/]")
        return
    
    filename = "mailtm_accounts.txt"
    create_multiple_accounts(num_accounts, filename)

if __name__ == "__main__":
    main()
