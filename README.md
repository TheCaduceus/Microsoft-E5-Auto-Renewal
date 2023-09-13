<div align="center"><h1>Microsoft E5 Auto Renewal</h1>
<b>An open-source Python program made using <a href="https://github.com/pallets/flask">Flask framework</a> for automatic renewal of Microsoft's Developer E5 subscription.</b></div><br>

## **📑 INDEX**

* [**⚙️ Installation**](#installation)
  * [Python & Git](#i-1)
  * [Download](#i-2)
  * [Requirements](#i-3)
* [**✏ Variables**](#installation)
* [**🕹 Deployment**](#deployment)
  * [Locally](#d-1)
  * [Replit](#d-2)
* [**⛑️ Need help!**](#help)
* [**❤️ Credits & Thanks**](#credits)

<a name="installation"></a>

## ⚙️ Installation

<a name="i-1"></a>

**1.Install Python & Git:**

For Windows:
```
winget install Python.Python.3.11
winget install Git.Git
```
For Linux:
```
sudo apt-get update && sudo apt-get install -y python3.11 git pip
```
For macOS:
```
brew install python@3.11 git
```
For Termux:
```
pkg install python -y
pkg install git -y
```

<a name="i-2"></a>

**2.Download repository:**
```
git clone https://github.com/TheCaduceus/Microsoft-E5-Auto-Renewal.git
```

**3.Change Directory:**

```
cd Microsoft-E5-Auto-Renewal
```

<a name="i-3"></a>

**4.Install requirements:**

```
pip install -r requirements.txt
```

## ✏ Variables
**Below given variables should be filled in `config.py` file or can be configured as environment variables.**
- `REFRESH_TOKEN`|`E5_REFRESH_TOKEN`: Refresh token for your admin account. `str`
- `CLIENT_ID`|`E5_CLIENT_ID`: ID of your Azure Active Directory app. `str`
- `CLIENT_SECRET`|`E5_CLIENT_SECRET`: Secret of your Azure Active Directory app. `str`
- `WEB_APP_PASSWORD`|`E5_WEB_APP_PASSWORD`: Strong password to protect critical routes of your web server. `str`
- `WEB_APP_HOST`|`E5_WEB_APP_HOST`: Bind address of web server. `str`
- `WEB_APP_PORT`|`E5_WEB_APP_PORT`: Port for web server to listen to. `int`
- `TIME_DELAY`|`E5_TIME_DELAY`: Time to wait before calling another endpoint. `int`

## 🕹 Deployment

<a name="d-1"></a>

**1.Running locally:** *(Not ideal for production)*
```
python main.py
```

<a name="d-2"></a>

**2.Running on Replit:** *(Recommended)*
* Fork [Microsoft-E5-Auto-Renewal](https://replit.com/@TheCaduceus/Microsoft-E5-Auto-Renewal) repl.
* Fill `config.py` or set given environment variables. ***Be aware! directly filling `config.py` can leak your tokens.***
* Run your repl and copy the generated endpoint.
* Setup a cron-job using [cron-job.org](https://cron-job.org) for every 15 minutes with below configuration.
  * **URL:** `https://YourReplURL.co/call`
  * **Interval:** 15 Minutes
  * **Header:** `Content-Type` as key & `application/json` as value.
  * **Request Method:** `POST`
  * **Request Body:** `{"password":"YourPasswordHere"}`

<a name="help"></a>

## ⛑️ Need help!

- Create an [issue](https://github.com/TheCaduceus/Microsoft-E5-Auto-Renewal/issues) on GitHub.
- [Subscribe](https://t.me/TheCaduceusOfficial) Telegram channel.
- Ask questions or doubts [here](https://t.me/DrDiscussion).
- Send a [personal message](https://t.me/TheCaduceusHere) to developer on Telegram.
- Tag on [Twitter](https://twitter.com/BeingDrCaduceus).

<a name="credits"></a>

## ❤️ Credits & Thanks

[**Dr.Caduceus**](https://github.com/TheCaduceus): Owner & developer of Microsoft E5 Auto Renewal Tool.<br>
