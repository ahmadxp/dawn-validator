# Dawn Validator Bot
DAWN Validator is a Chrome extension that allows you to participate in the DAWN network a decentralized wireless broadband protocol. This bot validates and checks the status of various applications by sending keepalive requests and fetching initial data, ensuring seamless operation through optional proxy support.

### Start Earning
Download and install **Dawn Validator**
[https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp](https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp)

---

## Feature
- Keep alive automation
- Multiple account
- Proxy support
- 1 Account = 1 Proxy
- Log minimalist

## Requirements
- Python 3.7 or higher
- aiohttp
- colorama
- JSON configuration file for app IDs and tokens

## Usage
1. Clone Git repository `https://github.com/ahmadxp/dawn-validator`
2. Open folder `cd dawn-validator`
3. Install requirements `pip install -r requirements.txt`
4. Setting `config.json`:
if you're want to using proxy set to `true`, `false` if not using proxy
```json
[
  {
    "appid": "your_appid1",
    "token": "your_bearer_token1",
    "proxy": false
  },
  {
    "appid": "your_appid2",
    "token": "your_bearer_token2",
    "proxy": true
  }
]
```
5. Set Proxy (Optional)
>make sure set config to `true` if you want to using proxy!
```json
[
  "http://user:pass@ip:port"
  "http://ip:port"
]
```

## Response
Known about response this bot
- Keepalive success
```
[user@email.com] KEEPALIVE: Keep alive recorded !!
[user@email.com] Total Points: XXXXX.X
```
- **Keepalive error / no response**. Ignore it, no problem
```
[user@email.com] Something wrong! Error: 502 Bad Gateway
```
- **Error Fetch initial data**. Relax, just error when trying to fetch initial data (get first response). But this error can be showing when appid/token is failed.
```
[ERROR] Failed to fetch initial data (appid: xxxxxxx), retrying in 15 seconds...
```
- **Proxy failed.** Same error fetch initial data, because the proxy is failed / invalid proxy auth / problem on proxy.
```
[ERROR] Failed to fetch initial data (appid: xxxxxxx), retrying in 15 seconds...
```
- Another error
```
[user@email.com] Failed to retrieve point data
```
## DYOR
This bot is designed solely for educational and automation purposes. Use it at your own risk. Author is not responsible for any account bans or restrictions caused by the use of this script.

---

## Keep it active
Support me if you like this script😊
- SOL `BPJSqxyf52FtdoVt163vZFDWYheJEryee4CdWWsrnJMv`
