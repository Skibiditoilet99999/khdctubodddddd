import requests
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from time import sleep

console = Console()

API_URL = "https://keyherlyswar.x10.mx/Apidocs/reglq.php?count="

def banner():
    console.print(Panel.fit("[bold cyan]TOOL REG GARENA AUTO[/]\n[green]Author: @SOICODOC[/]\n", title="🎮 Garena Account Generator", style="bold blue"))

def get_accounts(count):
    try:
        url = API_URL + str(count)
        response = requests.get(url)
        data = response.json()

        if data.get("status"):
            return data["result"]
        else:
            console.print("[red]❌ API trả về lỗi hoặc không có tài khoản.[/]")
            return []
    except Exception as e:
        console.print(f"[red]Lỗi khi kết nối API: {e}[/]")
        return []

def save_accounts(accounts):
    with open("garena_accounts.txt", "a", encoding="utf-8") as f:
        for acc in accounts:
            f.write(f"{acc['account']}|{acc['password']}\n")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    
    try:
        count = int(console.input("[yellow]Nhập số lượng tài khoản cần tạo (MAX 15): [bold cyan]"))
        if count > 15:
            sys.exit("TỐI ĐA LÀ 15")
    except ValueError:
        console.print("[red]Vui lòng nhập số hợp lệ![/]")
        sys.exit()

    console.print(f"[cyan]Đang tạo {count} tài khoản Garena...[/]")
    sleep(1)
    
    accounts = get_accounts(count)

    if accounts:
        table = Table(title=f"DANH SÁCH {len(accounts)} ACCOUNT GARENA", title_style="bold magenta")
        table.add_column("STT", justify="center", style="yellow", no_wrap=True)
        table.add_column("USERNAME", style="green")
        table.add_column("PASSWORD", style="cyan")

        # Progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[blue]Đang reg tài khoản...", total=len(accounts))
            
            for i, acc in enumerate(accounts, start=1):
                sleep(0.5)  # Giả lập thời gian reg
                progress.update(task, advance=1)
                console.print(f"[green]✔ Reg success tk #{i} -> {acc['account']} | {acc['password']}[/]")
                table.add_row(str(i), acc['account'], acc['password'])

        save_accounts(accounts)
        console.print(table)
        console.print(Panel.fit("[green]✅ Hoàn tất! Tài khoản đã lưu vào file [bold]garena_accounts.txt[/].[/]", style="bold green"))
    else:
        console.print("[red]Không lấy được tài khoản nào![/]")

if __name__ == "__main__":
    main()
