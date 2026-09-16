$ErrorActionPreference = "Stop"

Write-Host "Validando configuración de CampusMarket..."

$requiredVars = @(
    "CAMPUSMARKET_DB_HOST",
    "CAMPUSMARKET_DB_PORT",
    "CAMPUSMARKET_DB_USER",
    "CAMPUSMARKET_DB_PASSWORD",
    "CAMPUSMARKET_DB_NAME"
)

foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var)

    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "Falta configurar la variable de entorno $var."
    }
}

Write-Host "Verificando conexión con MySQL..."

python -c @"
import os
import pymysql

conexion = pymysql.connect(
    host=os.environ["CAMPUSMARKET_DB_HOST"],
    port=int(os.environ["CAMPUSMARKET_DB_PORT"]),
    user=os.environ["CAMPUSMARKET_DB_USER"],
    password=os.environ["CAMPUSMARKET_DB_PASSWORD"],
    database=os.environ["CAMPUSMARKET_DB_NAME"],
    connect_timeout=3,
)

with conexion.cursor() as cursor:
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()

conexion.close()

if resultado[0] != 1:
    raise RuntimeError("MySQL no respondió correctamente.")
"@

if ($LASTEXITCODE -ne 0) {
    throw "No fue posible establecer conexión con MySQL."
}

Write-Host "MySQL disponible."
Write-Host "Iniciando CampusMarket..."
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