import requests
import time
import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

buff_history = {}  # lưu số lần buff mỗi video (reset mỗi ngày)

def banner():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]TOOL BUFF VIEW TIKTOK[/bold cyan]\n[green]Giới hạn 5 lần/ngày mỗi video[/green]",
        title="[bold red]BUFF VIP",
        border_style="bold magenta"
    ))

def countdown(seconds):
    for i in range(seconds, 0, -1):
        console.print(f"[yellow]Chờ {i}s...[/yellow]", end="\r")
        time.sleep(1)
    print()

def get_video_list():
    try:
        with open("video_list.txt", "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
            if links:
                return links
    except:
        pass
    # fallback: nhập thủ công
    console.print("[cyan]Không tìm thấy file [bold]video_list.txt[/bold] hoặc file trống.")
    link = input("➤ Nhập link TikTok thủ công: ").strip()
    return [link] if link else []

def buff_view(video_url):
    url_api = f"http://apihoangthanhtung.ddns.net:5000/web={video_url}view?key=duongca1"
    try:
        res = requests.get(url_api, timeout=10)
        if res.status_code == 200:
            data = res.json()
            status = data.get("status", "")
            message = data.get("message", "")
            if status == "success":
                console.print(f"[green]✅ Thành công:[/green] {message}")
                return 0
            elif status == "wait":
                m = re.search(r'(\d+)\s*giay', message)
                seconds = int(m.group(1)) if m else 30
                console.print(f"[yellow]{message}[/yellow]")
                return seconds
            else:
                console.print(f"[red]⚠ Phản hồi lạ:[/red] {message}")
                return 15
        else:
            console.print(f"[red]❌ Lỗi HTTP {res.status_code}[/red]")
            return 20
    except Exception as e:
        console.print(f"[red]❌ Lỗi kết nối API: {e}[/red]")
        return 20

def reset_history_if_new_day():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    if getattr(reset_history_if_new_day, "last_day", None) != today:
        buff_history.clear()
        reset_history_if_new_day.last_day = today

if __name__ == "__main__":
    banner()
    videos = get_video_list()
    if not videos:
        console.print("[red]Không có video nào để buff![/red]")
        exit()

    console.print(f"[bold green]Tổng video cần buff: {len(videos)}[/bold green]")
    console.print("[cyan]Tự động buff mỗi video, giới hạn 5 lần/ngày. Nhấn Ctrl + C để thoát[/cyan]")

    try:
        while True:
            reset_history_if_new_day()
            for video in videos:
                count = buff_history.get(video, 0)
                if count >= 5:
                    console.print(f"[yellow]🚫 {video} đã đạt giới hạn 5 lần hôm nay.[/yellow]")
                    continue
                delay = buff_view(video)
                buff_history[video] = count + 1
                if delay > 0:
                    countdown(delay)
                else:
                    time.sleep(2)
            console.print("[bold magenta]🔁 Đã hoàn tất 1 vòng. Lặp lại sau 10 giây...[/bold magenta]")
            time.sleep(10)

    except KeyboardInterrupt:
        console.print("\n[bold red]⛔ Đã thoát tool theo yêu cầu.[/bold red]")
