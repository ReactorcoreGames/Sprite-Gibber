@echo off
setlocal
cd /d "%~dp0"
echo === Sprite Gibber Release Build ===
echo.

set "APP=SpriteGibber"
set "REL=dist\%APP%"
set "ZIP=dist\%APP%.zip"
set "PAUSE=pause"
if /i "%~1"=="nopause" set "PAUSE=rem"

if not exist "assets\icon.ico" (
    echo ERROR: assets\icon.ico not found. Cannot build.
    %PAUSE%
    exit /b 1
)

REM Clean previous output (PyInstaller works inside build\ so dist\ only ever holds the release)
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

REM Compile the exe. The hidden tabs are imported by name (gui\app.py _ensure_tab), so
REM PyInstaller can't see them: collect all of gui\ explicitly. The collector runs in a
REM separate Python process, which only finds the project's packages via PYTHONPATH
set "PYTHONPATH=%CD%"
pyinstaller --noconfirm --onedir --windowed ^
  --icon "%CD%\assets\icon.ico" ^
  --add-data "%CD%\assets\icon.ico;." ^
  --hidden-import PIL._tkinter_finder ^
  --collect-submodules gui ^
  --distpath "build\pyi_dist" --workpath "build\pyi_work" --specpath "build" ^
  --name "%APP%" ^
  main.py

if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller failed. See output above.
    %PAUSE%
    exit /b 1
)

REM Assemble the release folder
mkdir "%REL%"
xcopy /E /I /Y /Q "build\pyi_dist\%APP%" "%REL%" >nul

REM Frame masks and the icon are looked up next to the exe (assets\), not inside _internal
xcopy /E /I /Y /Q "assets\masks" "%REL%\assets\masks" >nul
copy /Y "assets\icon.ico" "%REL%\assets\" >nul

REM Example sprites to try presets on (free, no attribution needed)
xcopy /I /Y /Q "input\*.png" "%REL%\example_sprites" >nul

REM Release documents (promo.md is an internal marketing doc - never shipped)
copy /Y "README.md" "%REL%\" >nul
copy /Y "LICENSE"   "%REL%\" >nul
copy /Y "guide.md"  "%REL%\" >nul

REM Promo images (minus the cover's source art)
xcopy /E /I /Y /Q "promo" "%REL%\promo" >nul
if exist "%REL%\promo\sprite gibber og_img.jpg" del "%REL%\promo\sprite gibber og_img.jpg"

REM Zip it, with SpriteGibber\ as the zip's root folder. Windows' own tar (not Git's) writes zips;
REM retried because antivirus can briefly lock the freshly built exe
set "TRIES=0"
:zip
"%SystemRoot%\System32\tar.exe" -a -c -f "%ZIP%" -C dist "%APP%"
if not errorlevel 1 goto zipped
set /a TRIES+=1
if %TRIES% geq 5 (
    echo.
    echo ERROR: Zipping failed.
    %PAUSE%
    exit /b 1
)
if exist "%ZIP%" del "%ZIP%"
timeout /t 3 /nobreak >nul
goto zip
:zipped

REM Clean PyInstaller working dirs (retry once if antivirus still holds a file)
rmdir /s /q build 2>nul
if exist build (
    timeout /t 3 /nobreak >nul
    rmdir /s /q build
)

echo.
echo === Build complete ===
echo Release folder: %REL%\
echo Release zip:    %ZIP%
%PAUSE%
