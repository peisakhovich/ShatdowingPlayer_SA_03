@echo off
cd /d C:\Users\liudm\SadowingApp\SA_03\SA_03
call .venv\Scripts\activate
start "" http://127.0.0.1:8000/
mkdocs serve