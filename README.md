# Server Monitor Program Based on Lark Robot

## Introduction
Original intention: Due to multiple remote servers being unsupervised and far apart, it may not be possible to detect server problems in a timely manner. To solve this problem, we have developed this monitoring program to monitor the server status in real-time. Thanks to the openness of Lark (called Feishu in Chinese Mainland) platform of ByteDance Group, the program can be seamlessly integrated with Lark to ensure that problems can be found and responded in a timely manner.

![Python](https://github.com/jonacruz89/SAWARATSUKI.ServiceLogos/blob/main/Python/Python.png?raw=true)

> [What is Lark?](https://www.larksuite.com/hc/en-US/articles/792106773934-new-to-lark-start-here)

## Download Lark App

- **For global users**: 
  - [Download Lark ](https://www.larksuite.com/en_us/download)
- 如果你身处中国大陆请使用飞书:
  - [Download Feishu](https://www.feishu.cn/download)

### Configure robots
Subsequently, the markdown instructions will be clearly stated.....

## Function

### Query Request Class
- Check the fan speed
- View server status
- View export IP (applicable to home users)

### Monitoring category 🕒
- Monitoring service fan speed (minute level), speed exceeding threshold, push alarm
- Server alarm status (minute level) Speed exceeding threshold push alarm

## Quick Use

### Prerequisites
	OS: Linux is recommended (specifically for Debian and Ubuntu). 
    Windows is temporarily unsupported. ❌

**Steps**

1. Clone the Repository
    ```
    git clone https://github.com/hz157/Server_Watch_Base_LarkBot.git
    ```
2. Install ipmitool
    ```
    sudo apt-get update
    sudo apt-get install ipmitool
    ```
3. Set Up Virtual Environment

    It is recommended to set up a standalone Python environment:
    ```
    python -m venv venv
    source ./venv/bin/activate
    ```
4. Install Dependencies

    Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```
    如果在中国大陆网络环境建议使用清华大学镜像源
    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```