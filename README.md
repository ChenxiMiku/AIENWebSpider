# 异步爬虫

## 简介

此项目是一个简单的爬虫，用于抓取上海海洋大学爱恩学院的新闻动态，包括该网站的新闻内容和相关图片。该爬虫使用了 aiohttp 网络请求库，结合异步请求和多线程技术，以提高数据抓取的效率。经过初步测试，相较于使用 requests 请求库单线程实现，该爬虫的速度快了约 8 倍；而与使用 requests 请求库多线程（max_workers=32）相比，其速度快了约 3 倍。本项目还提供了该爬虫的requests多线程实现。

## 使用说明

1. **安装依赖**：
   - `aiohttp`
   - `beautifulsoup4`
   
   您可以使用以下命令安装依赖：
   ```bash
   pip install aiohttp beautifulsoup4 
2. **运行主程序**
   ```bash
   python asyncspider.py
## 合规性和法律要求

### 遵守网站 `robots.txt`

在使用爬虫前，请务必检查目标网站的 `robots.txt` 文件，确保您的爬取行为是允许的。该文件通常位于网站根目录下，例如 [https://example.com/robots.txt](https://example.com/robots.txt)。遵循 `robots.txt` 中的规则是尊重网站所有者的一种方式。

### 尊重版权

抓取的数据可能受到版权保护。请确保在使用抓取的数据时，遵循相关的版权法律法规，避免未经授权的使用。

### 数据安全和法律法规

在数据抓取和使用过程中，请遵循以下法律法规：

- **《数据安全法》**：确保您对数据的处理、存储和使用是合法合规的，保护用户隐私。
- **《个人信息保护法》**：在抓取涉及个人信息的数据时，请确保遵循相关法律，避免侵害个人隐私。

### 遵守 GPL-3.0 开源协议

本项目遵循 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) 开源协议。您可以自由使用、修改和分发本项目的代码，但请确保遵循 GPL-3.0 协议的条款。

## 注意事项

- 请勿进行恶意爬取或数据滥用。
- 控制请求频率，以避免对目标网站造成负担。
- 对抓取的数据进行合理使用，确保数据的安全性和合法性。

## 贡献

- 欢迎对本项目提出建议或贡献代码。如有任何问题，请联系维护者。