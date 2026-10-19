@echo off
cd /d "%~dp0"
echo Dang day code len GitHub...
git push -u origin main
if %ERRORLEVEL% equ 0 (
    echo.
    echo ================================================
    echo DAY LEN GITHUB THANH CONG!
    echo Link repo cua ban: https://github.com/sondthe200221/SpaceX-Falcon9-Landing-Prediction
    echo ================================================
) else (
    echo.
    echo [LOI] Khong the day len. Ban da bam 'Create repository' tren GitHub chua?
)
pause
