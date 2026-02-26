# Quick Fix for bcrypt Import Error (Virtual Environment)

## Problem
`ModuleNotFoundError: No module named 'bcrypt'`

## You're in a Virtual Environment (venv)

Since you're using a virtual environment, **DO NOT use the `--user` flag**.

## Solution

### Step 1: Make sure your virtual environment is activated

You should see `(venv)` at the beginning of your PowerShell prompt:
```
(venv) PS C:\Users\LOQ\OneDrive\Desktop\flask>
```

### Step 2: Install packages (WITHOUT --user flag)

```powershell
pip install Flask mysql-connector-python bcrypt
```

Or install from requirements.txt:
```powershell
pip install -r requirements.txt
```

### Step 3: Run the application

```powershell
python app.py
```

## If Installation is Slow/Timing Out

Try these alternatives:

**Option 1: Install with increased timeout**
```powershell
pip install --timeout 300 Flask mysql-connector-python bcrypt
```

**Option 2: Install without cache**
```powershell
pip install --no-cache-dir Flask mysql-connector-python bcrypt
```

**Option 3: Install one at a time**
```powershell
pip install Flask
pip install mysql-connector-python
pip install bcrypt
```

## Verify Installation

After installation, verify all packages are installed:

```powershell
python -c "import flask; import bcrypt; import mysql.connector; print('✓ All packages installed successfully!')"
```

## Common Issues

**Issue**: "ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv."
- **Solution**: Remove `--user` flag (you're already in a virtual environment)

**Issue**: Network timeout errors
- **Solution**: Use `--timeout 300` or `--no-cache-dir` flags

**Issue**: Virtual environment not activated
- **Solution**: Run `.\venv\Scripts\Activate.ps1` first
