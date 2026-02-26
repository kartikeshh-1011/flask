# Quick Fix Guide - Flask Server Already Running

## Problem
When you run `python app.py`, nothing happens or a new CMD opens because the server is already running in the background.

## Solution

### Option 1: Use the Existing Server (RECOMMENDED)
Your Flask server is already running! Just open your browser and go to:

**http://127.0.0.1:5000**

The server has been running for over 12 minutes and is ready to use.

### Option 2: Restart the Server
If you need to restart:

1. **Find the terminal with the running server**
   - Look for a terminal window showing Flask output
   - Or check VS Code's terminal panel

2. **Stop the server**
   - Press `CTRL+C` in that terminal

3. **Start again**
   ```powershell
   python app.py
   ```

### Option 3: Kill the Process (If stuck)
If you can't find the terminal:

```powershell
# Find the process
netstat -ano | findstr :5000

# Kill it (replace PID with the number from above)
taskkill /PID <PID> /F

# Then start fresh
python app.py
```

## Quick Test
Open your browser and visit these URLs:

- **Home**: http://127.0.0.1:5000
- **Signup**: http://127.0.0.1:5000/signup
- **Login**: http://127.0.0.1:5000/login
- **Feedback**: http://127.0.0.1:5000/feedback

If these load, your server is working perfectly!

## Why This Happens
- Flask can only run one instance per port
- Port 5000 is already in use by your running server
- The second `python app.py` command fails silently because port is occupied

## Recommended Workflow
1. Start server once: `python app.py`
2. Keep that terminal open
3. Use your browser to test
4. Only restart when you make code changes
