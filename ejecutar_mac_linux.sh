#!/bin/bash
echo "Instalando dependencias..."
python3 -m pip install -r requirements.txt
echo ""
echo "Iniciando Security AI..."
python3 -m streamlit run app.py
