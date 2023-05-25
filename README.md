# Linus Process Checker via SSH

An example of a 'scripty' program written in less than 45 minutes to notify me if any of my processes have exited on any of my playground servers.


## Paramiko
Paramiko is one of my most appreciated recent discoveries, I've also used it to control linux machines from a web dashboard from which an approved user can click a few buttons to restart a server, run a process outside of its scheduled time, view logs and schedule tasks without needing to know bash.

## .BAT
Also, for processes that run on windows, I enjoy the .BAT file approach to scripting run times as opposed to compiling .exes. It allows me to quickly edit code for processes running on development windows servers.

```bash
@echo off
set workdir=C:\path\to\your\project\folder
set venv=.\venv\Scripts\activate.bat
set scriptname=linux_process_tracker.py
cmd /k "cd /d %workdir% & %venv% & cd /d %workdir% & python .\%scriptname%"
```