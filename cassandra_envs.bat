@echo off
echo Configurando entorno virtual para Cassandra...
python -m venv cassandra\venv
call cassandra\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r cassandra\requirements.txt
deactivate
echo Entorno virtual para Cassandra configurado.
echo Todos los entornos virtuales han sido configurados correctamente.
pause
