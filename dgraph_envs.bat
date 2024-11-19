@echo off
echo Configurando entorno virtual para Dgraph...
python -m venv dgraph\venv
call dgraph\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r dgraph\requirements.txt
deactivate
echo Entorno virtual para Dgraph configurado.
pause