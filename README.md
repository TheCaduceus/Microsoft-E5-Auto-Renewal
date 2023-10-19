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
* [**🌐 Routes**](#routes)
* [**⏰ Cron-Job**](#cron-job)
* [**⛑️ Need help!**](#help)
* [**❤️ Credits & Thanks**](#credits)

<a name="how-to-use"></a>

## ❓ How to use?
**By following the steps given below, you can use the public instance without deploying your own server or requiring any setup.**

* Open below [URL](https://e5.thecaduceus.eu.org/auth) and get your refresh token.

  * To increase the chances of getting your subscription renewed, configure the tool for your subscription’s admin accounts first, and then for non-admin accounts.
  <br><br>
  ```
  https://e5.thecaduceus.eu.org/auth
  ```
  > [!NOTE]
  > All refresh tokens issued by the server have a validity period of 90 days from the date of issue. Therefore, it is important to renew them before they expire. You can acquire a new refresh token by logging in using the same URL.
* Now create a cron-job [here](https://cron-job.org) with following configuration:
  * **URL:**

    ```
    https://e5.thecaduceus.eu.org/call
    ```
  * **Interval**: 3 - 8 hours.
    > [!NOTE]
    > A too-small interval can lead to Microsoft API flooding issues.
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
winget install Python.Python.3.12
winget install Git.Git
```
For Linux:
```
sudo apt-get update && sudo apt-get install -y python3.12 git pip
```
For macOS:
```
brew install python@3.12 git
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
  * Choose application type as 'Web' & set Redirect URL to `http://localhost:53682/`.
  * Copy the Application (client) ID.
* `CLIENT_SECRET`|`E5_CLIENT_SECRET`: Secret of your Azure Active Directory app. `str`
  * In your  Azure Active Directory app overview, navigate to Client credentials and create secret.
* `REFRESH_TOKEN`|`E5_REFRESH_TOKEN`: Refresh token for your admin account. `str`
> [!NOTE]
> All refresh tokens issued by the authorization client have a validity period of 90 days from the date of issue. Therefore, it is important to renew them before they expire.
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

* **Interval**: 3 - 8 hours.
    > [!NOTE]
    > A too-small interval can lead to Microsoft API flooding issues.
* **Header**:

    ```json
    {"Content-Type":"application/json"}
    ```
* **Request Method**: `POST`
* **Parameters: (as JSON)**
  * `password` (*required*) - The web app password.
  
  For all other optional parameters, refer to [here](#routes).

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
