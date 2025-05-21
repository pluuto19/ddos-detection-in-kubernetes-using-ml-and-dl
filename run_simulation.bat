@echo off
echo DDoS Detection in Kubernetes Simulation
echo =====================================
echo.

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python 3.6+ and try again.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
pip show influxdb-client >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install influxdb-client
)

echo.
echo Starting the simulation...
echo.
cd simulation
python integrated_simulation.py

pause 