# 异步爬虫

## 简介

此项目是一个简单的爬虫，用于抓取上海海洋大学爱恩学院的新闻动态，包括该网站的新闻内容和相关图片。该爬虫使用了 aiohttp 网络请求库，结合异步请求和多线程技术，以提高数据抓取的效率。经过初步测试，相较于使用 requests 请求库单线程实现，该爬虫的速度快了约 8 倍；而与使用 requests 请求库多线程（max_workers=32）相比，其速度快了约 3 倍。本项目还提供了该爬虫的requests多线程实现。

使用tqdm库实现进度条。

## 使用说明
请按照以下步骤配置和运行该程序：

1. 克隆项目到本地：
    ```bash
    git clone https://github.com/ChenxiMiku/AIENWebSpider
    cd AIENWebSpider
    ```

2. **安装依赖**：
   - `aiohttp`
   - `beautifulsoup4`
   - `tqdm`
   
   您可以用以下命令安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

   或手动安装这些依赖：
   ```bash
   pip install aiohttp beautifulsoup4 tqdm
   ```

3. **运行主程序**
   ```bash
   python asyncspider.py
   ```

## 常见问题

### Error downloading https://wzgl.shou.edu.cn/_upload/article/images/xx/xx/xxxxxxxxxxxxxxxxxxxxxxxxxx/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx.png: Cannot connect to host wzgl.shou.edu.cn:443 ssl:default [信号灯超时时间已到]
**问题描述**  
此错误表明程序无法连接到 `wzgl.shou.edu.cn`，原因是该网站需要通过上海海洋大学的校园网或 VPN 才能访问。

**解决方法**  
请确保在以下环境下使用本程序：
1. 在上海海洋大学校园网内使用本程序。
2. 或通过 VPN 连接至上海海洋大学内网后使用本程序。

在此环境下重新运行程序即可正常访问该网址。

### 其他常见问题
如果遇到其他错误或问题，请提交 issue 或联系开发者。

## 合规性和法律要求

### 遵守网站 `robots.txt`

在使用爬虫前，请务必检查目标网站的 `robots.txt` 文件，确保您的爬取行为是允许的。该文件通常位于网站根目录下，例如 [https://example.com/robots.txt](https://example.com/robots.txt)。遵循 `robots.txt` 中的规则是尊重网站所有者的一种方式。

### 尊重版权

抓取的数据可能受到版权保护。请确保在使用抓取的数据时，遵循相关的版权法律法规，避免未经授权的使用。

### 数据安全和法律法规

在数据抓取和使用过程中，请遵循以下法律法规：

- **《中华人民共和国数据安全法》**：确保您对数据的处理、存储和使用是合法合规的，保护用户隐私。
- **《中华人民共和国个人信息保护法》**：在抓取涉及个人信息的数据时，请确保遵循相关法律，避免侵害个人隐私。

### 遵守 GPL-3.0 开源协议

本项目遵循 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 开源协议。您可以自由使用、修改和分发本项目的代码，但请确保遵循 GPL-3.0 协议的条款。

## 注意事项

- 请勿进行恶意爬取或数据滥用。
- 控制请求频率，以避免对目标网站造成负担。
- 对抓取的数据进行合理使用，确保数据的安全性和合法性。

## 贡献

- 欢迎对本项目提出建议或贡献代码。如有任何问题，请联系维护者。