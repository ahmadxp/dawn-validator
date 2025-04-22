import aiohttp
import asyncio
import json
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

GETPOINT_URL = "https://ext-api.dawninternet.com/api/atom/v1/userreferral/getpoint?appid="
KEEPALIVE_URL = "https://ext-api.dawninternet.com/chromeapi/dawn/v1/userreward/keepalive?appid="

EXTENSION_ID = "fpdkjdnhkakefebpekbdhillbhonfjjp"
VERSION = "1.1.5"

HEADERS_TEMPLATE = {
    "Origin": f"chrome-extension://{EXTENSION_ID}",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

def now():
    return datetime.now().strftime("%H:%M:%S")

async def get_point(session, appid, token):
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {token}"

    try:
        async with session.get(GETPOINT_URL + appid, headers=headers, timeout=30) as resp:
            if resp.status != 200:
                return None
            return await resp.json()
    except Exception:
        return None

async def send_keepalive(session, appid, token, email):
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {token}"

    payload = {
        "username": email,
        "extensionid": EXTENSION_ID,
        "numberoftabs": 0,
        "_v": VERSION
    }

    try:
        async with session.post(KEEPALIVE_URL + appid, headers=headers, json=payload, timeout=30) as resp:
            data = await resp.json()
            message = data.get("data", {}).get("message") or data.get("message", "")
            if data.get("success"):
                print(f"[{now()}] [{email}] " + Fore.GREEN + f"KEEPALIVE: {message}")
                return True
            else:
                print(f"[{now()}] [{email}] " + Fore.YELLOW + "KEEPALIVE: Invalid response")
                return False
    except Exception as e:
        print(f"[{now()}] [{email}] " + Fore.RED + f"Something wrong! Error: {str(e)[:3]} Bad Gateway")
        return False

async def monitor(account, proxy=None):
    appid = account["appid"]
    token = account["token"]

    conn = aiohttp.TCPConnector(ssl=False)
    session_args = {"connector": conn}
    if proxy:
        session_args["proxy"] = proxy

    async with aiohttp.ClientSession(**session_args) as session:
        email = "-"
        while True:
            resp = await get_point(session, appid, token)
            if resp and isinstance(resp, dict) and resp.get("status"):
                data = resp.get("data")
                if data and isinstance(data, dict):
                    referral = data.get("referralPoint")
                    if referral and isinstance(referral, dict):
                        email = referral.get("email", "-")
                        break
            print(Fore.RED + f"[ERROR] Failed to fetch initial data (appid: {appid}), retrying in 15 seconds...")
            await asyncio.sleep(15)

        proxy_info = f"Proxy {proxy}" if proxy else "No Proxy"
        print(f"[MONITOR] Active for {email} ~ {proxy_info}")

        while True:
            await send_keepalive(session, appid, token, email)

            point_resp = await get_point(session, appid, token)
            if point_resp and point_resp.get("status"):
                referral = point_resp["data"]["referralPoint"]
                reward = point_resp["data"]["rewardPoint"]

                commission = referral.get("commission", 0)
                total_points = (
                    commission +
                    reward.get("points", 0) +
                    reward.get("registerpoints", 0) +
                    reward.get("signinpoints", 0) +
                    reward.get("twitter_x_id_points", 0) +
                    reward.get("discordid_points", 0) +
                    reward.get("telegramid_points", 0)
                )
                print(f"[{now()}] [{email}] " + Fore.GREEN + f"Total Points: {total_points}")
            else:
                print(f"[{now()}] [{email}] " + Fore.RED + f"Failed to retrieve point data")

            print(f"[{now()}] [{email}] Waiting 5 minutes\n")
            await asyncio.sleep(300)

async def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Style.BRIGHT + ":: Dawn Validator Bot")
    print("Monitoring & Keepalive Dawn Extension")
    print("Github: https://github.com/ahmadxp/dawn-validator\n")

async def main():
    await banner()
    with open("config.json", "r", encoding="utf-8") as f:
        accounts = json.load(f)

    with open("proxy.json", "r", encoding="utf-8") as f:
        proxy_list = json.load(f)

    tasks = []
    proxy_index = 0
    for account in accounts:
        use_proxy = account.get("proxy", False)
        proxy = None
        if use_proxy:
            if proxy_index < len(proxy_list):
                proxy = proxy_list[proxy_index]
                proxy_index += 1
            else:
                proxy = proxy_list[0] if proxy_list else None
        tasks.append(monitor(account, proxy))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")
