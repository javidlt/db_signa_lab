@echo off
echo Configurando entorno virtual para MongoDB...
python -m venv mongo_db\venv
call mongo_db\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r mongo_db\requirements.txt
deactivate
echo Entorno virtual para MongoDB configurado.
pause