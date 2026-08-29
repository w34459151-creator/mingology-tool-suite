@echo off
setlocal
cd /d "%~dp0"
if exist "C:\Users\wanglinew\AppData\Local\Programs\Python\Python311\python.exe" (
  "C:\Users\wanglinew\AppData\Local\Programs\Python\Python311\python.exe" update_address_library.py
) else if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" update_address_library.py
) else (
  py -3 update_address_library.py
)
if errorlevel 1 exit /b 1
