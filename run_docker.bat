@echo off
set /p VERSION=<version.txt
echo Building Docker image diploma-rest:%VERSION%...
docker build -f Dockerfile.dev -t diploma-rest:%VERSION% .

echo Checking for existing container...
docker ps -a | findstr "diploma-rest" >nul
if %errorlevel% equ 0 (
    echo Stopping and removing existing container...
    docker stop diploma-rest
    docker rm diploma-rest
)

echo Starting new container...
docker run -d -p 8000:8000 --name diploma-rest diploma-rest:%VERSION%

echo Container status:
docker ps | findstr "diploma-rest" 