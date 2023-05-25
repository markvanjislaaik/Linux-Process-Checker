@echo off
set workdir=C:\path\to\your\project\folder
set venv=.\venv\Scripts\activate.bat
set scriptname=linux_process_tracker.py
cmd /k "cd /d %workdir% & %venv% & cd /d %workdir% & python .\%scriptname%"