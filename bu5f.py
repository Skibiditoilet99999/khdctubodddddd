import requests
import random
import time
from rich import print
from rich.panel import Panel

USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; SM-A107F)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Linux; Android 12; Redmi Note 10 Pro)',
]

def random_user_agent():
    return random.choice(USER_AGENTS)

def get_headers():
    ua = random_user_agent()
    return {
        'user-agent': ua,
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.6,en;q=0.5',
        'referer': 'https://myinstafollow.com/free-tiktok-tools/',
        'origin': 'https://myinstafollow.com',
    }

def buff_views(link, amount):
    if amount < 100:
        amount = 100  # Đảm bảo tối thiểu là 100 view
    
    headers = get_headers()
    files = {
        'service': (None, '7583'),
        'postlink': (None, link),
        'tiktokviewsQuantity': (None, str(amount)),
        'extended_user_agent': (None, f'User-agent header: {headers["user-agent"]}'),
    }
    res = requests.post(
        'https://myinstafollow.com/themes/vision/part/free-tiktok-views/submitForm.php',
        headers=headers,
        files=files
    )
    return res.text

def buff_likes(link, amount):
    if amount < 10:
        amount = 10  # đảm bảo tối thiểu 10 like

    headers = get_headers()
    files = {
        'service': (None, '6455'),
        'postlink': (None, link),
        'tiktoklikesQuantity': (None, str(amount)),
        'extended_user_agent': (None, f'User-agent header: {headers["user-agent"]}'),
    }
    res = requests.post(
        'https://myinstafollow.com/themes/vision/part/free-tiktok-likes/submitForm.php',
        headers=headers,
        files=files
    )
    return res.text

def cooldown_timer(seconds):
    print(Panel(f"[yellow]⏳ Chờ [bold]{seconds // 60} phút[/bold] để tiếp tục..."))
    for i in range(seconds, 0, -1):
        mins, secs = divmod(i, 60)
        print(f"[cyan]⏱  Còn lại: [bold]{mins:02d}:{secs:02d}[/bold]", end='\r')
        time.sleep(1)
    print("\n[green]✅ Hết thời gian chờ.[/green]")

def main():
    print(Panel("[bold green]TOOL BUFF TIKTOK[/bold green]"))

    # Nhập nhiều link
    links = []
    while True:
        link = input("[🔗] Nhập link TikTok (Enter để dừng): ").strip()
        if link == "":
            break
        links.append(link)

    if not links:
        print("[red]❌ Không có link nào được nhập![/red]")
        return

    mode = input("[⚙️] Chọn chế độ (1: View, 2: Tym, 3: View + Tym): ").strip()
    amount = int(input("[🔢] Nhập số lượng muốn buff mỗi link: "))

    for idx, link in enumerate(links, 1):
        print(Panel(f"[bold cyan]🎯 Bắt đầu buff link thứ {idx}: {link}"))

        if mode == "1":
            print(Panel("[blue]🚀 Buff View..."))
            res = buff_views(link, amount)
            print("[green]Kết quả:[/green]", res[:200])

        elif mode == "2":
            print(Panel("[magenta]💓 Buff Tym..."))
            res = buff_likes(link, amount)
            print("[green]Kết quả:[/green]", res[:200])

        elif mode == "3":
            print(Panel("[blue]🚀 Buff View trước..."))
            res1 = buff_views(link, amount)
            print("[green]Kết quả:[/green]", res1[:200])

            print("[yellow]⏳ Đợi 90s trước khi buff Tym...[/yellow]")
            time.sleep(90)

            print(Panel("[magenta]💓 Buff Tym..."))
            res2 = buff_likes(link, amount)
            print("[green]Kết quả:[/green]", res2[:200])

        else:
            print("[red]❌ Sai chế độ. Dừng tool.[/red]")
            return

        print(Panel(f"[bold green]✅ Hoàn tất buff cho link {idx}[/bold green]"))

    
if __name__ == "__main__":
    main()
