import requests
import time
import os

API_URL = "http://apihoangthanhtung.ddns.net:5000"
API_KEY = "buoi"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    print("=" * 50)
    print("🚀 TOOL BUFF TIKTOK - BVTOOL 🚀")
    print("Tool Buff by HTT")
    print("=" * 50)

def main():
    while True:
        clear()
        banner()

        link = input("🔗 Nhap link TikTok: ").strip()
        print("\nChon loai buff:")
        print("1. 💗 Buff Tym")
        print("2. 👁️ Buff View")
        choice = input("👉 Nhap lua chon (1 hoac 2): ").strip()

        if choice == "1":
            action = "tym"
        elif choice == "2":
            action = "view"
        else:
            print("❌ Lua chon khong hop le!")
            time.sleep(2)
            continue

        full_url = f"{API_URL}/web={link}/{action}?key={API_KEY}"
        print("\n🔄 Đang gui yeu cau...")

        try:
            res = requests.get(full_url, timeout=10)
            data = res.json()
            print("\n📦 Ket qua:")
            for k, v in data.items():
                print(f"🔹 {k.capitalize()}: {v}")
        except Exception as e:
            print(f"❌ Loi ket noi: {e}")

        again = input("\n↩️ Buff tiep? (y/n): ").lower()
        if again != "y":
            print("👋 Tam biet!")
            break

if __name__ == "__main__":
    main()

