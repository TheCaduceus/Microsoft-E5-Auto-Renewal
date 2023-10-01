<div align="center"><h1>Microsoft E5 Auto Renewal</h1>
<b>An open-source Python program made using <a href="https://github.com/pallets/flask">Flask framework</a> for automatic renewal of Microsoft's Developer E5 subscription.</b></div><br>

## **📑 INDEX**

* [**⚙️ Installation**](#installation)
  * [Python & Git](#i-1)
  * [Download](#i-2)
  * [Requirements](#i-3)
* [**📝 Variables**](#variables)
* [**🕹 Deployment**](#deployment)
  * [Locally](#d-1)
  * [Replit](#d-2)
* [**🌐 Routes**](#routes)
* [**⏰ Cron-Job**](#cron-job)
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

<a name="variables"></a>

## 📝 Variables
**The variables provided below should either be completed within the config.py file or configured as environment variables.**
* `CLIENT_ID`|`E5_CLIENT_ID`: ID of your Azure Active Directory app. `str`
  * Create an app in [Azure Active Directory](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps).
  * Set application permission: `files.read.all`, `files.readwrite.all`, `sites.read.all`, `sites.readwrite.all`, `user.read.all`, `user.readwrite.all`, `directory.read.all`, `directory.readwrite.all`, `mail.read`, `mail.readwrite`, `mailboxsetting.read`, and `mailboxsetting.readwrite`.
  * Choose application type as 'Web' & set Redirect URL to `http://localhost:53682/`.
  * Copy the Application (client) ID.
* `CLIENT_SECRET`|`E5_CLIENT_SECRET`: Secret of your Azure Active Directory app. `str`
  * In your  Azure Active Directory app overview, navigate to Client credentials and create secret.
* `REFRESH_TOKEN`|`E5_REFRESH_TOKEN`: Refresh token for your admin account. `str`
  * Install [rclone](https://rclone.org).
  * In CLI, run:

    ```
    rclone authorize "onedrive" "ClientID" "ClientSecret"
    ```
  * From output, copy the value of `refresh_token` key.
* `WEB_APP_PASSWORD`|`E5_WEB_APP_PASSWORD`: Strong password to protect critical routes of your web server. `str`
  * Keep it strong and don't share it.
* `WEB_APP_HOST`|`E5_WEB_APP_HOST`: Bind address of web server. `str`
  * By default `0.0.0.0` to run on all possible addresses.
* `WEB_APP_PORT`|`E5_WEB_APP_PORT`: Port for web server to listen to. `int`
  * By default `8080`.
* `TIME_DELAY`|`E5_TIME_DELAY`: Time (in seconds) to wait before calling another endpoint. `int`
  * By default 3 seconds.

<a name="deployment"></a>

## 🕹 Deployment

<a name="d-1"></a>

**1.Running locally:**
```
python main.py
```

<a name="d-2"></a>

**2.Running on Replit:** *(Recommended)*
* Fork [Microsoft-E5-Auto-Renewal](https://replit.com/@TheCaduceus/Microsoft-E5-Auto-Renewal) repl.
* Fill `config.py` or set given environment variables. ***Be aware! directly filling `config.py` can leak your tokens.***
* Run your repl and copy the generated endpoint.

<a name="routes"></a>

## 🌐 Routes

* **`/`**

  Retrieve server statistics in JSON format, including the server version, total received requests, total successful requests, and the total number of errors encountered thus far.

  * **Request Methods:**
    * `GET` - Get server statistics as JSON.
    * `HEAD` - Ping the server.
  * **Headers:**
    * None.
  * **URL Parameters:**
    * None.
  * **Example:**
      ```shell
      curl http://127.0.0.1:8080/
      ```

* **`/call`**

  Command server to call Microsoft APIs on behalf of a user account.

  * **Request Methods:**
    * `POST` - Create a new activity thread that sends a ping to all Microsoft APIs once.
  * **Headers:**
    ```json
    {"Content-Type":"application/json"}
    ```
  * **Request Body: (as JSON)**
    * `password` (*required*) - The web app password.
    * `refresh_token` (*optional*) - The refresh token of user account to act behalf of. By default provided refresh token in *config.py*.
  * **Example:**
      ```shell
      curl -X POST -H "Content-Type: application/json" -d '{"password":"RequiredPassword", "refresh_token": "OptionalRefreshToken"}' "http://127.0.0.1:8080/call"
      ```

* **`/getLog`**

    Generate download request for current log file.

  * **Request Methods:**
    * `GET` - Get server's log file.
  * **Headers:**
    * None.
  * **URL Parameters:**
    * `password` (*required*) - The web app password.
  * **Example**
      ```shell
      curl -o "event-log.txt" "http://127.0.0.1:8080/getLog?password=1234"
      ```

<a name="cron-job"></a>

## ⏰ Cron-Job
**The Cron-Job will instruct our web server to invoke Microsoft APIs at regular intervals. To ensure proper functionality, the configuration of the cron-job must align with the following settings:**

* **URL**: Your server address, can be an FQDN or an IP address followed by `/call`.
  * In case of local deployment (private IP), you must setup cron-job on the same local network or reverse DNS.

    ```
    https://example.com/call
    http://127.0.0.1:8080/call
    ```

* **Interval**: 15 minutes - 8 hours.
  * A too-small interval can lead to API flooding issues.
* **Header**:

    ```json
    {"Content-Type":"application/json"}
    ```

* **Request Method**: `POST`
* **Request Body: (as Json)**
  * `password` (*required*) - Your `WEB_APP_PASSWORD` to ensure that this request originates from a trusted source.
  * `refresh_token` (*optional*) - The refresh token of the user account to act behalf of. By default, the refresh token provided in config.py.

    ```json
    {
      "password": "RequiredPassword",
      "refresh_token": "OptionalRefreshToken"
    }
    ```

<a name="help"></a>

## ⛑️ Need help!
- Ask questions or doubts [here](https://t.me/DrDiscussion).

<a name="credits"></a>

## ❤️ Credits & Thanks

[**Dr.Caduceus**](https://github.com/TheCaduceus): Owner & developer of Microsoft E5 Auto Renewal Tool.<br>
