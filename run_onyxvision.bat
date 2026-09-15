@echo off
chcp 65001 >nul
title OnyxVision (曜石视界) Core Engine & Web Player

echo ======================================================================
echo       ONYXVISION (曜石视界) · 私有影视与流媒体中枢
echo ======================================================================
echo.
echo [1/2] 正在启动 OnyxVision 核心引擎与 Web 播放器...
echo.

set PYTHON_EXE=C:\Users\13705\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo [错误] 未找到 Python 虚拟环境: %PYTHON_EXE%
    pause
    exit /b 1
)

:: 延迟 2 秒后自动唤起默认浏览器打开 OnyxVision Web 播放器
start /min cmd /c "timeout /t 2 >nul & start http://127.0.0.1:8000"

"%PYTHON_EXE%" "D:\Antigravity对话保存位置\OnyxVision\backend\run.py"

pause
