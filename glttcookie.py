import os, time, random, sys, json, re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from colorama import init
from pystyle import Colors, Colorate
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import box
# Bug dc thì bú all đi,a mày cho full suộc đấy ,PHUOC
# ======================= CHROMEDRIVER ===========================
CHROMEDRIVER_PATH = "/data/data/com.termux/files/usr/bin/chromedriver"

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Mobile Safari/537.36",
]

def create_driver(user_agent=None):
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
    chrome_opts.add_argument("--window-size=720,1280")
    chrome_opts.add_argument("--lang=vi-VN")
    chrome_opts.add_argument("--disable-infobars")
    chrome_opts.add_argument("--disable-notifications")
    chrome_opts.add_argument("--disable-popup-blocking")
    chrome_opts.add_argument(f"--user-agent={user_agent or random.choice(USER_AGENTS)}")
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_opts)

# ======================= SETUP ===========================
init(autoreset=True)
console = Console()
def clear(): os.system("clear")

# ======================= BANNER ==========================
def banner():
    clear()
    ascii = """
██████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██╗░░░░░
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
██████╦╝╚██╗░██╔╝░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══██╗░╚████╔╝░░░░██║░░░██║░░██║██║░░██║██║░░░░░
██████╦╝░░╚██╔╝░░░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚═════╝░░░░╚═╝░░░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
"""
    gradient = random.choice([Colors.red_to_yellow, Colors.green_to_cyan,
                               Colors.purple_to_red, Colors.yellow_to_red,
                               Colors.blue_to_purple, Colors.rainbow])
    print(Colorate.Vertical(gradient, ascii))
    print("\n")
banner()

# =================== AUTHORIZATION & TOKEN ===================
def get_auth():
    if os.path.exists("Authorization.txt") and os.path.exists("token.txt"):
        with open("Authorization.txt") as f1, open("token.txt") as f2:
            return f1.read().strip(), f2.read().strip()
    else:
        author = Prompt.ask("[bold yellow]Nhập Authorization[/bold yellow]")
        token = Prompt.ask("[bold yellow]Nhập Token[/bold yellow]")
        open("Authorization.txt","w").write(author)
        open("token.txt","w").write(token)
        return author, token

author, token = get_auth()

headers = {
    'Authorization': author,
    't': token,
    'Content-Type': 'application/json;charset=utf-8',
    'User-Agent': 'Mozilla/5.0',
}
scraper = requests.Session()

# =================== API CLASS ===================
class GolikeAPI:
    def __init__(self, s, h): self.s, self.h = s, h
    def accounts(self):
        try: return self.s.get('https://gateway.golike.net/api/tiktok-account', headers=self.h).json().get("data", [])
        except: return []
    def get_job(self, acc_id):
        try: return self.s.get('https://gateway.golike.net/api/advertising/publishers/tiktok/jobs', headers=self.h, params={'account_id': acc_id}).json().get("data", {})
        except: return {}
    def complete_job(self, ads_id, acc_id):
        try:
            return self.s.post('https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs', headers=self.h, json={'ads_id': ads_id,'account_id': acc_id,'async': True,'data': None}).json()
        except: return {}
    def skip_job(self, ads_id, obj_id, acc_id, job_type):
        try: self.s.post('https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs', headers=self.h, json={'ads_id': ads_id,'object_id': obj_id,'account_id': acc_id,'type': job_type})
        except: pass

# =================== SELENIUM CLASS ===================
class TikTokSelenium:
    def __init__(self, cookie, user_agent=None):
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.driver = create_driver(self.user_agent)
        self.driver.get("https://www.tiktok.com/")
        self.username = None
        self._set_cookie(cookie)

    def _set_cookie(self, cookie):
        time.sleep(3)
        self.driver.delete_all_cookies()
        for ck in cookie.split(";"):
            if "=" in ck:
                n, v = ck.strip().split("=", 1)
                try: self.driver.add_cookie({"name": n, "value": v, "domain": "www.tiktok.com"})
                except: pass
        self.driver.get("https://www.tiktok.com/")
        time.sleep(5)
        if self.is_logged_in():
            self.username = self.get_username()

    def is_logged_in(self):
        return '"uniqueId":"' in self.driver.page_source

    def get_username(self):
        try:
            html = self.driver.page_source
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
            if m:
                data = json.loads(m.group(1))
                return data["props"]["pageProps"]["userInfo"]["user"]["uniqueId"]
        except:
            return None

    def follow(self, link):
        self._interact(link, '//button[contains(@data-e2e,"follow")]')

    def like(self, link):
        self._interact(link, '//span[contains(@class,"like")]')

    def comment(self, link, text):
        self.driver.get(link)
        try:
            area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.DraftEditor-editorContainer'))
            )
            area.send_keys(text)
            area.send_keys(Keys.ENTER)
        except:
            print("[red]❌ Comment fail![/red]")

    def _interact(self, link, xpath):
        self.driver.get(link)
        try:
            btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            time.sleep(random.uniform(2,5))
            btn.click()
        except:
            print("[red]❌ Follow/Like fail![/red]")

    def quit(self):
        self.driver.quit()

# =================== MAIN ===================
api = GolikeAPI(scraper, headers)
accounts = api.accounts()
if not accounts:
    console.print("[red]Không lấy được danh sách acc! Kiểm tra token/Authorization."); sys.exit()

table = Table(title="Danh Sách Acc", box=box.ROUNDED, border_style="cyan")
table.add_column("STT", style="yellow"); table.add_column("Nickname", style="green")
for i,a in enumerate(accounts,1): table.add_row(str(i), a["nickname"])
console.print(table)

chon = int(Prompt.ask("[bold cyan]Chọn acc[/bold cyan]"))
acc = accounts[chon-1]; acc_id, nickname = acc["id"], acc["nickname"]

cookie = Prompt.ask("[bold cyan]Nhập Cookie TikTok[/bold cyan]")
tiktok = TikTokSelenium(cookie)
if not tiktok.is_logged_in():
    console.print("[red]Cookie TikTok không hợp lệ hoặc chưa login![/red]"); tiktok.quit(); sys.exit()
console.print(f"[green]✅ Cookie hợp lệ, đăng nhập thành công! Username: {tiktok.username}[/green]")

delay = int(Prompt.ask("[yellow]Delay (giây)[/yellow]", default="10"))
doiacc = int(Prompt.ask("[yellow]Số lần fail thì đổi acc[/yellow]", default="5"))

dem, tong, fail = 0, 0, 0
while True:
    if fail >= doiacc: console.print("[red]Acc lỗi nhiều, đổi acc khác!"); break
    job = api.get_job(acc_id)
    if not job or "link" not in job:
        console.print("[yellow]Không có job..."); time.sleep(3); fail += 1; continue
    link, loai, ads_id, obj_id = job["link"], job["type"], job["id"], job["object_id"]

    console.print(Panel(f"[bold yellow]Đang làm job: {loai} | Link: {link}[/bold yellow]", border_style="blue"))
    if loai=="follow": tiktok.follow(link)
    elif loai=="like": tiktok.like(link)
    elif loai=="comment": tiktok.comment(link, job.get("message") or job.get("content") or "Hay quá!")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), transient=True) as progress:
        t = progress.add_task("[cyan]Đợi hoàn tất...", total=delay)
        for i in range(delay): time.sleep(1); progress.update(t, advance=1)

    nhantien = api.complete_job(ads_id, acc_id)
    if nhantien.get("status") == 200:
        gia = nhantien["data"].get("price_per_after_cost", 0); dem += 1; tong += gia; fail = 0
        console.print(Panel(f"[green]✅ SUCCESS | +{gia} xu | Tổng: {tong}[/green]", border_style="green"))

        # đổi user agent sau mỗi job thành công
        tiktok.driver.quit()
        new_ua = random.choice(USER_AGENTS)
        tiktok = TikTokSelenium(cookie, user_agent=new_ua)
        console.print(f"[cyan]🔄 Đã đổi User-Agent: {new_ua}[/cyan]")

    else:
        fail += 1; api.skip_job(ads_id, obj_id, acc_id, loai)
        console.print(Panel(f"[red]❌ FAIL | Tổng: {tong}[/red]", border_style="red"))

# Tao cho full suộc đấy,lấy r sửa banner m đi 🤑
