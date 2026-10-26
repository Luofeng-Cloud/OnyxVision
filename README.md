<div align="center">

# 🔮 OnyxVision · 曜石视界

### The Obsidian-Deep Private Streaming Hub & 4K HDR Player
### 极夜曜石 · 极简私有云影音流媒体中枢与 4K HDR 播放器

[![Latest Release](https://img.shields.io/github/v/release/Luofeng-Cloud/OnyxVision?style=flat-square&color=blue&logo=github)](https://github.com/Luofeng-Cloud/OnyxVision/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg?style=flat-square)](LICENSE)
[![iOS Support](https://img.shields.io/badge/iOS-14.0%2B-black.svg?style=flat-square&logo=apple)](https://developer.apple.com/ios/)
[![Capacitor](https://img.shields.io/badge/Capacitor-8.5-119EFF.svg?style=flat-square&logo=capacitor)](https://capacitorjs.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.4%2B-4FC08D.svg?style=flat-square&logo=vue.js)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Platform](https://img.shields.io/badge/Platform-iOS%20%7C%20Windows%20%7C%20Web-orange.svg?style=flat-square)](https://github.com/Luofeng-Cloud/OnyxVision)

<p align="center">
  <b>沉浸式 Apple HIG 磨砂毛玻璃</b> · <b>2:3 黄金比例海报墙</b> · <b>全手势触控播放内核</b> · <b>Emby / Jellyfin / WebDAV 全协议直连</b> · <b>iPhone 扫码即映 PWA 与 Capacitor 跨端原生架构</b>
</p>

[🇨🇳 简体中文](#-简体中文) | [🇺🇸 English](#-english) | [🏗️ 架构概览](#️-架构概览--architecture) | [🚀 开发者从源码运行](#-开发者快速开始-run-from-source)

</div>

---

## 📸 界面预览 / Screenshots

| 首页海报墙与 Hero Banner 轮播 | 影视详情页与动态环境光漫射 |
|:---:|:---:|
| ![Home](docs/images/onyxvision_home.png) | ![Detail](docs/images/onyxvision_detail.png) |

| 极客级音画技术参数检视器 | 全能触控手势播放器 |
|:---:|:---:|
| ![Specs](docs/images/onyxvision_specs.png) | ![Player](docs/images/onyxvision_player.png) |

| 左滑亮度调节 HUD (毛玻璃指示柱) | 长按 2.0X 极速播放 HUD |
|:---:|:---:|
| ![Brightness](docs/images/onyxvision_brightness.png) | ![FastForward](docs/images/onyxvision_fastforward.png) |

| iPhone 扫码即映 (局域网即连二维码) | Emby / Jellyfin / WebDAV 媒体源连接 |
|:---:|:---:|
| ![QRCode](docs/images/onyxvision_qrcode.png) | ![Sources](docs/images/onyxvision_sources.png) |

---

## 🇨🇳 简体中文

### 🌟 核心特性

1. **100% 苹果原生设计美学 (Apple HIG)**
   - **曜石极夜质感**：基于 `#0A0B0E` 深空底色，全局搭配 `backdrop-filter: blur(25px)` 的高保真磨砂毛玻璃。
   - **Hero Banner 动态轮播**：50% 视高大图，底部多段渐变消融，高光标题、★TMDB 评分、极客规格角标。
   - **2:3 黄金海报网格**：自适应多端流式布局（手机 2 列、iPad 4 列、桌面 6-7 列），带已播红色进度条与 Hover 1.04x 微呼吸动效。
   - **动态环境光漫射 (Dynamic Ambient Light)**：影视详情页依据海报自动提取深邃主色调，顶部投射 140px 柔和漫反射光晕。

2. **全能触控手势播放内核**
   - **左半屏上下滑**：调节屏幕亮度（带磨砂胶囊指示柱）。
   - **右半屏上下滑**：调节音量与音频软增益（100%-200%）。
   - **水平横向滑动**：毫秒级时间轴 Seeking 与时间提示。
   - **长按屏幕 (300ms)**：临时切入 **2.0x 极速快进**，顶部浮现流光提示，松手无缝切回原速。
   - **双击左/右**：快退 10 秒 / 快进 10 秒；中央双击播放/暂停。
   - **高级控制**：倍速 (0.5x - 3.0x)、画幅比例 (适应/16:9/4:3/铺满)、ASS 特效/外挂字幕切换、画中画 (PiP)。

3. **极客级音画技术参数面板 (Specs Inspector)**
   - 1:1 调出全格式技术诊断面板：4K DCI (3840x2160)、HEVC Main 10@L5.1、Dolby Vision (Profile 8.1) + HDR10、10-bit BT.2020、42.8 Mbps 超高码率、Dolby Atmos 7.1 TrueHD 母带音频。

4. **多源虚拟文件系统 (VFS) 与双向同步**
   - **Emby / Jellyfin 协议原生直连**：支持地址、端口、账号密码或 API Key 登录；构建 static=true 原画 Direct Play 直通，完全跳过服务端压制；全生命周期回传 10 秒心跳播放进度，已看/未看状态实时对齐。
   - **WebDAV / Alist 挂载**：支持挂载各类私有 NAS、阿里云盘、网盘聚合。
   - **本地影视扫库**：内置多阶段正则清洗器，剥离压制组与技术标签，对接 TMDB API v3 智能刮削。

5. **iPhone 扫码即映 (局域网即连与 PWA 极速体验)**
   - 电脑端启动服务后，终端与界面自动生成当前 Wi-Fi 局域网直连二维码。
   - 移动设备相机扫码秒级接入，支持 Safari “添加到主屏幕” 获得全屏沉浸独立应用体验。

---

## 🚀 开发者快速开始 (Run from Source)

### 1. 克隆代码仓库
```bash
git clone https://github.com/Luofeng-Cloud/OnyxVision.git
cd OnyxVision
```

### 2. 后端服务启动 (FastAPI)
```bash
# 安装 Python 核心依赖 (推荐 Python 3.10+)
pip install -r backend/requirements.txt

# 准备环境变量配置文件
cp .env.example .env

# 启动后端核心服务 (默认监听 0.0.0.0:8000)
python backend/run.py
```

### 3. 前端工程构建与调试 (Vue 3 + Vite)
```bash
cd frontend

# 安装前端依赖
npm install

# 启动本地热重载开发服务器
npm run dev

# 编译生产环境静态资源 (输出至 backend/static 目录供后端一体化托管)
npm run build
```

### 4. 移动端 Capacitor 原生同步 (可选)
```bash
# 同步构建产物至 iOS 原生工程
npx cap sync ios

# 使用 Xcode 打开 iOS 项目进行本地联调与签名构建
npx cap open ios
```

### 5. Windows 平台快速启动脚本
在工程根目录下直接执行批处理脚本：
```bat
run_onyxvision.bat
```
脚本将自动在后台挂载服务并在默认浏览器中唤起 `http://127.0.0.1:8000`。

---

## 🇺🇸 English

### 🌟 Key Features
- **Obsidian Dark & Frosted Glass**: Built with Apple Human Interface Guidelines (HIG) aesthetics, frosted glass blur (`backdrop-filter: blur(25px)`), and dynamic ambient lighting extracted from posters.
- **Full Touch Gesture Player**: Left-swipe brightness, right-swipe volume boost, horizontal seek with HUD timestamp, long-press 2.0x fast-forward, double-tap jump +/-10s, and aspect ratio controls.
- **Specs Inspector**: Detailed media diagnostic drawer (4K DCI, HEVC 10-bit, Dolby Vision Profile 8.1, Atmos 7.1, 42.8 Mbps).
- **Multi-Source VFS**: Direct Play streaming for Emby, Jellyfin, WebDAV, Alist, and local disk folders with TMDB v3 automatic metadata scraping.
- **Bi-directional Scrobbling**: Full playback progress heartbeat (Playing, Progress, Stopped) and played status sync with Emby servers.
- **Instant LAN QR Code for iPhone**: Generates dynamic QR codes for mobile devices on the same Wi-Fi. Add to home screen for a seamless PWA experience.

---

## 🏗️ 架构概览 / Architecture

```text
+-------------------------------------------------------------------------------+
|                       OnyxVision iOS App / PWA Frontend                       |
|  [Apple HIG Dark UI]  [Hero Carousel]  [2:3 Poster Grid]  [Dynamic Lighting]  |
|  [Full-Screen Gesture Player (Brightness / Volume / Seek / 2x Turbo / PiP)]   |
+-------------------------------------------------------------------------------+
                                       | (Capacitor Bridge / REST API Direct)
+-------------------------------------------------------------------------------+
|                     OnyxVision Core Backend (FastAPI)                         |
|  +------------------------+  +------------------------+  +-----------------+  |
|  | Emby / Jellyfin Engine |  | WebDAV / Local Storage |  | TMDB Scraper v3 |  |
|  +------------------------+  +------------------------+  +-----------------+  |
|  +-------------------------------------------------------------------------+  |
|  | HTTP Range 206 Partial Content Streamer & Bi-directional Scrobbler      |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
                                       |
                     [SQLite WAL Local Metadata Cache]
```

---

## 📜 开源协议 / License

本项目采用 [MIT License](LICENSE) 授权许可。
