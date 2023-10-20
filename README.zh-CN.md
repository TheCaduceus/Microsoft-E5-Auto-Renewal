<div align="center"><h1>Microsoft E5 Auto Renewal</h1>
<b><a href="README.md">English</a> | <a>中文</a></b><br>
<b>使用 <a href="https://github.com/pallets/quart">Quart</a> & <a href="https://github.com/encode/uvicorn">Uvicorn</a> 制作的开源 Python 程序，用于自动续订微软开发者 E5 订阅。</b>
</div><br>

## **📑 目录**

* [**❓ 如何使用？**](#how-to-use)
* [**⚙️ 安装**](#installation)
  * [Python & Git](#i-1)
  * [下载](#i-2)
  * [安装环境](#i-3)
* [**📝 变量**](#variables)
* [**🕹 部署**](#deployment)
  * [本地](#d-1)
  * [Docker](#d-2)
* [**🌐 Routes**](#routes)
* [**⏰ Cron-Job**](#cron-job)
* [**⛑️ 使用帮助!**](#help)
* [**❤️ 致谢**](#credits)

<a name="how-to-use"></a>

## ❓ 如何使用？
**通过以下步骤，您可以使用公共实例，而无需部署自己的服务器或进行任何设置。**

* 打开下面的 [URL](https://e5.thecaduceus.eu.org/auth) 并获取refresh token。

  * 为了增加订阅续订的机会，请先为订阅的管理员账户配置工具，然后再为非管理员账户配置。
  <br><br>
  ```
  https://e5.thecaduceus.eu.org/auth
  ```
  > [!提示]
  > 服务器发布的所有refresh token的有效期为自发布之日起90天。因此，在它们到期之前续订是很重要的。您可以通过使用相同的URL登录来获取新的refresh token。
* 现在，使用以下配置在[此处](https://cron-job.org)创建一个cron作业：
  * **URL:**

    ```
    https://e5.thecaduceus.eu.org/call
    ```
  * **时间间隔**: 3 - 8 小时.
    > [!提示]
    > 过小的间隔可能会导致Microsoft API溢出问题。
  * **Headers:**

    ```json
    {"Content-Type":"application/json"}
    ```
  * **Request Method:** POST
  * **Request Body:**

    ```json
    {"refresh_token": "YourRefreshTokenHere"}
    ```
* 搞定！🎉

<a name="installation"></a>

## ⚙️ 安装

<a name="i-1"></a>

**1.安装 Python 和 Git:**

Windows 用户:
```
winget install Python.Python.3.12
winget install Git.Git
```
Linux 用户:
```
sudo apt-get update && sudo apt-get install -y python3.12 git pip
```
macOS 用户:
```
brew install python@3.12 git
```
Termux 用户:
```
pkg install python -y
pkg install git -y
```

<a name="i-2"></a>

**2.下载仓库:**
```
git clone https://github.com/TheCaduceus/Microsoft-E5-Auto-Renewal.git
```

**3.进入工作目录:**

```
cd Microsoft-E5-Auto-Renewal
```

<a name="i-3"></a>

**4.安装环境:**

```
pip install -r requirements.txt
```

<a name="variables"></a>

## 📝 变量
**下面提供的变量应该在config.py文件中完成，或者配置为环境变量。**
* `CLIENT_ID`|`E5_CLIENT_ID`: Azure Active Directory应用程序的ID。 `str`
  * 在 [Azure Active Directory](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) 中创建应用程序。
  * 选择应用程序类型为“Web”并将重定向URL设置为 `http://localhost:53682/`.
  * 复制应用程序（客户端）ID 或 Application (client) ID.
* `CLIENT_SECRET`|`E5_CLIENT_SECRET`: Azure Active Directory应用程序的密钥。 `str`
  * 在Azure Active Directory应用程序概述中，导航到客户端凭据并创建密钥。
* `REFRESH_TOKEN`|`E5_REFRESH_TOKEN`: 刷新管理员帐户的令牌（token）。 `str`
> [!提示]
> 授权客户端发布的所有刷新令牌的有效期为自发布之日起90天。因此，在它们到期之前续订是很重要的。
  * 在CLI中，运行：

    ```
    python auth.py YourClientID YourClientSecret
    ```
  * 按照屏幕上的说明操作。
  * 从输出中，复制`refresh_token`键的值。
* `WEB_APP_PASSWORD`|`E5_WEB_APP_PASSWORD`: 强大的密码保护您的网络服务器的关键路由。 `str`
  * 密码设置复杂点，并且注意不要分享给其他人。
* `WEB_APP_HOST`|`E5_WEB_APP_HOST`: web服务器的绑定地址。 `str`
  * 默认情况下，`0.0.0.0`在所有可能的地址上运行。
* `WEB_APP_PORT`|`PORT`: 要侦听的web服务器的端口。`int`
  * 默认端口 `8080`.
* `TIME_DELAY`|`E5_TIME_DELAY`: 调用另一个终结点之前等待的时间（以秒为单位）。 `int`
  * 默认情况下为3秒。

<a name="deployment"></a>

## 🕹 部署

<a name="d-1"></a>

**1.在本地运行:** *(最适合测试)*
```
python main.py
```

<a name="d-2"></a>

**2.使用Docker:** *(推荐)*
* 构建自己的Docker镜像：
```
docker build -t msft-e5-renewal .
```
* 运行Docker容器：
```
docker run -p 8080:8080 msft-e5-renewal
```

<a name="routes"></a>

## 🌐 Routes

* **/** - GET

  以JSON格式检索服务器统计信息，包括服务器版本、收到的请求总数、成功的请求总数以及迄今为止遇到的错误总数。

  * **Headers:**
    * None.
  * **参数：**
    * None.
  * **例如:**

    ```shell
    curl http://127.0.0.1:8080/
    ```

* **/call** - POST

  命令服务器代表用户帐户调用Microsoft API。

  * **Headers:**

    ```json
    {"Content-Type":"application/json"}
    ```
  * **参数：（作为JSON）**
    * `password` (*必需*) - web应用程序密码。
    * `client_id` (*可选*) - Azure Active Directory应用程序的ID。默认情况下，在*config.py*中提供客户端ID。
    * `client_secret` (*可选*) - Azure Active Directory应用程序的secret。默认情况下，在*config.py*中提供客户端secret。
    * `refresh_token` (*可选*) - 要代理的用户帐户的刷新令牌。默认情况下，在*config.py*中提供刷新令牌。
  * **例如:**

    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"password":"RequiredPassword", "refresh_token": "OptionalRefreshToken"}' "http://127.0.0.1:8080/call"
    ```

* **/logs** - GET

    生成当前日志文件的下载请求。

  * **Headers:**
    * None.
  * **参数：（在URL中）**
    * `password` (*必须*) - web应用程序密码。
    * `as_file` (*可选*) - 默认情况下，此参数设置为False，允许您选择是将日志作为文件发送，选项为True还是False。
  * **例如:**

    ```shell
    curl -o "event-log.txt" "http://127.0.0.1:8080/logs?password=1234&as_file=True"
    ```

<a name="cron-job"></a>

## ⏰ Cron-Job
**Cron作业将指示我们的web服务器定期调用Microsoft API。为了确保正确的功能，cron作业的配置必须与以下设置保持一致：**

* **URL**: 服务器地址，可以是FQDN或IP + `/call`。
  * 如果是本地部署（专用IP），则必须在同一本地网络或反向DNS上设置cron作业。

    ```
    https://example.com/call
    http://127.0.0.1:8080/call
    ```

* **间隔**: 3 - 8 小时.
    > [!提示]
    > 过小的间隔可能会导致Microsoft API溢出问题。
* **Header**:

    ```json
    {"Content-Type":"application/json"}
    ```
* **请求方法**: `POST`
* **参数：（作为JSON）**
  * `password` (*必须*) - web应用程序密码。
  
  有关所有其他可选参数，请参阅 [这里](#routes).

    ```json
    {
      "password": "RequiredPassword",
      "refresh_token": "OptionalRefreshToken"
    }
    ```

<a name="help"></a>

## ⛑️ 使用帮助！
- 在[这里](https://t.me/DrDiscussion)提出问题或疑虑。

<a name="credits"></a>

## ❤️ 致谢

[**Dr.Caduceus**](https://github.com/TheCaduceus): Microsoft E5自动更新工具的所有者和开发人员。<br>
