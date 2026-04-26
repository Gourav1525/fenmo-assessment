# Run both backend and frontend together
Write-Host "Starting Expense Tracker..."

# Start backend in background
Write-Host "Starting backend..."
Start-Job -ScriptBlock {
    & "c:\Users\goldi\Documents\fenmo-assessment\venv\Scripts\python.exe" -m uvicorn api.index:app --reload
} -Name "BackendJob"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "Starting frontend..."
& "c:\Users\goldi\Documents\fenmo-assessment\venv\Scripts\streamlit.exe" run frontend/app.py

# When frontend stops, stop backend
Write-Host "Stopping backend..."
Stop-Job -Name "BackendJob"