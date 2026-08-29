@echo off
setlocal
set "TASK_NAME=MyBookAnalysis monthly address update"
set "RUNNER=%~dp0run_monthly_address_update.bat"
schtasks /Create /TN "%TASK_NAME%" /TR "cmd.exe /c \"\"%RUNNER%\"\"" /SC MONTHLY /D 1 /ST 03:00 /F
if errorlevel 1 (
  echo Failed to create the scheduled task.
  exit /b 1
)
echo Scheduled task created: %TASK_NAME%
echo It runs on day 1 of every month at 03:00.
