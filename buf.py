import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.table import Table
from rich.console import Console

API_URL = "http://apihoangthanhtung.ddns.net:5000"
API_KEY = "tungvip"
console = Console()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    console.print("=" * 50, style="bold green")
    console.print("      [cyan]TOOL BUFF TIKTOK BY PHUOCAN[/cyan]", justify="center")
    console.print("=" * 50, style="bold green")

def send_request(link, action, index):
    full_url = f"{API_URL}/web={link}/{action}?key={API_KEY}"
    try:
        res = requests.get(full_url, timeout=10)
        data = res.json()
        return {"index": index, **data}
    except Exception as e:
        return {"index": index, "status": "error", "message": str(e)}

def main():
    while True:
        clear()
        banner()

        link = input("🔗 Nhập link TikTok: ").strip()
        print("\n📌 Chọn loại buff:")
        print("1. Buff Tym ❤️")
        print("2. Buff View 👁️")
        choice = input("👉 Nhập lựa chọn (1 hoặc 2): ").strip()

        if choice == "1":
            action = "tym"
        elif choice == "2":
            action = "view"
        else:
            console.print("❌ [red]Lựa chọn không hợp lệ![/red]")
            time.sleep(2)
            continue

        try:
            thread_count = int(input("🔁 Nhập số luồng (buff bao nhiêu lần): "))
        except ValueError:
            console.print("❌ [red]Số không hợp lệ![/red]")
            time.sleep(2)
            continue

        console.print("\n🚀 Đang thực hiện buff...\n", style="bold cyan")

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request, link, action, i+1) for i in range(thread_count)]
            for future in as_completed(futures):
                results.append(future.result())

        table = Table(title="📊 Kết quả buff")
        table.add_column("STT", justify="center")
        table.add_column("Trạng Thái")
        table.add_column("Chi Tiết")

        for r in sorted(results, key=lambda x: x["index"]):
            status = r.get("status", "success")
            if status == "error":
                table.add_row(str(r["index"]), "[red]Lỗi[/red]", r.get("message", "Không rõ"))
            else:
                msg = ", ".join([f"{k}: {v}" for k, v in r.items() if k != "index"])
                table.add_row(str(r["index"]), "[green]Thành công[/green]", msg)

        console.print(table)

        again = input("\n↩️ Buff tiếp? (y/n): ").lower()
        if again != "y":
            console.print("👋 [yellow]Tạm biệt![/yellow]")
            break

if __name__ == "__main__":
    main()
