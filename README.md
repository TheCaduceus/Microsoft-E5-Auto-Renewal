<div align="center"><h1>Microsoft E5 Auto Renewal</h1>
<b>An open-source Python program made using <a href="https://github.com/pallets/quart">Quart</a> & <a href="https://github.com/encode/uvicorn">Uvicorn</a> for automatic renewal of Microsoft's Developer E5 subscription.</b></div><br>

## **📑 INDEX**

* [**❓ How to use?**](#how-to-use)
* [**⚙️ Installation**](#installation)
  * [Python & Git](#i-1)
  * [Download](#i-2)
  * [Requirements](#i-3)
* [**📝 Variables**](#variables)
* [**🕹 Deployment**](#deployment)
  * [Locally](#d-1)
  * [Docker](#d-2)
  * [Cyclic](#d-3)
* [**🌐 Routes**](#routes)
* [**⏰ Cron-Job**](#cron-job)
* [**⛑️ Need help!**](#help)
* [**❤️ Credits & Thanks**](#credits)

<a name="how-to-use"></a>

## ❓ How to use?
**If you lack the knowledge to deploy your own web server, you can use a ready-to-use public instance directly by following steps given below.**

* Open below [URL](https://e5.thecaduceus.eu.org/auth) and get your refresh token.
  ```
  https://e5.thecaduceus.eu.org/auth
  ```
* Now create a cron-job [here](https://cron-job.org) with following configuration:
  * **URL:**
    ```
    https://e5.thecaduceus.eu.org/call
    ```
  * **Headers:**
    ```json
    {"Content-Type":"application/json"}
    ```
  * **Request Method:** POST
  * **Request Body:**
    ```json
    {"refresh_token": "YourRefreshTokenHere"}
    ```
* You did it!🎉

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
  * Set application permissions:
    ```
    Directory.Read.All,
    Directory.ReadWrite.All,
    Files.Read,
    Files.Read.All,
    Files.ReadWrite,
    Files.ReadWrite.All,
    Mail.Read,
    Mail.ReadWrite,
    MailboxSettings.Read,
    MailboxSettings.ReadWrite,
    Sites.Read.All,
    Sites.ReadWrite.All,
    User.Read,
    User.Read.All,
    User.ReadWrite.All
    ```
  * Choose application type as 'Web' & set Redirect URL to `http://localhost:53682/`.
  * Copy the Application (client) ID.
* `CLIENT_SECRET`|`E5_CLIENT_SECRET`: Secret of your Azure Active Directory app. `str`
  * In your  Azure Active Directory app overview, navigate to Client credentials and create secret.
* `REFRESH_TOKEN`|`E5_REFRESH_TOKEN`: Refresh token for your admin account. `str`
  * In CLI, run:
    ```
    python auth.py YourClientID YourClientSecret
    ```
  * Follow on-screen instructions.
  * From output, copy the value of `refresh_token` key.
* `WEB_APP_PASSWORD`|`E5_WEB_APP_PASSWORD`: Strong password to protect critical routes of your web server. `str`
  * Keep it strong and don't share it.
* `WEB_APP_HOST`|`E5_WEB_APP_HOST`: Bind address of web server. `str`
  * By default `0.0.0.0` to run on all possible addresses.
* `WEB_APP_PORT`|`PORT`: Port for web server to listen to. `int`
  * By default `8080`.
* `TIME_DELAY`|`E5_TIME_DELAY`: Time (in seconds) to wait before calling another endpoint. `int`
  * By default 3 seconds.

<a name="deployment"></a>

## 🕹 Deployment

<a name="d-1"></a>

**1.Running locally:** *(Best for testing)*
```
python main.py
```

<a name="d-2"></a>

**2.Using Docker:** *(Recommended)*
* Build own Docker image:
```
docker build -t msft-e5-renewal .
```
* Run the Docker container:
```
docker run -p 8080:8080 msft-e5-renewal
```

<a name="d-3"></a>

**3.Deployment on Cyclic:** *(Easiest & Free)*
* Sign-up on Cyclic [here](https://app.cyclic.sh/#/join/TheCaduceus).
* Click deployment button given below:<br>
[![Deploy to Cyclic](https://deploy.cyclic.sh/button.svg)](https://deploy.cyclic.sh/TheCaduceus/Microsoft-E5-Auto-Renewal)
* Select `main.py` as main file and `cyclic` as branch.
* Switch to 'Variables' tab and set all environment variables (starting with `E5_`) except `PORT` given above.
* Click "Connect Cyclic" and it will be deployed automatically.
* Finally, you can create cron-job using your Cyclic app endpoint as mentioned [here](#cron-job).

> [!NOTE]
> Due to the read-only file system provided by Cyclic, the /logs route is disabled.

<a name="routes"></a>

## 🌐 Routes

* **/** - GET

  Retrieve server statistics in JSON format, including the server version, total received requests, total successful requests, and the total number of errors encountered thus far.

  * **Headers:**
    * None.
  * **Parameters:**
    * None.
  * **Example:**
      ```shell
      curl http://127.0.0.1:8080/
      ```

* **/call** - POST

  Command server to call Microsoft APIs on behalf of a user account.

  * **Headers:**
    ```json
    {"Content-Type":"application/json"}
    ```
  * **Parameters: (as JSON)**
    * `password` (*required*) - The web app password.
    * `client_id` (*optional*) - ID of your Azure Active Directory app. By default provided client ID in *config.py*.
    * `client_secret` (*optional*) - Secret of your Azure Active Directory app. By default provided client secret in *config.py*.
    * `refresh_token` (*optional*) - The refresh token of user account to act behalf of. By default provided refresh token in *config.py*.
  * **Example:**
      ```shell
      curl -X POST -H "Content-Type: application/json" -d '{"password":"RequiredPassword", "refresh_token": "OptionalRefreshToken"}' "http://127.0.0.1:8080/call"
      ```

* **/logs** - GET

    Generate download request for current log file.

  * **Headers:**
    * None.
  * **Parameters: (in URL)**
    * `password` (*required*) - The web app password.
    * `as_file` (*optional*) - By default, this parameter is set to False, allowing you to choose whether to send logs as a file with options True or False.
  * **Example**
      ```shell
      curl -o "event-log.txt" "http://127.0.0.1:8080/logs?password=1234&as_file=True"
      ```

<a name="cron-job"></a>

## ⏰ Cron-Job
**The Cron-Job will instruct our web server to invoke Microsoft APIs at regular intervals. To ensure proper functionality, the configuration of the cron-job must align with the following settings:**

* **URL**: Server address, can be an FQDN or an IP address followed by `/call`.
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
* **Parameters: (as Json)**
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
