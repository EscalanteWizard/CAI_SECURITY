# Prototipo CAI Security

Este proyecto es un prototipo académico para una actividad de Design Thinking.

La aplicación simula la plataforma de **CAI Security**, un sistema de seguridad
tecnológica con:

- Cámaras conectadas.
- Sensores de barrera láser en el perímetro.
- Detección simulada de movimiento sospechoso.
- Reconocimiento facial por IA simulada, con base de datos ficticia de personas registradas.
- Sistema de contramedidas de disuasión no letal (conceptual y ficticio).
- Alertas al usuario con nivel de riesgo.
- Vista simulada de cámaras.
- Opción de contactar vigilancia.
- Opción de marcar una alerta como falsa alarma.
- Historial de eventos.
- Interfaz con tema claro/oscuro, con la identidad visual de CAI Security.

## Importante

El prototipo NO utiliza cámaras, sensores, inteligencia artificial ni sustancias
reales. La idea es demostrar de forma visual y funcional cómo sería la experiencia
del usuario en el producto final. El módulo de "Contramedidas" es completamente
ficticio: no describe ni implementa ningún dispositivo o sustancia real.

---

# Cómo correrlo en Visual Studio Code

## Opción 1: Windows

1. Abra esta carpeta en Visual Studio Code.
2. Abra una terminal en VS Code.
3. Ejecute:

```bash
python -m pip install -r requirements.txt
```

4. Luego ejecute:

```bash
python -m streamlit run app.py
```

También puede intentar abrir `ejecutar_windows.bat`.

---

## Opción 2: macOS o Linux

1. Abra esta carpeta en Visual Studio Code.
2. Abra una terminal.
3. Ejecute:

```bash
python3 -m pip install -r requirements.txt
```

4. Luego ejecute:

```bash
python3 -m streamlit run app.py
```

También puede ejecutar:

```bash
bash ejecutar_mac_linux.sh
```

---

# Cómo hacer la demostración en clase

1. Abra la aplicación.
2. Enseñe el Panel principal (cámaras, sensores láser y sistema de disuasión).
3. Presione `🌙 Modo oscuro` en la barra lateral para mostrar el cambio de tema.
4. Presione `Simular movimiento sospechoso`.
5. Muestre la alerta y sus opciones: ver cámara, contactar vigilancia, falsa alarma
   y activar contramedida.
6. Entre a la sección Sensores láser y presione `Simular corte de haz láser`.
7. Entre a la sección Reconocimiento facial y presione `Simular detección de rostro`
   un par de veces (algunas detecciones serán "Autorizado" y otras "Desconocido").
8. Entre a la sección Contramedidas y muestre la activación simulada por zona.
9. Presione `Contactar vigilancia` y muestre el mensaje de confirmación.
10. Reinicie la demostración.
11. Enseñe el Historial con todos los eventos generados.

Con esto se demuestra el flujo completo del prototipo:

Cámara / Sensor láser / Reconocimiento facial -> IA -> Alerta -> Usuario -> Vigilancia / Contramedida
