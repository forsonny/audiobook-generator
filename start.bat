@echo off
color 0A
echo ===================================================
echo    Audiobook Generator - Application Launcher
echo ===================================================
echo.
echo Starting the application...
echo This will launch both the backend and frontend services.
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo ERROR: Python is not installed or not in the PATH.
    echo Please install Python 3.8 or newer and try again.
    goto error
)

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo ERROR: Node.js is not installed or not in the PATH.
    echo Please install Node.js v16+ and try again.
    goto error
)

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo ERROR: npm is not installed or not in the PATH.
    echo Please install Node.js with npm and try again.
    goto error
)

echo All dependencies found! Starting application...
echo.
echo Press Ctrl+C to stop all services.
echo.

npm run start:all
if %ERRORLEVEL% neq 0 goto error
goto end

:error
echo.
echo Application failed to start properly.
echo.
echo Troubleshooting options:
echo 1. Start backend only (for debugging)
echo 2. Start frontend only (if backend is already running)
echo 3. Exit
echo.
set /p option="Choose an option (1-3): "

if "%option%"=="1" (
    echo Starting backend only...
    npm run start:backend-only
    goto end
)
if "%option%"=="2" (
    echo Starting frontend only...
    npm run start:frontend-only
    goto end
)
if "%option%"=="3" (
    goto end
)

echo Invalid option. Exiting.

:end
echo.
echo Thank you for using Audiobook Generator!
echo. 