From the root of your project:
-
```
Sentinel/
│
├── Sentinel.pyw
├── Sentinel.spec
├── src/
├── installer/
├── dist/
└── ...
```
activate your virtual environment first.
```
.\.venv\Scripts\Activate.ps1
```
You should now see something like
```
(.venv) PS C:\Users\erik_\PycharmProjects\pythonProject\Programming\Sentinel>
```
Build Sentinel.exe
-
If you're using PowerShell instead of Command Prompt, use backticks instead of ^:


```
(.venv) PS C:\Users\erik_\PycharmProjects\pythonProject\programming\sentinel>

pyinstaller `
    --clean `
    --noconfirm `
    --onefile `
    --windowed `
    --name Sentinel `
    --paths src `
    Sentinel.pyw
```
The next command
-
Once the executable exists, package it into an installer:

``& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" `
    "installer\Sentinel.iss"``