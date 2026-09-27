$ErrorActionPreference = "Stop"

Write-Host "Testing EduGenie..."

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/health" `
    -Method Get

$response | ConvertTo-Json