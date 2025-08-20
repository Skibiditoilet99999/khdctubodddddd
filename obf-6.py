#!/usr/bin/env python3

try:

    import requests, time, os, re, json, sys

    from rich import print as println
    
    from pystyle import Colors,Colorate,Center

    import platform

    import random

    from rich.console import Console

    from rich.panel import Panel

    from fake_useragent import UserAgent

except ModuleNotFoundError:

    print("Required modules are not installed. Please run 'pip install -r requirements.txt'.")

    sys.exit(1)



BASE_URL = "https://socioblend.com"

SUCCESS, FAILED, DELAY = [], [], {

    "TIME": 0

}

CONSOLE = Console()


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

    # Banner ASCII     # Tool by phước, Không xóa dòng này để tôn trọng tác giả.
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



    


class SubmitTikTokViews:



    def __init__(self, video_url: str) -> None:

        """Initialize the SubmitTikTokViews class."""

        self.video_url = video_url

        self.session = requests.Session()



    def RetrieveCookies(self) -> str:

        """Retrieve cookies from the session."""

        self.session.headers = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",

            "Accept-Encoding": "gzip, deflate",

            "Accept-Language": "en-US,en;q=0.9",

            "Connection": "keep-alive",

            "Host": "socioblend.com",

            "Sec-Fetch-Dest": "document",

            "Sec-Fetch-Mode": "navigate",

            "Sec-Fetch-Site": "none",

            "Sec-Fetch-User": "?1",

            "Upgrade-Insecure-Requests": "1",

            "User-Agent": f"{UserAgent().random}"

        }

        response = self.session.get(f"{BASE_URL}/free-tiktok-views", verify=True, allow_redirects=True)



        cookies_string = "; ".join([f"{key}={value}" for key, value in self.session.cookies.get_dict().items()])



        return cookies_string

    

    def SubmitForm(self, cookies: str) -> None:

        """Submit the form with the video URL and cookies."""

        global SUCCESS, FAILED, DELAY

        data = {

            "video_url": f"{self.video_url}",

        }

        self.session.headers.update(

            {

                "Content-Length": f"{len(json.dumps(data))}",

                "Content-Type": "application/x-www-form-urlencoded",

                "Sec-Fetch-Site": "same-origin",

                "Sec-Fetch-Mode": "cors",

                "Cookie": f"{cookies}",

                "Accept": "*/*",

                "Sec-Fetch-Dest": "empty",

                "Origin": f"{BASE_URL}",

                "Referer": f"{BASE_URL}/free-tiktok-views",

            }

        )



        response = self.session.post(f"{BASE_URL}/submit-tiktok.php", data=data, verify=True, allow_redirects=False)

        if '"status":"success"' in response.text:

            SUCCESS.append(f"{response.status_code} - {response.reason}")

            CONSOLE.print(

                Panel(f"""[bold white]Status:[bold green] Đã gửi view thành công!  🤑🤑🤑

[bold white]Link:[bold red] {self.video_url}

[bold white]Views:[bold yellow] +1000""", width=59, style="bold bright_black", title="[bold bright_black]> [Successfully] <")

            )

        elif '"retry_after"' in response.text:

            retry_after = re.search(r'"retry_after":(\d+)', response.text)

            if retry_after: DELAY["TIME"] = int(retry_after.group(1))

        elif 'The URL you entered is not a valid TikTok video link.' in response.text:

            CONSOLE.print(

                Panel("[bold red]URL bạn nhập không phải là liên kết video TikTok hợp lệ. Vui lòng kiểm tra lại liên kết.", width=59, style="bold bright_black", title="[bold bright_black]> [Invalid Link] <")

            )

            sys.exit(1)

        else:

            FAILED.append(f"{response.status_code} - {response.reason}")

            println(f"[bold bright_black]   ╰─>[bold red] THẤT BẠI KHI BUFF VIEW!             ", end="\r")

            time.sleep(5)



        return None



def Main() -> None:

    """Main function to run the script."""

    os.system("clear" if os.name == "posix" else "cls")

    banner()

    CONSOLE.print(

        Panel(f"[bold yellow]Vui lòng nhập liên kết video TikTok của bạn. Hãy nhớ kiểm tra liên kết trước khi nhấn enter.\nTôi khuyên bạn nên lấy liên kết từ trình duyệt của mình!", width=59, style="bold bright_red", title="[bold bright_black]> [Tiktok Link] <", subtitle="[bold bright_black]╭──────", subtitle_align="left")

    )

    video_url = CONSOLE.input("[bold bright_red]   ╰─> ").strip()

    if video_url.startswith("https://www.tiktok.com/@") or video_url.startswith("https://tiktok.com/@"):

        CONSOLE.print(

            Panel("[bold white]Vui lòng đợi một lát..., Bạn có thể sử dụng[bold red] CTRL + Z[bold white] để dừng tool hoặc [bold yellow] CTRL + C[bold white] nếu bị treo!", width=59, style="bold bright_black", title="[bold bright_black]> [Processing] <")

        )

        time.sleep(2)

        while True:

            try:

                if DELAY["TIME"] != 0:

                    for timer in range(DELAY["TIME"], 0, -1):

                        println(f"[bold bright_black]   ╰─>[bold white] BẮT ĐẦU[bold green] {timer}[bold white]/[bold green]{DELAY['TIME']}[bold white] THÀNH CÔNG:-[bold green]{len(SUCCESS)}[bold white] THẤT BẠI:-[bold red]{len(FAILED)}     ", end="\r")

                        time.sleep(1)

                    DELAY["TIME"] = 0

                    println(f"[bold bright_black]   ╰─>[bold yellow] BẮT ĐẦU GỬI TIẾP!                            ", end="\r")

                    time.sleep(5)

                    continue

                println(f"[bold bright_black]   ╰─>[bold green] BUFF THÀNH CÔNG!               ", end="\r")

                time.sleep(2)



                submitter = SubmitTikTokViews(video_url)

                cookies = submitter.RetrieveCookies()

                submitter.SubmitForm(cookies)

            except requests.exceptions.RequestException:

                println(f"[bold bright_black]   ╰─>[bold red] KẾT NỐI CỦA BẠN ĐANG GẶP SỰ CỐ!!     ", end="\r")

                time.sleep(10)

                continue

            except KeyboardInterrupt:

                continue

            except Exception as e:

                println(f"[bold bright_black]   ╰─>[bold red] {str(e).upper()}!", end="\r")

                time.sleep(5)

                continue

    else:

        CONSOLE.print(

            Panel("[bold red]Rất tiếc, bạn đã nhập sai liên kết video TikTok. Vui lòng thử lại theo định dạng https://www.tiktok.com/@... Hoặc vào checkshorturl.com để thử lại...", width=59, style="bold bright_black", title="[bold bright_black]> [Wrong Link] <")

        )

        sys.exit(1)


Main()
