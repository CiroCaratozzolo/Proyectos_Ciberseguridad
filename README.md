ES
👁️ Real-Time Network Connection Monitor (Blue Team Tool)
Este proyecto implementa un sistema de monitoreo de host (HIDS ligero) diseñado para auditar las conexiones de red salientes en tiempo real. 
Su objetivo es detectar rápidamente comportamientos anómalos o sospechosos, como la comunicación con servidores Command & Control (C2) o intentos de exfiltración de datos.

| Característica | Propósito de Seguridad | Librería / Técnica |
|----------------|------------------------|--------------------|
| Monitoreo Continuo | Audita el sistema en intervalos definidos buscando persistencia | Bucle while True con time.sleep() |
| Whitelisting Inteligente | Filtra el ""ruido"" de conexiones comunes (HTTPS, DNS), enfocando la atención en las anomalías. | Lista SAFE_PORTS | 
| Mapeo de Procesos | Identifica el ejecutable (chrome.exe, python.exe) responsable de la conexión. | psutil.Process(pid) |
| Detección ESTABLISHED | Se centra solo en conexiones activas que están transmitiendo datos. | psutil.CONN_ESTABLISHED |
| Logging Persistente | Guarda todas las alertas en un archivo de registro para análisis forense posterior. | Módulo logging de Python |

🛠️ Tecnologías
Python 3

Psutil: Para interactuar con el sistema operativo y acceder a la tabla de conexiones de red.

Logging: Para gestionar la escritura de alertas en el archivo alertas_red.log.

🚀 Instalación y Requerimientos
1) Clonar el repositorio (bash):
   git clone https://github.com/TuUsuario/Network-Monitor-Python.git
   cd Network-Monitor-Python

2) Crear e instalar el entorno virtual:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install psutil

💻 Uso (Ejecución y Automatización)

1. Ejecución Manual (Consola)
Ejecutar el script directamente para ver las alertas en tiempo real:
  python network_monitor.py
  # Presione Ctrl + C para detener el monitoreo.
  
2. Automatización (Persistencia)
Para un monitoreo 24/7, el script está configurado para ejecutarse en segundo plano (headless) utilizando el módulo logging.
Windows: Se recomienda configurarlo mediante el Programador de Tareas (Task Scheduler) para que inicie automáticamente al encender o iniciar sesión,
asegurando que el proceso python.exe corra permanentemente en segundo plano.

🧠 Aprendizajes Clave (Blue Team Focus)
Este proyecto me permitió profundizar en los siguientes conceptos de ciberseguridad:

1) Diferenciación de Sockets: Entendí cómo el sistema operativo diferencia entre listening sockets (puertos a la escucha) y established sockets (conexiones activas), y por qué el estado ESTABLISHED es crucial para la detección de amenazas.

2) Estrategias de Monitoreo: Apliqué el principio de reducción de ruido mediante el whitelisting de puertos comunes para hacer el sistema de alerta más eficiente y menos propenso a los Falsos Positivos.

3) Persistencia: Implementé soluciones para que el script pueda funcionar como un servicio básico del sistema, una habilidad fundamental en la detección y respuesta.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
EN
👁️ Real-Time Network Connection Monitor (Blue Team Tool)
This project implements a lightweight Host Intrusion Detection System (HIDS) designed to audit outbound network connections in real-time.

Its goal is to quickly detect anomalous or suspicious behaviors, such as communication with Command & Control (C2) servers or data exfiltration attempts.

| Feature | Security Purpose | Library / Technique |
|----------------|------------------------|--------------------|
| Continuous Monitoring | Audits the system at defined intervals, checking for connection persistence. | while True loop with time.sleep() |
| Intelligent Whitelisting | Filters out "noise" from common connections (HTTPS, DNS), focusing attention on anomalies. | SAFE_PORTS list | 
| Process Mapping | Identifies the executable (chrome.exe, python.exe) responsible for the connection. | psutil.Process(pid) |
| ESTABLISHED Detection | Focuses only on active connections that are currently transmitting data. | psutil.CONN_ESTABLISHED |
| Persistent Logging | Saves all alerts to a log file for subsequent forensic analysis. | Python's logging module |

🛠️ Technologies
Python 3

Psutil: For interacting with the operating system and accessing the network connection table.

Logging: To manage the writing of alerts to the alertas_red.log file.

🚀 Installation and Requirements
1) Clone the repository (bash):
  git clone https://github.com/YourUsername/Network-Monitor-Python.git
  cd Network-Monitor-Python
2) Create and install the virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install psutil

💻 Usage (Execution and Automation)
1. Manual Execution (Console)
Run the script directly to view alerts in real-time:
  python network_monitor.py
  # Press Ctrl + C to stop the monitoring.
2. Automation (Persistence)
For 24/7 monitoring, the script is configured to run headless (in the background) using the logging module.

Windows: It is recommended to set it up using the Task Scheduler so that it starts automatically upon boot or login, 
ensuring the python.exe process runs permanently in the background.

🧠 Key Learnings (Blue Team Focus)
This project allowed me to gain a deeper understanding of the following cybersecurity concepts:

1) Socket Differentiation: I understood how the operating system differentiates between listening sockets (ports awaiting connection) and established sockets (active connections), and why the ESTABLISHED state is crucial for threat detection.

2) Monitoring Strategies: I applied the principle of noise reduction by whitelisting common ports to make the alert system more efficient and less prone to False Positives.

3) Persistence: I implemented solutions so the script can function as a basic system service, a fundamental skill in detection and response.
