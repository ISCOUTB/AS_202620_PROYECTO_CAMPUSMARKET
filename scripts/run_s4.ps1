$ErrorActionPreference = "Stop"

Write-Host "Iniciando CampusMarket S4..."
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"

$backend = Start-Process `
    -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "backend.app.main:app", "--reload", "--port", "8000" `
    -PassThru

try {
    Push-Location "frontend/campusmarket"
    flutter pub get
    flutter run -d chrome --web-port 3000
}
finally {
    Pop-Location
    if (!$backend.HasExited) {
        Stop-Process -Id $backend.Id
    }
}
