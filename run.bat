@echo off
cls

:: Mengecek apakah virtual environment sudah ada
if not exist "script\venv" (
    echo Virtual environment tidak ditemukan. Mengatur virtual environment...
    python -m venv script\venv
)

:: Mengaktifkan virtual environment
call script\venv\Scripts\activate.bat

:: Mengecek apakah dependencies sudah terinstall
if not exist "script\requirements.txt" (
    echo File requirements.txt tidak ditemukan.
    pause
    exit /b
)

:: Install dependencies jika pertama kali
echo Memeriksa dependencies...
pip install -r script\requirements.txt

:: Menu Pilihan
echo =========================================
echo           TikTok Bot - Zefoy Automation
echo =========================================
echo [1] Views
echo [2] Views Incognito
echo [3] Like
echo [4] Like Incognito
echo =========================================
echo Pilih opsi (1-4):
set /p option=Pilihanmu: 

:: Memberikan perintah berdasarkan pilihan
if "%option%"=="1" (
    echo Memulai Views...
    python script\view.py
)

if "%option%"=="2" (
    echo Memulai Views Incognito...
    python script\viewincognito.py
)

if "%option%"=="3" (
    echo Memulai Like...
    python script\like.py
)

if "%option%"=="4" (
    echo Memulai Like Incognito...
    python script\likeincognito.py
)

:: Copyright
echo =========================================
echo Copyright Kondang - TikTok Bot Automation
echo =========================================
pause
