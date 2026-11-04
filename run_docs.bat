@echo off
cd /d C:\Users\pga\SadowingApp\ShatdowingPlayer_SA_03
call .venv\Scripts\activate
start "" http://127.0.0.1:8000/
python -m mkdocs serve