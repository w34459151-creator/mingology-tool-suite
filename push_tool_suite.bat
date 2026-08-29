@echo off
chcp 65001 >nul
title Push mingology-tool-suite

echo ==========================================
echo  1) 进入项目目录
echo ==========================================
cd /d "%~dp0"

echo.
echo ==========================================
echo  2) 当前分支/状态
echo ==========================================
git branch --show-current
git status

echo.
set /p MSG=请输入本次提交说明(直接回车则用默认):
if "%MSG%"=="" set MSG=chore: update mingology tool suite

echo.
echo ==========================================
echo  3) 拉取远端最新，避免冲突
echo ==========================================
git pull --rebase
if errorlevel 1 (
  echo.
  echo [ERROR] git pull --rebase 失败，请先处理冲突后重试。
  pause
  exit /b 1
)

echo.
echo ==========================================
echo  4) 提交并推送
echo ==========================================
git add .
git commit -m "%MSG%"
if errorlevel 1 (
  echo.
  echo [INFO] 没有可提交内容(可能你还没改文件)。
  git status
  pause
  exit /b 0
)

git push
if errorlevel 1 (
  echo.
  echo [ERROR] git push 失败，请检查网络/权限/分支保护。
  pause
  exit /b 1
)

echo.
echo [OK] 已成功推送到 GitHub。
git log -1 --oneline
pause