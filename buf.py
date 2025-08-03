import requests
import time
import re
from pystyle import Colors,Colorate,Center
gradient_options = [
    Colors.red_to_yellow,
    Colors.green_to_cyan,
    Colors.purple_to_red,
    Colors.yellow_to_red,
    Colors.blue_to_purple,
    Colors.rainbow,
]    # Tool by phước, Không xóa dòng này để tôn trọng tác giả.
# hàm chống bug mạng tránh mấy a bug lỏd 🤟
def checkmang():
    try:
        response = requests.get("https://google.com/", timeout=5)
        return True
    except requests.ConnectionError:
        return False
if not checkmang():
    print("\033[1;31mCheck Mạng Wifi Hoặc 4G ! ")
    sleep(0.5)
    exit()
	
def se3():
    os.system("cls" if os.name == "nt" else "clear")
    os_type = platform.system()
    os_text = f"Hệ điều hành: {os_type}"

    # Banner ASCII    # Tool by phước, Không xóa dòng này để tôn trọng tác giả.
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
    print(Center.XCenter(Colorate.Horizontal(gradient, "Box Zalo: https://zalo.me/g/bhbotm174\n")))
    print(Center.XCenter(Colorate.Horizontal(gradient, "Admin: Phạm An Phước + Trần Dương Ngọc Thành\n")))
    print(Center.XCenter(Colorate.Horizontal(gradient, "Thông Báo : Key sẽ bán với giá siêu rẻ 500đ/1 day \n")))

    # Tool by phước, Không xóa dòng này để tôn trọng tác giả.
cookies = {
    'PHPSESSID': '501ca64fe86f0376d5d67f4dd5bd20d3',
    # ... thêm các cookie khác
}

headers = {
    'authority': 'socioblend.com',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://socioblend.com',
    'referer': 'https://socioblend.com/free-tiktok-views',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; SM-A207F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
}

def send_tiktok(video_url):
    data = {'video_url': video_url}
    response = requests.post('https://socioblend.com/submit-tiktok.php', cookies=cookies, headers=headers, data=data)
    return response.text

def extract_wait_time(response_text):
    # Tìm thời gian chờ trong thông báo (nếu có)
    match = re.search(r'(\d+)\s?(seconds|minutes|giây|phút)', response_text)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if 'minute' in unit or 'phút' in unit:
            return value * 60
        return value
    return 60 * 20  # Mặc định chờ 20 phút nếu không rõ

def auto_loop(video_url, max_loops=None):
    count = 0
    while True:
        count += 1
        print(f"\n🔁 Lần gửi thứ {count}...")

        try:
            res = send_tiktok(video_url)
        except Exception as e:
            print(f"❌ Lỗi gửi request: {e}")
            time.sleep(60)
            continue

        if 'success' in res.lower():
            print("✅ Thành công!")
            wait_time = 60 * 20  # Mặc định 20 phút
        elif 'wait' in res.lower() or 'cooldown' in res.lower():
            print("⏳ Đang cooldown...")
            wait_time = extract_wait_time(res)
        elif 'already' in res.lower():
            print("⚠️ Đã gửi trước đó, chờ tiếp...")
            wait_time = extract_wait_time(res)
        else:
            print("❌ Phản hồi không xác định:\n", res)
            wait_time = 60 * 10

        print(f"⏱️ Chờ {wait_time // 60} phút {wait_time % 60} giây...\n")
        time.sleep(wait_time)

        if max_loops and count >= max_loops:
            break

if __name__ == "__main__":
    banner()
    link = input("🔗 Nhập link TikTok: ")
    auto_loop(link)
