@echo off
echo Instalando dependencias...
python -m pip install -r requirements.txt
echo.
echo Iniciando Security AI...
python -m streamlit run app.py
pause
