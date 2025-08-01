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

        print(Fore.LIGHTWHITE_EX + "\nKết quả từ API:")
        print(res)  # 👈 In toàn bộ dữ liệu để kiểm tra

        if not isinstance(res, dict) or 'data' not in res:
            print(Fore.RED + "Phản hồi bất thường từ API. Thử lại sau.")
            return []

        return res.get('data', [])
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

        if response.status_code == 200 and res.get("success", True):
            print(Fore.LIGHTGREEN_EX + f"💰 Nhận xu thành công: {res}")
        else:
            print(Fore.LIGHTRED_EX + f"⚠️ Nhận xu thất bại: {res}")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi khi gọi API nhận xu: {e}")


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

def main():
    banner()
    # Gọi hàm và sử dụng giá trị trả về
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

            from datetime import datetime
            sky = "\033[38;5;117m"
            blue_cyan = "\033[38;5;75m"
            light_sky = "\033[38;5;111m"
            light_magenta = "\033[38;5;189m"
            very_light_blue = "\033[38;5;159m"
            reset = "\033[0m"
            print(
            f"{sky}\n🔁 Job {blue_cyan}{da_lam} "
            f"{light_sky}│ 🕒 {light_magenta}{datetime.now().strftime('%H:%M:%S')}{reset}"
            )
            open_url(link)

            cho_co_hieu_ung(min_delay, max_delay)

            report_job(headers, uid_id, job_id, job_type)
            if da_lam % 4 == 0:
               get_coin(headers, job_type, uid_id, job_id if job_type == "tiktok_comment" else None)


            # Hiệu ứng ngẫu nhiên sau mỗi job
            symbol = random.choice(symbols)
            print(Fore.GREEN + f"🎉 Hoàn thành job {job_id} {symbol}")

            if total_jobs > 0 and da_lam >= total_jobs:
                print(Fore.LIGHTWHITE_EX + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(
                    Fore.LIGHTGREEN_EX + "✅ " 
                    + Fore.LIGHTYELLOW_EX + "Hoàn thành: " 
                    + Fore.LIGHTMAGENTA_EX + f"{da_lam} job " 
                    + Fore.LIGHTBLUE_EX + "✔ Tool đã chạy thành công!"
                )
                print(Fore.LIGHTWHITE_EX + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                return


main()

