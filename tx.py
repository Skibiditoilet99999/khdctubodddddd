import os, json, random, time
from datetime import datetime
import uuid, psutil, requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
console = Console()
DATA_DIR = "users"
os.makedirs(DATA_DIR, exist_ok=True)
DEVICE_DB = "devices.json"

def load_json(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {}

def save_json(path, data):
    json.dump(data, open(path, "w"), indent=2)

# Get public IP
def get_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return "0.0.0.0"

# Get MAC address
def get_mac():
    return uuid.getnode()

# Check if device already used
def device_registered():
    devices = load_json(DEVICE_DB)
    ip = get_ip()
    mac = str(get_mac())
    return devices.get(ip) or devices.get(mac)

def register():
    ip = get_ip()
    mac = str(get_mac())
    if device_registered():
        console.print("[red]⚠️ Thiết bị này đã dùng để tạo tài khoản rồi!")
        return None
    username = Prompt.ask("🔐 [cyan]Nhập tên tài khoản muốn tạo[/]").strip()
    user_file = os.path.join(DATA_DIR, username+".json")
    if os.path.exists(user_file):
        console.print("[red]Tên tài khoản đã tồn tại!")
        return None
    data = {
        "username": username, "balance": 10000,
        "last_checkin": "", "history": [],
        "total":0, "win":0, "lose":0
    }
    save_json(user_file, data)
    dev = load_json(DEVICE_DB)
    dev[ip] = username; dev[mac] = username
    save_json(DEVICE_DB, dev)
    console.print(f"[green]✅ Đăng ký thành công! Tài khoản: {username}, được tặng 10k khởi đầu")
    return username

def login():
    username = Prompt.ask("🔐 [green]Nhập tài khoản đăng nhập[/]").strip()
    user_file = os.path.join(DATA_DIR, username+".json")
    if os.path.exists(user_file):
        console.print(f"[cyan]✅ Đăng nhập thành công: {username}")
        return username
    console.print("[red]❌ Tài khoản không tồn tại!")
    return None

def load_user(u): return load_json(os.path.join(DATA_DIR, u+".json"))
def save_user(u, d): save_json(os.path.join(DATA_DIR, u+".json"), d)

def checkin(u, d):
    today = datetime.now().strftime("%Y-%m-%d")
    if d["last_checkin"] != today:
        d["balance"] += 5000000
        d["last_checkin"] = today
        console.print("[bold green]🎁 Điểm danh thành công +1 jack")
        save_user(u, d)
    else:
        console.print("[yellow]⚠️ Hôm nay đã điểm danh rồi")

def show_stats(u, d):
    win = d["win"]; lose = d["lose"]; t = d["total"]
    rate = (win/t*100) if t>0 else 0
    console.print(f"🧾 [cyan]TK {u}[/]: SD={d['balance']} | Ván={t} | Win/Loss={[win,lose]} | Win%={rate:.2f}%")

def leaderboard():
    table = Table(title="🏆 BXH Người Chơi")
    table.add_column("Top"); table.add_column("User"); table.add_column("Balance")
    items = []
    for fn in os.listdir(DATA_DIR):
        d = load_json(os.path.join(DATA_DIR, fn))
        items.append((d["username"], d["balance"]))
    items.sort(key=lambda x:x[1], reverse=True)
    for i,(u,b) in enumerate(items[:10],1):
        table.add_row(str(i), u, str(b))
    console.print(table)

def shake():
    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as p:
        task = p.add_task("🌀 Đang lắc...", total=None)
        time.sleep(random.uniform(1.5, 2.5))

def update_res(u, d, win):
    d["total"]+=1
    if win: d["win"]+=1
    else: d["lose"]+=1

# Modes
def mode_taixiu(u, d):
    bet = int(Prompt.ask("💵 Cược (max 5k)", default="50000"))
    if bet>d["balance"]: console.print("[red]Không đủ tiền"); return
    pick = Prompt.ask("Tài hay Xỉu", choices=["t","x"])
    shake()
    dice = [random.randint(1,6) for _ in range(3)]; tot=sum(dice); res="t" if tot>=11 else "x"
    console.print(f"🎲 {dice} → Total={tot} → {'Tài' if res=='t' else 'Xỉu'}")
    if pick==res:
        d["balance"]+=bet; console.print(f"[green]✅ Win +{bet}")
        update_res(u,d,True)
    else:
        d["balance"]-=bet; console.print(f"[red]❌ Lose -{bet}")
        update_res(u,d,False)
    save_user(u,d)

def mode_3cang(u,d):
    bet=int(Prompt.ask("💵 Cược (max5k)", default="50000"))
    if bet>d["balance"]: console.print("[red]Không đủ tiền"); return
    num=Prompt.ask("Nhập 3 số (vd:123)")
    shake()
    res="".join(str(random.randint(0,9)) for _ in range(3))
    console.print(f"🔢 Kết quả: {res}")
    if num==res:
        win=bet*500; d["balance"]+=win; console.print(f"[green]🎉 Trúng +{win}")
        update_res(u,d,True)
    else:
        d["balance"]-=bet; console.print(f"[red]❌ Thua -{bet}")
        update_res(u,d,False)
    save_user(u,d)

def mode_lode(u,d):
    bet=int(Prompt.ask("💵 Cược (max5k)", default="50000"))
    if bet>d["balance"]: console.print("[red]Không đủ tiền"); return
    num=Prompt.ask("Nhập 2 số (vd:23)")
    shake()
    res=f"{random.randint(0,99):02}"
    console.print(f"🎯 Kết quả: {res}")
    if num==res:
        win=bet*70; d["balance"]+=win; console.print(f"[green]🎉 Win +{win}")
        update_res(u,d,True)
    else:
        d["balance"]-=bet; console.print(f"[red]❌ Lose -{bet}")
        update_res(u,d,False)
    save_user(u,d)

def main():
    console.print("[bold blue]🎲 GAME XÍ NGẦU VIP")
    while True:
        acc = Prompt.ask("1. Đăng nhập\n2. Đăng ký\n0. Out\n", choices=["1","2","0"])
        if acc=="1":
            user=login(); break
        if acc=="2":
            user=register()
            if user: break
        if acc=="0": return

    d=load_user(user)
    while True:
        console.clear(); save_user(user,d)
        console.print(Panel(f"User: [bold]{user}[/] | SD: [green]{d['balance']}đ[/]"))
        cmd = Prompt.ask("Chọn \n1:Tài Xỉu\n2:3 Càng \n3:Lô đề \n4:Điểm danh nhận tiền ng mới\n5:Thông tin \n6:Bảng xếp hạng ng chơi \n0:Exit\n",
                         choices=["1","2","3","4","5","6","0"])
        if cmd=="1": mode_taixiu(user,d)
        elif cmd=="2": mode_3cang(user,d)
        elif cmd=="3": mode_lode(user,d)
        elif cmd=="4": checkin(user,d)
        elif cmd=="5": show_stats(user,d)
        elif cmd=="6": leaderboard()
        elif cmd=="0": break
        Prompt.ask("Nhấn Enter để về menu")
        console.clear()

if __name__=="__main__":
    main()
