@echo off
title OnyxVision (曜石视界) - Git Push to GitHub
cd /d D:\EmbyVision

echo ====================================================================
echo      OnyxVision (曜石视界) - Pushing code to GitHub Actions
echo      Repository: https://github.com/Luofeng-Cloud/OnyxVision.git
echo ====================================================================
echo.
echo [*] Pushing commits to GitHub...
echo.

git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo [SUCCESS] Code pushed successfully!
    echo Cloud build started on GitHub Actions.
    echo Opening browser to check build progress...
    echo ====================================================================
    start https://github.com/Luofeng-Cloud/OnyxVision/actions
) else (
    echo.
    echo ====================================================================
    echo [ERROR] Git push encountered an issue.
    echo Please make sure GitHub authorization is granted.
    echo ====================================================================
)

echo.
echo Press any key to exit this window...
pause >nul
