@echo off
chcp 65001 >nul
title Pull and Run mingology tool suite

echo ==========================================
echo  1) 进入项目目录
echo ==========================================
cd /d "%~dp0"

echo.
echo ==========================================
echo  2) 查看当前分支
echo ==========================================
git branch --show-current

echo.
echo ==========================================
echo  3) 拉取 GitHub 最新代码
echo ==========================================
git pull
if errorlevel 1 (
  echo.
  echo [ERROR] git pull 失败，请先处理冲突或网络问题。
  pause
  exit /b 1
)

echo.
echo ==========================================
echo  4) 显示最新提交
echo ==========================================
git log -1 --oneline

echo.
echo ==========================================
echo  5) 启动验证入口 run_query.bat
echo ==========================================
if exist "run_query.bat" (
  call run_query.bat
) else (
  echo [ERROR] 未找到 run_query.bat，请确认文件在当前目录。
  pause
  exit /b 1
)

echo.
echo [OK] 已完成：拉取 + 启动验证。
pause