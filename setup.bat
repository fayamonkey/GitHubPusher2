@echo off
echo Setting up GitHub Project Uploader...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo You can download it from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install PyQt6 PyGithub

REM Get the current directory
set "SCRIPT_DIR=%~dp0"

REM Create the shortcut
echo Creating desktop shortcut...
set "DESKTOP_PATH=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP_PATH%\GitHub Project Uploader.lnk"

REM Create a temporary VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "pythonw.exe" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Arguments = """%SCRIPT_DIR%github_uploader.py""" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "GitHub Project Uploader" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "shell32.dll,147" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Execute the VBScript and delete it
cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

echo.
echo Setup completed successfully!
echo A shortcut has been created on your desktop.
echo.
pause 