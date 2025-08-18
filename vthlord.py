import os
import time
import pyfiglet
import aiohttp
import asyncio
import json
from colorama import Fore, Style, init
import requests
from collections import defaultdict, Counter
from urllib.parse import urlparse, parse_qs
import re
init()
os.system("cls")
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def parse_escapemaster_url(url):
    """Parse URL để lấy userId và secretKey"""
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        user_id = query_params.get('userId', [None])[0]
        secret_key = query_params.get('secretKey', [None])[0]
        
        if user_id and secret_key:
            return user_id, secret_key
        else:
            return None, None
    except Exception as e:
        print(Fore.RED + f"Lỗi khi parse URL: {e}" + Style.RESET_ALL)
        return None, None

current_time = int(time.time() * 1000)

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Panel tiêu đề
console.print(Panel.fit("[bold cyan]HƯỚNG DẪN LẤY LINK[/bold cyan]", border_style="cyan", padding=(1, 2)))

# Tạo bảng hướng dẫn
table = Table(show_header=False, box=None)
table.add_column("Bước", style="bold white")
table.add_column("Hướng Dẫn", style="white")

table.add_row("[bold cyan]B1[/bold cyan]", "Vào [bold magenta]xworld.io[/bold magenta] và đăng nhập")
table.add_row("[bold cyan]B2[/bold cyan]", "Vào game [bold green]Vua Thóat Hiểm[/bold green]")
table.add_row("[bold cyan]B3[/bold cyan]", "Sao chép link URL từ thanh địa chỉ")

console.print(table)

# Hiển thị ví dụ link
console.print(Panel.fit("[yellow]VD: https://escapemaster.net/battleroyale/?userId=XXXXX&secretKey=XXXXXXXXXXXXXXXX&language=default[/yellow]", title="Ví dụ", border_style="yellow", padding=(1, 2)))



import os
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def nhap_du_lieu():
    console.print("\n[bold yellow]Tool By PhuocAn[/bold yellow]")
    console.print(Panel.fit("[bold cyan]NHẬP THÔNG TIN NGƯỜI DÙNG[/bold cyan]", border_style="cyan", padding=(1, 2)))

    file_name = "xworld_data.json"

    # Nếu file đã tồn tại → đọc lại, nếu lỗi thì yêu cầu nhập lại
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
            console.print("[green]✅ Đã tìm thấy thông tin cũ, dùng lại...[/green]")
            user_id = data.get("user_id", "")
            user_login = data.get("user_login", "login_v2")
            user_secret_key = data.get("user_secret_key", "")
        except (json.JSONDecodeError, ValueError):
            console.print("[red]⚠ File bị lỗi hoặc trống! Vui lòng nhập lại.[/red]")
            os.remove(file_name)
            return nhap_du_lieu()  # Gọi lại hàm để nhập lại
    else:
        user_id = Prompt.ask("[yellow]➤ UID Acc Xworld[/yellow]")
        user_secret_key = Prompt.ask("[yellow]➤ Secret Key Xworld[/yellow]")

        with open(file_name, "w") as f:
            json.dump({
                "user_id": user_id,
                "user_login": "login_v2",
                "user_secret_key": user_secret_key
            }, f)
        console.print("[green]✅ Đã lưu thông tin vào file![/green]")

    # Nhập số tiền cược
    while True:
        try:
            amount = int(Prompt.ask("[yellow]➤ Số tiền cược ban đầu (tối thiểu 1 BUILD)[/yellow]"))
            if amount < 1:
                raise ValueError
            break
        except ValueError:
            console.print("[red]⚠ Vui lòng nhập số nguyên ≥ 1 cho số tiền cược.[/red]")
            time.sleep(1)

    console.print("\n[green]✅ Nhập dữ liệu thành công![/green]")
    return user_id, user_secret_key, amount

# Gọi hàm nhập dữ liệu
user_id, user_secret_key, amount = nhap_du_lieu()
user_login = "login_v2"

amount = int(input(Fore.YELLOW + "Nhập số tiền cược ban đầu (nhỏ nhất 1 build): "))

print(Fore.CYAN + "\n=== CÀI ĐẶT STOP LOSS/TAKE PROFIT ===" + Style.RESET_ALL)
while True:
    stop_loss_input = input(Fore.YELLOW + "Bật Stop Loss? (y/n): ").strip().lower()
    if stop_loss_input == 'y':
        stop_loss_enabled = True
        break
    elif stop_loss_input == 'n':
        stop_loss_enabled = False
        break
    else:
        print(Fore.RED + "Vui lòng nhập 'y' hoặc 'n'" + Style.RESET_ALL)

stop_loss_amount = 0
take_profit_amount = 0

if stop_loss_enabled:
    stop_loss_amount = int(input(Fore.YELLOW + "Nhập số BUILD dừng lỗ (VD: 100): "))
    take_profit_amount = int(input(Fore.YELLOW + "Nhập số BUILD dừng lời (VD: 200): "))

# Cài đặt gấp cược
print(Fore.CYAN + "\n=== CÀI ĐẶT GẤP CƯỢC ===" + Style.RESET_ALL)
while True:
    martingale_input = input(Fore.YELLOW + "Bật gấp cược khi thua? (y/n): ").strip().lower()
    if martingale_input == 'y':
        martingale_enabled = True
        break
    elif martingale_input == 'n':
        martingale_enabled = False
        break
    else:
        print(Fore.RED + "Vui lòng nhập 'y' hoặc 'n'" + Style.RESET_ALL)

# Cài đặt hệ số gấp khi thua
if martingale_enabled:
    print(Fore.CYAN + "\n=== CÀI ĐẶT HỆ SỐ GẤP CƯỢC ===" + Style.RESET_ALL)
    print(Fore.WHITE + "Hệ số gấp mặc định: Lần 1: x15, Lần 2: x20, Lần 3: x15" + Style.RESET_ALL)
    while True:
        custom_input = input(Fore.YELLOW + "Tùy chỉnh hệ số gấp? (y/n): ").strip().lower()
        if custom_input == 'y':
            custom_multiplier = True
            break
        elif custom_input == 'n':
            custom_multiplier = False
            break
        else:
            print(Fore.RED + "Vui lòng nhập 'y' hoặc 'n'" + Style.RESET_ALL)

    multiplier_1 = 15
    multiplier_2 = 20
    multiplier_3 = 15

    if custom_multiplier:
        multiplier_1 = float(input(Fore.YELLOW + "Nhập hệ số gấp lần 1 (mặc định 15): ") or "15")
        multiplier_2 = float(input(Fore.YELLOW + "Nhập hệ số gấp lần 2 (mặc định 20): ") or "20")
        multiplier_3 = float(input(Fore.YELLOW + "Nhập hệ số gấp lần 3 (mặc định 15): ") or "15")
else:
    custom_multiplier = False
    multiplier_1 = 1
    multiplier_2 = 1
    multiplier_3 = 1

# Cài đặt phân tích dự đoán
print(Fore.CYAN + "\n=== CÀI ĐẶT PHÂN TÍCH DỰ ĐOÁN ===" + Style.RESET_ALL)
while True:
    prediction_input = input(Fore.YELLOW + "Bật phân tích dự đoán kết quả? (y/n): ").strip().lower()
    if prediction_input == 'y':
        prediction_enabled = True
        break
    elif prediction_input == 'n':
        prediction_enabled = False
        break
    else:
        print(Fore.RED + "Vui lòng nhập 'y' hoặc 'n'" + Style.RESET_ALL)

cuoc_ban_dau = amount
so_du_ban_dau = 0
tool_running = True  # Biến điều khiển việc dừng tool
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Biến lưu trữ lịch sử kết quả để phân tích
history_results = []
last_checked_issue = None
so_du_truoc_cuoc = 0  # Số dư trước khi đặt cược

def print_colored_ascii_art(text):
    ascii_art = pyfiglet.figlet_format(text)
    lines = ascii_art.splitlines()
    for i, line in enumerate(lines):
        print(colors[i % len(colors)] + line + Style.RESET_ALL)

url = f"https://user.3games.io/user/regist?is_cwallet=1&is_mission_setting=true&version=&time={current_time}"
api_10_van = f"https://api.escapemaster.net/escape_game/recent_10_issues?asset=BUILD"
api_100_van = f"https://api.escapemaster.net/escape_game/recent_100_issues?asset=BUILD"
api_cuoc = "https://api.escapemaster.net/escape_game/bet"
api_my_joined = "https://api.escapemaster.net/escape_game/my_joined?asset=BUILD&page=1&page_size=10"

headers = {
    "user-id": user_id,
    "user-login": user_login,
    "user-secret-key": user_secret_key,
    "accept": "*/*",
    "accept-language": "vi,en;q=0.9",
    "country-code": "vn",
    "origin": "https://xworld.info",
    "priority": "u=1, i",
    "referer": "https://xworld.info/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "xb-language": "vi-VN",
    "Content-Type": "application/json"
}

def Login():
    global so_du_ban_dau
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                username = data["data"]["username"]
                ctoken_contribute = data["data"]["cwallet"]["ctoken_contribute"]
                # Không làm tròn, giữ nguyên số thập phân
                print(Fore.GREEN + f"Username: {username}")
                so_du_ban_dau = ctoken_contribute
                print(Fore.GREEN + f"Số Dư: {ctoken_contribute:.2f} BUILD" + Style.RESET_ALL)
                print(Fore.CYAN + f"🔍 Debug: Đã lưu so_du_ban_dau = {so_du_ban_dau:.2f}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Đăng nhập không thành công" + Style.RESET_ALL)
                print(Fore.RED + f"Ctrl C để dừng tool" + Style.RESET_ALL)
                return
        else:
            print(f"Lỗi mạng")
    except requests.RequestException as e:
        print(f"Lỗi không xác định")

def tong_loi_lo():
    global tool_running
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                ctoken_contribute = data["data"]["cwallet"]["ctoken_contribute"]
                # Tính toán lời/lỗ thực tế (không tính tiền đặt cược hiện tại)
                loi_lo = ctoken_contribute - so_du_ban_dau
                
                # Debug: hiển thị thông tin tính toán
                print(Fore.CYAN + f"🔍 Debug: Số dư hiện tại={ctoken_contribute:.2f}, Số dư ban đầu={so_du_ban_dau:.2f}, Chênh lệch={loi_lo:.2f}" + Style.RESET_ALL)

                # Kiểm tra Stop Loss/Take Profit
                if stop_loss_enabled:
                    if loi_lo <= -stop_loss_amount:
                        print(Fore.RED + f"🛑 ĐÃ ĐẠT STOP LOSS: {loi_lo:.2f} BUILD" + Style.RESET_ALL)
                        print(Fore.RED + f"🛑 DỪNG TOOL TỰ ĐỘNG!" + Style.RESET_ALL)
                        tool_running = False
                        return
                    elif loi_lo >= take_profit_amount:
                        print(Fore.GREEN + f"🎯 ĐÃ ĐẠT TAKE PROFIT: {loi_lo:.2f} BUILD" + Style.RESET_ALL)
                        print(Fore.GREEN + f"🎯 DỪNG TOOL TỰ ĐỘNG!" + Style.RESET_ALL)
                        tool_running = False
                        return

                print(Fore.CYAN + f"💰 Số dư hiện tại: {ctoken_contribute:.2f} BUILD" + Style.RESET_ALL)
                print(Fore.CYAN + f"💰 Số dư ban đầu: {so_du_ban_dau:.2f} BUILD" + Style.RESET_ALL)
                
                # Hiển thị lời/lỗ thực tế (không tính tiền đặt cược hiện tại)
                if loi_lo >= 0:
                    print(Fore.GREEN + f"📊 TỔNG THỂ: +{loi_lo:.2f} BUILD (LỜI)" + Style.RESET_ALL)
                else:
                    # Kiểm tra xem có phải do tiền đặt cược hiện tại không
                    if abs(loi_lo) <= amount:
                        print(Fore.YELLOW + f"📊 TỔNG THỂ: {loi_lo:.2f} BUILD (TIỀN CƯỢC HIỆN TẠI)" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"📊 TỔNG THỂ: {loi_lo:.2f} BUILD (LỖ)" + Style.RESET_ALL)
        else:
            print(f"Lỗi mạng")
    except requests.RequestException as e:
        print(f"Lỗi không xác định: {e}")

def phan_tich_lich_su():
    """Phân tích lịch sử 100 ván gần nhất để dự đoán"""
    global history_results
    try:
        response = requests.get(api_100_van, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                issues = data.get("data", [])
                history_results = []
                
                room_mapping = {
                    1: "Nhà Kho",
                    2: "Phòng Họp", 
                    3: "Phòng Giám Đốc",
                    4: "Phòng Trò Chuyện",
                    5: "Phòng Giám Sát",
                    6: "Văn Phòng",
                    7: "Phòng Tài Vụ",
                    8: "Phòng Nhân Sự"
                }
                
                # Kiểm tra và xử lý từng issue
                for issue in issues:
                    try:
                        # Kiểm tra xem issue có phải là dictionary không
                        if isinstance(issue, dict) and "killed_room_id" in issue:
                            room_id = issue["killed_room_id"]
                            room_name = room_mapping.get(room_id, "Không xác định")
                            history_results.append(room_name)
                        else:
                            continue
                    except Exception as e:
                        print(Fore.YELLOW + f"Lỗi xử lý issue: {e}" + Style.RESET_ALL)
                        continue
                
                if not history_results:
                    return None
                
                # Phân tích tần suất xuất hiện
                room_counts = Counter(history_results)
                total_games = len(history_results)
                
                print(Fore.CYAN + "\n=== PHÂN TÍCH LỊCH SỬ 100 VÁN GẦN NHẤT ===" + Style.RESET_ALL)
                for room, count in room_counts.most_common():
                    percentage = (count / total_games) * 100
                    print(Fore.WHITE + f"{room}: {count} lần ({percentage:.1f}%)" + Style.RESET_ALL)
                
                # Tìm phòng có tần suất thấp nhất (có thể sẽ xuất hiện tiếp theo)
                least_frequent_room = min(room_counts.items(), key=lambda x: x[1])
                print(Fore.YELLOW + f"\n🔮 Dự đoán: {least_frequent_room[0]} có thể xuất hiện tiếp theo (ít xuất hiện nhất)" + Style.RESET_ALL)
                
                return least_frequent_room[0]
            else:
                print(Fore.RED + f"Lỗi API: {data.get('message', 'Không xác định')}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Lỗi HTTP: {response.status_code}" + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"Lỗi phân tích lịch sử: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Lỗi không xác định: {e}" + Style.RESET_ALL)
    return None

def kiem_tra_ket_qua_cuoc():
    """Kiểm tra kết quả cược vừa đặt"""
    global last_checked_issue, chuoi_thang, so_du_truoc_cuoc
    
    # Thử kiểm tra kết quả tối đa 5 lần với delay
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response = requests.get(api_my_joined, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("code") == 0:
                        items = data.get("data", {}).get("items", [])
                        if items:
                            latest_bet = items[0]  # Cược gần nhất
                            issue_id = latest_bet.get("issue_id")
                            bet_amount = latest_bet.get("bet_amount", 0)
                            enter_room_id = latest_bet.get("enter_room_id")
                            enter_room = latest_bet.get("enter_room", "Không xác định")
                            killed_room_id = latest_bet.get("killed_room_id")
                            killed_room = latest_bet.get("killed_room", "Không xác định")
                            
                            # Tính toán kết quả - LOGIC ĐÚNG
                            if enter_room_id == killed_room_id:
                                result = "lose"  # Vào phòng sát thủ vào = THUA (bị giết)
                            else:
                                result = "win"   # Vào phòng khác = THẮNG (sống sót)
                            
                            # Debug: hiển thị thông tin chi tiết
                            # print(Fore.CYAN + f"🔍 Debug: Bạn vào ID={enter_room_id}, Sát thủ vào ID={killed_room_id}, Kết quả={result}" + Style.RESET_ALL)
                            
                            # Chỉ kiểm tra nếu là ván mới hoặc có kết quả
                            if issue_id != last_checked_issue:
                                last_checked_issue = issue_id
                                
                                # Thêm delay để đợi kết quả của vòng vừa đặt cược
                                time.sleep(2)
                                
                                # Hiển thị thông tin sát thủ
                                print(Fore.LIGHTYELLOW_EX + f"🔪 Sát thủ vào: {killed_room}" + Style.RESET_ALL)
                                
                                # Hiển thị phòng đặt cược thay vì phòng kết quả
                                room_mapping_reverse = {
                                    1: "Nhà Kho",
                                    2: "Phòng Họp", 
                                    3: "Phòng Giám Đốc",
                                    4: "Phòng Trò Chuyện",
                                    5: "Phòng Giám Sát",
                                    6: "Văn Phòng",
                                    7: "Phòng Tài Vụ",
                                    8: "Phòng Nhân Sự"
                                }
                                
                                # Lấy room_id từ last_checked_issue để hiển thị phòng đặt cược
                                try:
                                    response_bet = requests.get(api_my_joined, headers=headers, timeout=5)
                                    if response_bet.status_code == 200:
                                        bet_data = response_bet.json()
                                        if bet_data.get("code") == 0:
                                            bet_items = bet_data.get("data", {}).get("items", [])
                                            if bet_items:
                                                bet_room_id = bet_items[0].get("enter_room_id")
                                                bet_room_name = room_mapping_reverse.get(bet_room_id, "Không xác định")
                                                print(Fore.LIGHTBLUE_EX + f"🎯 Bạn đặt cược vào: {bet_room_name}" + Style.RESET_ALL)
                                            else:
                                                print(Fore.LIGHTBLUE_EX + f"🎯 Bạn vào: {enter_room}" + Style.RESET_ALL)
                                        else:
                                            print(Fore.LIGHTBLUE_EX + f"🎯 Bạn vào: {enter_room}" + Style.RESET_ALL)
                                    else:
                                        print(Fore.LIGHTBLUE_EX + f"🎯 Bạn vào: {enter_room}" + Style.RESET_ALL)
                                except:
                                    print(Fore.LIGHTBLUE_EX + f"🎯 Bạn vào: {enter_room}" + Style.RESET_ALL)
                                
                                # Tính toán kết quả ván cụ thể trước
                                try:
                                    # Thêm delay để đảm bảo số dư đã được cập nhật
                                    time.sleep(1)
                                    
                                    response_balance = requests.get(url, headers=headers, timeout=5)
                                    if response_balance.status_code == 200:
                                        balance_data = response_balance.json()
                                        if balance_data.get("code") == 200:
                                            so_du_sau_cuoc = balance_data["data"]["cwallet"]["ctoken_contribute"]
                                            ket_qua_van = so_du_sau_cuoc - so_du_truoc_cuoc
                                            
                                            # SỬA: Sử dụng logic game thay vì chênh lệch số dư
                                            # Chênh lệch -1.00 là tiền đặt cược, không phải kết quả thắng/thua
                                            actual_result = result  # Sử dụng logic game
                                            
                                            if actual_result == "win":
                                                print(Fore.GREEN + f"💰 Ván này THẮNG: +{bet_amount:.2f} BUILD" + Style.RESET_ALL)
                                            else:
                                                print(Fore.RED + f"💰 Ván này THUA: -{bet_amount:.2f} BUILD" + Style.RESET_ALL)
                                                
                                except Exception as e:
                                    print(Fore.RED + f"❌ Lỗi tính toán số dư: {e}" + Style.RESET_ALL)
                                    actual_result = result  # Fallback về logic cũ
                                
                                # Cập nhật chuỗi thắng dựa trên kết quả thực tế
                                if actual_result == "win":
                                    chuoi_thang += 1
                                    print(Fore.LIGHTMAGENTA_EX + f"Chuỗi thắng liên tiếp hiện tại: {chuoi_thang} ván" + Style.RESET_ALL)
                                elif actual_result == "lose":
                                    chuoi_thang = 0
                                    print(Fore.LIGHTMAGENTA_EX + f"Chuỗi thắng liên tiếp hiện tại: {chuoi_thang} ván" + Style.RESET_ALL)
                                
                                tong_loi_lo()
                                return True
                            else:
                                # Nếu chưa có kết quả mới, đợi thêm
                                if attempt < max_attempts - 1:
                                    time.sleep(1)
                                    continue
                                else:
                                    print(Fore.YELLOW + "⏳ Chưa có kết quả mới, đợi vòng tiếp theo..." + Style.RESET_ALL)
                                    return False
                        else:
                            if attempt == 0:
                                print(Fore.YELLOW + "⏳ Chưa có dữ liệu cược, đang chờ..." + Style.RESET_ALL)
                            time.sleep(0.5)
                            continue
                    else:
                        error_msg = data.get('msg', 'Không xác định')
                        print(Fore.RED + f"Lỗi API: {error_msg}" + Style.RESET_ALL)
                        
                        # Nếu lỗi login, thử refresh session
                        if data.get("code") == 1004 and "Must login" in error_msg:
                            print(Fore.YELLOW + "🔄 Đang thử refresh session..." + Style.RESET_ALL)
                            if refresh_session():
                                # Thử lại request sau khi refresh
                                continue
                        
                        if attempt == max_attempts - 1:
                            print(Fore.CYAN + f"🔍 Debug API Response: {data}" + Style.RESET_ALL)
                        break
                except Exception as json_error:
                    print(Fore.RED + f"Lỗi parse JSON: {json_error}" + Style.RESET_ALL)
                    if attempt == max_attempts - 1:
                        print(Fore.CYAN + f"🔍 Debug Raw Response: {response.text}" + Style.RESET_ALL)
                    break
            else:
                print(Fore.RED + f"Lỗi HTTP: {response.status_code}" + Style.RESET_ALL)
                if attempt == max_attempts - 1:
                    print(Fore.CYAN + f"🔍 Debug Response: {response.text}" + Style.RESET_ALL)
                break
                
        except requests.RequestException as e:
            print(Fore.RED + f"Lỗi kiểm tra kết quả: {e}" + Style.RESET_ALL)
            break
        except Exception as e:
            print(Fore.RED + f"Lỗi không xác định: {e}" + Style.RESET_ALL)
            break
    
    print(Fore.YELLOW + "⚠️ Không thể lấy kết quả sau nhiều lần thử" + Style.RESET_ALL)
    return False

vong_choi = None
chuoi_thang = 0
count_thang = 0

def lich_su():
    global vong_choi
    try:
        response = requests.get(api_10_van, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                room_mapping = {
                    1: "Nhà Kho",
                    2: "Phòng Họp",
                    3: "Phòng Giám Đốc",
                    4: "Phòng Trò Chuyện",
                    5: "Phòng Giám Sát",
                    6: "Văn Phòng",
                    7: "Phòng Tài Vụ",
                    8: "Phòng Nhân Sự"
                }
                issues = data.get("data", [])[:3]
                vong_choi_truoc = issues[0]["issue_id"]
                id_ket_qua_vong_truoc = issues[0]["killed_room_id"]
                ten_phong_vong_truoc = room_mapping.get(id_ket_qua_vong_truoc, "Không xác định")
                vong_choi_hien_tai = issues[0]["issue_id"] + 1
                issue_details = []
                for issue in issues:
                    issue_id = issue["issue_id"]
                    killed_room_id = issue["killed_room_id"]
                    room_name = room_mapping.get(killed_room_id, "Không xác định")
                    issue_details.append(f"Issue ID: {issue_id}, Room: {room_name}")

                if vong_choi_truoc != vong_choi:
                    print(Fore.LIGHTCYAN_EX + f"Vòng chơi hiện tại: #{vong_choi_hien_tai}" + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + f"Kết quả vòng trước: #{vong_choi_truoc} | {ten_phong_vong_truoc}" + Style.RESET_ALL)
                    vong_choi = vong_choi_truoc
                    
                    # Phân tích dự đoán nếu được bật
                    if prediction_enabled:
                        try:
                            predicted_room = phan_tich_lich_su()
                        except Exception as e:
                            print(Fore.RED + f"Lỗi khi phân tích dự đoán: {e}" + Style.RESET_ALL)
                            predicted_room = None
                    
                    kiem_tra_dieu_kien(issue_details)
                    print("----------------------------------------------------")
    except requests.RequestException as e:
        print(Fore.RED + f"Lỗi: {e}" + Style.RESET_ALL)

number_cuoc = 0

def kiem_tra_dieu_kien(issue_details):
    global number_cuoc,amount,cuoc_ban_dau,chuoi_thang,count_thang,tool_running
    room_mapping = {
            "Nhà Kho": 1,
            "Phòng Họp": 2,
            "Phòng Giám Đốc": 3,
            "Phòng Trò Chuyện": 4,
            "Phòng Giám Sát": 5,
            "Văn Phòng": 6,
            "Phòng Tài Vụ": 7,
            "Phòng Nhân Sự": 8
        }
    room_0 = issue_details[0].split(",")[1].split(":")[1].strip()
    room_1 = issue_details[1].split(",")[1].split(":")[1].strip()
    room_2 = issue_details[2].split(",")[1].split(":")[1].strip()
    
    # Debug: hiển thị thông tin issue_details
    print(Fore.CYAN + f"🔍 Debug: room_0={room_0}, room_1={room_1}, room_2={room_2}, number_cuoc={number_cuoc}" + Style.RESET_ALL)
    
    # Nếu bật phân tích dự đoán, ưu tiên dự đoán
    if prediction_enabled and len(history_results) > 0:
        try:
            predicted_room = min(Counter(history_results).items(), key=lambda x: x[1])[0]
            predicted_room_id = room_mapping.get(predicted_room)
            if predicted_room_id:
                print(Fore.MAGENTA + f"🎯 Sử dụng dự đoán: {predicted_room}" + Style.RESET_ALL)
                dat_cuoc(predicted_room_id)
                number_cuoc = 1
                return
        except Exception as e:
            print(Fore.YELLOW + f"Lỗi khi sử dụng dự đoán: {e}" + Style.RESET_ALL)
            print(Fore.YELLOW + "Chuyển sang logic cũ" + Style.RESET_ALL)
    
    if room_0 != room_1 and number_cuoc == 0 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Đặt cược theo : {room_name}" + Style.RESET_ALL)
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    elif room_0 != room_1 and room_0 != room_2 and number_cuoc == 1 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thắng - Đặt cược tiếp: {room_name}" + Style.RESET_ALL)
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    elif room_0 != room_1 and room_0 == room_2 and number_cuoc == 1 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thua - Gấp cược: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        
        if martingale_enabled:
            amount = int(amount * multiplier_1)
            print(Fore.YELLOW + f"💰 Gấp cược x{multiplier_1}: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 2
        else:
            print(Fore.YELLOW + f"💰 Giữ nguyên số tiền cược: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 1
            
        room_id = room_mapping.get(room_name, None)
        print(Fore.CYAN + f"🔍 Debug: Đặt cược room_name={room_name}, room_id={room_id}" + Style.RESET_ALL)
        dat_cuoc(room_id)
        return
    # ---------------------------------------------
    elif room_0 != room_1 and room_0 != room_2 and number_cuoc == 2 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thắng - Reset về cơ bản: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        amount = cuoc_ban_dau
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    elif room_0 != room_1 and room_0 == room_2 and number_cuoc == 2 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thua - Gấp cược lần 2: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        
        if martingale_enabled:
            amount = int(amount * multiplier_2)
            print(Fore.YELLOW + f"💰 Gấp cược x{multiplier_2}: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 3
        else:
            print(Fore.YELLOW + f"💰 Giữ nguyên số tiền cược: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 1
            
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        return
    # ----------------------------------
    elif room_0 != room_1 and room_0 != room_2 and number_cuoc == 3 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thắng - Reset về cơ bản: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        amount = cuoc_ban_dau
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    elif room_0 != room_1 and room_0 == room_2 and number_cuoc == 3 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thua - Gấp cược lần 3: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        
        if martingale_enabled:
            amount = int(amount * multiplier_3)
            print(Fore.YELLOW + f"💰 Gấp cược x{multiplier_3}: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 4
        else:
            print(Fore.YELLOW + f"💰 Giữ nguyên số tiền cược: {amount:.2f} BUILD" + Style.RESET_ALL)
            number_cuoc = 1
            
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        return
    # --------------------------------------
    elif room_0 != room_1 and room_0 != room_2 and number_cuoc == 4 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Thắng - Reset về cơ bản: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        
        if martingale_enabled:
            amount = cuoc_ban_dau
            print(Fore.YELLOW + f"💰 Reset về số tiền ban đầu: {amount:.2f} BUILD" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"💰 Giữ nguyên số tiền cược: {amount:.2f} BUILD" + Style.RESET_ALL)
            
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    elif room_0 != room_1 and room_0 == room_2 and number_cuoc == 4 :
        room_name = issue_details[1].split(",")[1].split(":")[1].strip()
        print(Fore.CYAN + f"🎯 Đã đạt gấp cược tối đa - Reset: {room_name}" + Style.RESET_ALL)
        if not tool_running:
            return
        
        if martingale_enabled:
            amount = cuoc_ban_dau
            print(Fore.YELLOW + f"💰 Reset về số tiền ban đầu: {amount:.2f} BUILD" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"💰 Giữ nguyên số tiền cược: {amount:.2f} BUILD" + Style.RESET_ALL)
            
        room_id = room_mapping.get(room_name, None)
        dat_cuoc(room_id)
        number_cuoc = 1
        return
    # ---------------------------
    elif room_0 == room_1 :
        print(Fore.RED + f"Phát hiện sát thủ vào 1 phòng liên tục !" + Style.RESET_ALL)
        if not tool_running:
            return
        print(Fore.LIGHTMAGENTA_EX + f"Chuỗi thắng liên tiếp hiện tại: {chuoi_thang} ván" + Style.RESET_ALL)

def dat_cuoc(room_id):
    global so_du_truoc_cuoc
    
    # Debug: hiển thị thông tin đặt cược
    room_mapping_debug = {
        1: "Nhà Kho",
        2: "Phòng Họp", 
        3: "Phòng Giám Đốc",
        4: "Phòng Trò Chuyện",
        5: "Phòng Giám Sát",
        6: "Văn Phòng",
        7: "Phòng Tài Vụ",
        8: "Phòng Nhân Sự"
    }
    room_name_debug = room_mapping_debug.get(room_id, "Không xác định")
    print(Fore.CYAN + f"🔍 Debug: Đặt cược room_id={room_id}, room_name={room_name_debug}" + Style.RESET_ALL)
    
    body = {
        "asset_type": "BUILD",
        "bet_amount": amount,
        "room_id": room_id,
        "user_id": headers["user-id"]
    }
    
    # Lưu số dư trước khi đặt cược
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                so_du_truoc_cuoc = data["data"]["cwallet"]["ctoken_contribute"]
    except:
        pass
    
    # Thử đặt cược tối đa 3 lần
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(api_cuoc, headers=headers, json=body, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("code") == 0:
                        print(Fore.GREEN + f"✅ Cược thành công {amount:.2f} BUILD (lần thử {attempt + 1})" + Style.RESET_ALL)
                        # Kiểm tra kết quả ngay lập tức
                        kiem_tra_ket_qua_cuoc()
                        return True
                    else:
                        error_msg = data.get("message", "Không xác định")
                        print(Fore.YELLOW + f"⚠️ Lần {attempt + 1}: {error_msg}" + Style.RESET_ALL)
                        # Debug: hiển thị response chi tiết
                        if attempt == max_retries - 1:
                            print(Fore.CYAN + f"🔍 Debug Response: {data}" + Style.RESET_ALL)
                except Exception as json_error:
                    print(Fore.YELLOW + f"⚠️ Lần {attempt + 1}: Lỗi parse JSON - {json_error}" + Style.RESET_ALL)
                    if attempt == max_retries - 1:
                        print(Fore.CYAN + f"🔍 Debug Raw Response: {response.text}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"⚠️ Lần {attempt + 1}: HTTP {response.status_code}" + Style.RESET_ALL)
                if attempt == max_retries - 1:
                    print(Fore.CYAN + f"🔍 Debug Response: {response.text}" + Style.RESET_ALL)
                
        except requests.RequestException as e:
            print(Fore.YELLOW + f"⚠️ Lần {attempt + 1}: Lỗi mạng - {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Lần {attempt + 1}: Lỗi không xác định - {e}" + Style.RESET_ALL)
        
        # Đợi 1 giây trước khi thử lại (trừ lần cuối)
        if attempt < max_retries - 1:
            time.sleep(1)
    
    print(Fore.RED + f"❌ Không thể đặt cược sau {max_retries} lần thử!" + Style.RESET_ALL)
    return False

def refresh_session():
    """Refresh session khi bị lỗi login"""
    global headers
    try:
        # Thử đăng nhập lại
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                print(Fore.GREEN + "✅ Session đã được refresh thành công!" + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + f"❌ Không thể refresh session: {data.get('message', 'Lỗi')}" + Style.RESET_ALL)
                return False
        else:
            print(Fore.RED + f"❌ Lỗi HTTP khi refresh: {response.status_code}" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi refresh session: {e}" + Style.RESET_ALL)
        return False

def test_api_connection():
    """Test kết nối API trước khi chạy tool"""
    print(Fore.CYAN + "\n=== KIỂM TRA KẾT NỐI API ===" + Style.RESET_ALL)
    
    # Test API đăng nhập
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                print(Fore.GREEN + "✅ API đăng nhập: OK" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"❌ API đăng nhập: {data.get('message', 'Lỗi')}" + Style.RESET_ALL)
                return False
        else:
            print(Fore.RED + f"❌ API đăng nhập: HTTP {response.status_code}" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"❌ API đăng nhập: {e}" + Style.RESET_ALL)
        return False
    
    # Test API lịch sử
    try:
        response = requests.get(api_10_van, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                print(Fore.GREEN + "✅ API lịch sử: OK" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"❌ API lịch sử: {data.get('message', 'Lỗi')}" + Style.RESET_ALL)
                return False
        else:
            print(Fore.RED + f"❌ API lịch sử: HTTP {response.status_code}" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"❌ API lịch sử: {e}" + Style.RESET_ALL)
        return False
    
    # Test API my_joined
    try:
        response = requests.get(api_my_joined, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                print(Fore.GREEN + "✅ API my_joined: OK" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"❌ API my_joined: {data.get('message', 'Lỗi')}" + Style.RESET_ALL)
                return False
        else:
            print(Fore.RED + f"❌ API my_joined: HTTP {response.status_code}" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"❌ API my_joined: {e}" + Style.RESET_ALL)
        return False
    
    print(Fore.GREEN + "🎉 Tất cả API đều hoạt động tốt!" + Style.RESET_ALL)
    return True

if __name__ == "__main__":
    clear_screen()

    print(Fore.CYAN + "\n=== CÀI ĐẶT HIỆN TẠI ===" + Style.RESET_ALL)
    print(Fore.WHITE + f"Số tiền cược ban đầu: {cuoc_ban_dau:.2f} BUILD" + Style.RESET_ALL)
    if stop_loss_enabled:
        print(Fore.WHITE + f"Stop Loss: -{stop_loss_amount} BUILD" + Style.RESET_ALL)
        print(Fore.WHITE + f"Take Profit: +{take_profit_amount} BUILD" + Style.RESET_ALL)
    else:
        print(Fore.WHITE + "Stop Loss/Take Profit: TẮT" + Style.RESET_ALL)

    print(Fore.WHITE + f"Gấp cược: {'BẬT' if martingale_enabled else 'TẮT'}" + Style.RESET_ALL)
    if martingale_enabled:
        print(Fore.WHITE + f"Hệ số gấp: x{multiplier_1} | x{multiplier_2} | x{multiplier_3}" + Style.RESET_ALL)
    print(Fore.WHITE + f"Phân tích dự đoán: {'BẬT' if prediction_enabled else 'TẮT'}" + Style.RESET_ALL)
    print(Fore.CYAN + "=========================" + Style.RESET_ALL)

    Login()

    if not test_api_connection():
        print(Fore.RED + "❌ Có lỗi với API, vui lòng kiểm tra lại thông tin đăng nhập!" + Style.RESET_ALL)
        input("Nhấn Enter để thoát...")
        exit()

    if prediction_enabled:
        try:
            phan_tich_lich_su()
        except Exception as e:
            print(Fore.RED + f"Lỗi khi phân tích lịch sử ban đầu: {e}" + Style.RESET_ALL)
            print(Fore.YELLOW + "Tool sẽ tiếp tục chạy với logic cũ" + Style.RESET_ALL)

    try:
        while tool_running:
            lich_su()
            if not tool_running:
                print(Fore.YELLOW + "\n🛑 Tool đã dừng do đạt điều kiện Stop Loss/Take Profit!" + Style.RESET_ALL)
                break
            time.sleep(15)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n🛑 Tool đã dừng bởi người dùng (Ctrl+C)" + Style.RESET_ALL)
