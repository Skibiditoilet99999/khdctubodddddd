# thêm api
import requests
import os
import time
import random
from tqdm import tqdm
from colorama import Fore, init
import platform
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import random
from rich.text import Text 
from pystyle import Colors,Colorate,Center
init(autoreset=True)

def cho_co_hieu_ung(min_delay, max_delay):
    delay = random.randint(min_delay, max_delay)

    with Progress(
        SpinnerColumn(spinner_name="dots"),  # Sử dụng spinner kiểu ⠋⠙⠸⠴⠦⠇
        TextColumn("[bold cyan]Delay..."),
        transient=True,  # Ẩn sau khi xong
    ) as progress:
        task = progress.add_task("", total=None)
        time.sleep(delay)

gradient_options = [
    Colors.red_to_yellow,
    Colors.green_to_cyan,
    Colors.purple_to_red,
    Colors.yellow_to_red,
    Colors.blue_to_purple,
    Colors.rainbow,
]

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    os_type = platform.system()
    os_text = f"Hệ điều hành: {os_type}"

    # Banner ASCII
    ascii = """
           © COPYRIGHT BY PHƯỚC AN + BVZONE 2025

██████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██╗░░░░░
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
██████╦╝╚██╗░██╔╝░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══██╗░╚████╔╝░░░░██║░░░██║░░██║██║░░██║██║░░░░░
██████╦╝░░╚██╔╝░░░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚═════╝░░░░╚═╝░░░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝

"""

    # Random màu
    gradient = random.choice(gradient_options)
    colored_ascii = Colorate.Vertical(gradient, ascii)
    for line in colored_ascii.splitlines():
        print(Center.XCenter(line))
        time.sleep(0.01)

    # Quote sự kiện
    
    print(Center.XCenter(Colorate.Horizontal(gradient, f"\n{os_text}")))
    print(Center.XCenter(Colorate.Horizontal(gradient, "🔗 Box Zalo: https://zalo.me/g/bhbotm174\n")))
    print(Center.XCenter(Colorate.Horizontal(gradient, "🔗 Admin: Phạm An Phước + Trần Dương Ngọc Thành\n")))

def print_coin_received(coin):
    print(Fore.LIGHTWHITE_EX + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    text = Text(f"[=_=] > Nhận thành công {coin} xu | Tool Bvzone")
    print(Fore.LIGHTWHITE_EX + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    gradient_colors = ["green", "bright_green", "cyan", "magenta", "red"]
    for i in range(len(text)):
        text.stylize(gradient_colors[i % len(gradient_colors)], i, i + 1)
    console.print(text)

def config_uid(token, uid_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-Api-Version': 'public_ver_1',
    }
    json_data = {'uidId': uid_id}
    try:
        r = requests.post('https://public.traodoituongtac.com/api/v2/config-uid', headers=headers, json=json_data)
        res = r.json()
        print(Fore.GREEN + '✅ Cấu hình UID thành công:', res.get("message", res))
        return headers
    except Exception as e:
        print(Fore.RED + f'❌ Lỗi khi cấu hình UID: {e}')
        exit()

def get_jobs(headers, uid_id, uid_name, job_type):
    json_data = {
        'fields': job_type,
        'uidId': uid_id,
        'uidName': uid_name,
    }
    try:
        r = requests.post('https://public.traodoituongtac.com/api/v2/get-jobs', headers=headers, json=json_data)
        res = r.json()

        if not isinstance(res, dict) or 'data' not in res:
            print(Fore.RED + "❌ Phản hồi bất thường từ API. Thử lại sau.")
            return []

        data = res.get('data', [])
        print(Fore.LIGHTGREEN_EX + f"✅ Đã tìm thấy {len(data)} job.")
        return data

    except Exception as e:
        print(Fore.RED + '❌ Lỗi khi lấy job:', e)
        return []


def report_job(headers, uid_id, job_id, job_type):
    json_data = {
        'field': job_type,
        'isJobDie': False,
        'isSuccess': True,
        'jobId': job_id,
        'uidId': uid_id,
        'note': 'Đã hoàn thành bằng tool',
    }
    try:
        r = requests.post('https://public.traodoituongtac.com/api/v2/reports', headers=headers, json=json_data)
        print(Fore.MAGENTA + 'Xác minh thành công:', r.json())
    except Exception as e:
        print(Fore.RED + 'Lỗi khi xác minh job:', e)

def get_coin(headers, job_type, uid_id, job_id=None):
    json_data = {
        "field": job_type,
        "uidId": uid_id
    }

    if job_type == "tiktok_comment" and job_id:
        json_data["jobId"] = job_id

    try:
        response = requests.post(
            "https://public.traodoituongtac.com/api/v2/get-coins",
            headers=headers,
            json=json_data
        )
        res = response.json()

        if response.status_code == 200 and res.get("success") == True:
            coin = res.get("coin_received", 0)
            print_coin_received(coin)
        else:
            print(Fore.LIGHTRED_EX + "⚠️ Nhận xu thất bại!")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi khi gọi nhận xu: {e}")



def kiem_tra_ket_noi_adb(ip_port):
    try:
        os.system(f"adb disconnect")
        os.system(f"adb connect {ip_port}")
        out = os.popen("adb devices").read()
        if "device" in out and ip_port.split(":")[0] in out:
            print(Fore.GREEN + f"✅ Đã kết nối ADB với thiết bị: {ip_port}")
            return True
        else:
            print(Fore.RED + "❌ Kết nối thất bại. Hãy kiểm tra lại IP:PORT và bật gỡ lỗi USB/Wi-Fi.")
            return False
    except Exception as e:
        print(Fore.RED + f"Lỗi khi kết nối ADB: {e}")
        return False


def open_url(url):
    try:
        os.system(f'termux-open-url "{url}"')
        print(Fore.YELLOW + 'Đã mở:', url)
    except Exception as e:
        print(Fore.RED + 'Không mở được link:', e)

def chon_nhiem_vu():
    print(Fore.LIGHTBLUE_EX + "\nChọn loại nhiệm vụ:")
    print("1. Tiktok Follow")
    print("2. Tiktok Tym (Like)")
    print("3. Tiktok Cmt ")
    while True:
        choice = input(Fore.LIGHTYELLOW_EX + "👉 Nhập lựa chọn (1/2/3): ").strip()
        if choice == "1":
            return "tiktok_follow"
        elif choice == "2":
            return "tiktok_like"
        elif choice == "3":
           return "tiktok_comment"
        else:
            print(Fore.RED + "⚠️ Lựa chọn không hợp lệ. Vui lòng chọn lại.")

from datetime import datetime
from colorama import Fore
from tqdm import tqdm
import random
import time
from rich.console import Console
from rich.table import Table
import os

console = Console()

def show_menu():
    table = Table(title="Chọn chế độ", show_lines=True)
    table.add_column("Lựa chọn", style="cyan", justify="center")
    table.add_column("Mô tả", style="magenta")

    table.add_row("1", "Dùng TOKEN + UID đã lưu từ trước")
    table.add_row("2", "Nhập TOKEN và UID mới")

    console.print(table)
    return input("[bold yellow]👉 Nhập lựa chọn [1/2]: [/]").strip()

def nhap_token_uid():
    token = input("🔑 Nhập TOKEN Traodoituongtac: ").strip()
    uid = input("👤 Nhập UID TikTok (vd: abcdxyz1234): ").strip()
    with open("config.txt", "w") as f:
        f.write(f"{token}\n{uid}")
    return token, uid

def load_token_uid():
    with open("config.txt", "r") as f:
        lines = f.read().splitlines()
        return lines[0], lines[1]

# Bắt đầu
if os.path.exists("config.txt"):
    lua_chon = show_menu()
    if lua_chon == "1":
        try:
            token, uid_id = load_token_uid()
            print(f"✅ Đã dùng token: {token}")
            print(f"✅ Đã dùng UID: {uid_id}")
        except Exception:
            print("❌ File config.txt lỗi. Vui lòng nhập lại.")
            token, uid_id = nhap_token_uid()
    elif lua_chon == "2":
        token, uid_id = nhap_token_uid()
    else:
        print("❌ Lựa chọn không hợp lệ. Thoát...")
        exit()
else:
    print("⚠️ Không tìm thấy file config.txt. Vui lòng nhập thông tin:")
    token, uid_id = nhap_token_uid()

uid_name = uid_id  # Tùy theo đoạn code cũ bạn đang dùng

from rich.console import Console
from rich.table import Table

console = Console()

def chon_che_do_adb():
    table = Table(title="🔌 Chọn chế độ kết nối thiết bị", show_lines=True)
    table.add_column("Lựa chọn", style="cyan", justify="center")
    table.add_column("Mô tả", style="magenta")

    table.add_row("1", "Kết nối ADB Auto")
    table.add_row("2", "Không dùng ADB")

    console.print(table)
    return input("[bold yellow]👉 Nhập lựa chọn (1/2): [/]").strip()


def main():
    banner()

    # Bảng chọn chế độ ADB
    def chon_che_do_adb():
        table = Table(title="🔌 Chọn chế độ kết nối thiết bị", show_lines=True)
        table.add_column("Lựa chọn", style="cyan", justify="center")
        table.add_column("Mô tả", style="magenta")
        table.add_row("1", "Kết nối ADB Auto")
        table.add_row("2", "Không dùng ADB ")
        console.print(table)
        return input("[bold yellow]👉 Nhập lựa chọn (1/2): [/]").strip()

    adb_mode = chon_che_do_adb()
    use_adb = False
    x = y = 0

    if adb_mode == "1":
        ip_port = input(Fore.LIGHTCYAN_EX + "📶 Nhập IP:PORT thiết bị (ví dụ 192.168.1.8:5555): ").strip()
        if kiem_tra_ket_noi_adb(ip_port):
            use_adb = True
            try:
                x = int(input(Fore.CYAN + "📍 Nhập tọa độ X để tap TikTok: "))
                y = int(input(Fore.CYAN + "📍 Nhập tọa độ Y để tap TikTok: "))
            except:
                print(Fore.RED + "⚠️ Tọa độ không hợp lệ. Tắt chế độ ADB.")
                use_adb = False
        else:
            print(Fore.RED + "⚠️ Không thể kết nối ADB. Chạy chế độ thường.")

    # Load TOKEN và UID
    token, uid_id = load_token_uid()
    uid_name = uid_id
    job_type = chon_nhiem_vu()
    headers = config_uid(token, uid_id)

    try:
        total_jobs = int(input(Fore.LIGHTGREEN_EX + "📌 Nhập số job muốn chạy (0 = không giới hạn): ").strip())
    except:
        total_jobs = 0 
    try:
        min_delay = int(input(Fore.LIGHTCYAN_EX + "⏱ Nhập delay tối thiểu (giây): ").strip())
        max_delay = int(input(Fore.LIGHTCYAN_EX + "⏱ Nhập delay tối đa (giây): ").strip())
        if min_delay > max_delay:
            min_delay, max_delay = 5, 15
            print(Fore.YELLOW + "⚠️ Delay không hợp lệ. Dùng mặc định 5–15s.")
    except:
        min_delay, max_delay = 5, 15
        print(Fore.YELLOW + "⚠️ Không nhập delay. Dùng mặc định 5–15s.")

    da_lam = 0
    job_id_done = set()
    symbols = ["✔", "✨", "🚀", "🔥", "💯"]

    while True:
        jobs = get_jobs(headers, uid_id, uid_name, job_type)

        if not jobs:
            print(Fore.LIGHTRED_EX + "Hết job! Đang chờ 10 giây để thử lại...")
            time.sleep(10)
            continue

        for job in tqdm(jobs, desc="Đang làm job", colour='cyan'):
            if not isinstance(job, dict):
                print(Fore.RED + "Dữ liệu job không hợp lệ. Bỏ qua.")
                continue

            job_id = job.get('job_id')
            link = job.get('link')
            if not job_id or not link:
                print(Fore.RED + "❌ Job lỗi: thiếu ID hoặc link. Bỏ qua.")
                continue
            if job_id in job_id_done:
                print(Fore.YELLOW + f"🔁 Đã làm job {job_id} trước đó. Bỏ qua.")
                continue

            job_id_done.add(job_id)
            da_lam += 1

            # Hiển thị job đang làm
            now = datetime.now().strftime('%H:%M:%S')
            print(f"\033[38;5;117m\n \033[38;5;75m[{da_lam}] │ \033[38;5;189m{now}\033[0m")

            # Lấy comment nếu là job comment
            comment_text = ""
            if job_type == "tiktok_comment":
                comment_text = job.get('extra_info', {}).get('comment') or job.get('job_info', '')
                print(f"Nội dung cần comment: {comment_text} ")
            open_url(link)

            # Tự tap và comment nếu dùng ADB
            if use_adb:
                try:
                    time.sleep(3)
                    os.system(f'adb shell input tap {x} {y}')
                    print(Fore.LIGHTGREEN_EX + f"📱 Đã tap tại tọa độ {x},{y}")

                    if job_type == "tiktok_comment" and comment_text:
                        time.sleep(2)
                        os.system(f'adb shell input text "{comment_text}"')
                        time.sleep(1)
                        os.system('adb shell input keyevent 66')
                        print(Fore.LIGHTGREEN_EX + f"Đã comment: {comment_text}")
                except Exception as e:
                    print(Fore.RED + f"❌ ADB lỗi: {e}")

            # Delay có hiệu ứng
            cho_co_hieu_ung(min_delay, max_delay)

            # Gửi xác nhận hoàn thành
            report_job(headers, uid_id, job_id, job_type)

            # Nhận xu mỗi 4 job
            if da_lam % 4 == 0:
                get_coin(headers, job_type, uid_id, job_id if job_type == "tiktok_comment" else None)

            symbol = random.choice(symbols)
            print(f"[{da_lam}]| {job_id} | {now} | SUCCESS | {symbol}")

            if total_jobs > 0 and da_lam >= total_jobs:
                print(Fore.LIGHTWHITE_EX + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(Fore.LIGHTGREEN_EX + "✅ "
                      + Fore.LIGHTYELLOW_EX + "Hoàn thành: "
                      + Fore.LIGHTMAGENTA_EX + f"{da_lam} job "
                      + Fore.LIGHTBLUE_EX + "✔ Tool đã chạy thành công!")
                print(Fore.LIGHTWHITE_EX + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                return

main()


