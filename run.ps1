Set-Location $PSScriptRoot

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm is not installed. Install Node.js from https://nodejs.org and try again."
    exit 1
}

npm install
npm run dev