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
  <b>沉浸式 Apple HIG 磨砂毛玻璃</b> · <b>2:3 黄金比例海报墙</b> · <b>全手势触控播放内核</b> · <b>Emby / Jellyfin / WebDAV 全协议直连</b> · <b>iPhone 扫码即映 PWA 与原生 .ipa</b>
</p>

[📥 获取 iOS 安装包 (.ipa)](#-ios-安装包获取) | [📱 iOS 侧载安装指南](#-ios-侧载安装指南-sideloading) | [🇨🇳 简体中文](#-简体中文) | [🇺🇸 English](#-english)

</div>

---

## 📥 iOS 安装包获取

> [!TIP]
> OnyxVision 已全线打通 GitHub Actions 工业级云端打包流，每一版 Release 均由官方 macOS 运行器直接生成免签标准 `.ipa` 安装包。

- 🚀 **最新版本下载**：前往 [GitHub Releases 页面](https://github.com/Luofeng-Cloud/OnyxVision/releases) 直接获取最新 `OnyxVision.ipa`。
- 📦 **免签包直链**：[下载最新发布版 OnyxVision.ipa](https://github.com/Luofeng-Cloud/OnyxVision/releases/latest/download/OnyxVision.ipa)

---

## 📱 iOS 侧载安装指南 (Sideloading)

由于本项目当前分发的是**免签标准 .ipa 安装包**，用户可通过以下主流侧载途径将应用安装至 iPhone 或 iPad：

### 方式一：TrollStore 巨魔商店（首选推荐 ⭐️⭐️⭐️⭐️⭐️）
- **适用场景**：iOS 14.0 - 16.6.1 / 17.0（符合巨魔漏洞支持的设备）。
- **优势**：**永久免重签、免越狱、安装后永不过期、无证书失效风险**。
- **操作流程**：
  1. 在 iPhone 的 Safari 浏览器中直接下载 `OnyxVision.ipa`。
  2. 下载完成后点击“共享”按钮，选择 **“在 TrollStore 中打开”**。
  3. 点击 **Install** 即可秒级完成安装并原生常驻手机。

### 方式二：AltStore / Sideloadly（电脑辅助自签 ⭐️⭐️⭐️⭐️）
- **适用场景**：所有 iOS 版本的未越狱 iPhone / iPad。
- **优势**：官方 Apple ID 个人免费开发者证书签名，安全稳定。
- **操作流程**：
  1. 在电脑端（Windows 或 macOS）安装 [Sideloadly](https://sideloadly.io/) 或 [AltStore](https://altstore.io/)。
  2. 数据线连接 iPhone 与电脑，打开 Sideloadly 并将下载好的 `OnyxVision.ipa` 拖拽进窗口。
  3. 输入自己的 Apple ID 账号密码（建议使用备用小号或专用密码）。
  4. 点击 **Start** 自动完成证书签名并推送到 iPhone。
  5. 手机端首次打开前，进入 **设置 -> 通用 -> VPN与设备管理**，信任对应的开发者证书即可启动。
  *（注：个人免费证书有效期为 7 天，连接同一局域网可自动无缝续签）*

### 方式三：牛蛙助手 / 全能签 / 个人证书移动端直签 ⭐️⭐️⭐️⭐️
- **适用场景**：持有个人开发者证书、企业证书或配备牛蛙助手移动端的用户。
- **操作流程**：
  1. 将 `OnyxVision.ipa` 导入到移动端签名应用（如牛蛙助手、全能签、Scarlet、ESign）。
  2. 绑定自有证书后点击“立即签名”，安装生成的已签名版本即可。

### 方式四：iPhone 扫码即映 (PWA 极速模式 ⭐️⭐️⭐️⭐️)
- **适用场景**：无需任何证书、不借助任何侧载工具。
- **操作流程**：
  1. 电脑端启动 OnyxVision 后，终端或前端界面会显示局域网直连二维码。
  2. iPhone 打开自带相机扫码进入。
  3. 点击 Safari 底部 **“分享” -> “添加到主屏幕”**。
  4. 回到桌面启动，即刻享有独立全屏、无 Safari 顶底栏遮挡的媲美原生 App 体验！

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

---

### 🚀 快速启动

#### 方式一：Windows 一键启动 (推荐)
直接双击运行工程根目录下的：
```bat
run_onyxvision.bat
```
系统将自动启动后端服务，并在 2 秒后自动在默认浏览器中打开 OnyxVision 首页：`http://127.0.0.1:8000`。

#### 方式二：命令行手动启动
```bash
# 安装依赖
pip install -r backend/requirements.txt

# 启动服务
python backend/run.py
```

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