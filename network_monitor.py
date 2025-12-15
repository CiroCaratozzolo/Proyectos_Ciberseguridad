import psutil
import time
import socket
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
# Puertos remotos considerados "seguros" o estándar (Web, DNS, Email)
# Si una conexión sale a uno de estos puertos, la ignoramos (para reducir ruido).
SAFE_PORTS = [80, 443, 53, 25, 587, 993, 465]

# Intervalo de escaneo en segundos
SCAN_INTERVAL = 5

def get_process_name(pid):
    """Obtiene el nombre del proceso dado su PID."""
    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "Desconocido"

def monitor_connections():
    print(f"[*] Iniciando Monitor de Conexiones...")
    print(f"[*] Ignorando puertos seguros: {SAFE_PORTS}")
    print(f"[*] Escaneando cada {SCAN_INTERVAL} segundos...\n")
    print(f"{'HORA':<20} {'PID':<10} {'PROCESO':<20} {'REMOTO':<25} {'ESTADO'}")
    print("-" * 90)

    # Conjunto para recordar conexiones ya alertadas y no repetir spam
    seen_connections = set()

    try:
        while True:
            # Obtiene todas las conexiones de red (inet = IPv4/IPv6)
            connections = psutil.net_connections(kind='inet')

            for conn in connections:
                # Solo nos interesan las conexiones ESTABLECIDAS (tráfico activo)
                if conn.status == psutil.CONN_ESTABLISHED:
                    
                    # Obtener datos de la conexión
                    remote_ip = conn.raddr.ip if conn.raddr else None
                    remote_port = conn.raddr.port if conn.raddr else None
                    pid = conn.pid
                    
                    # Si no hay IP remota (raro en established), saltar
                    if not remote_ip or not remote_port:
                        continue

                    # --- LÓGICA DE ALERTA ---
                    # Si el puerto remoto NO está en la lista segura
                    if remote_port not in SAFE_PORTS:
                        
                        # Crear una firma única para esta conexión
                        conn_signature = f"{pid}-{remote_ip}-{remote_port}"
                        
                        # Si es una conexión nueva que no hemos visto en esta sesión
                        if conn_signature not in seen_connections:
                            
                            process_name = get_process_name(pid)
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            remote_addr = f"{remote_ip}:{remote_port}"

                            # IMPRIMIR ALERTA
                            print(f"{timestamp:<20} {pid:<10} {process_name:<20} {remote_addr:<25} [ALERTA: Puerto inusual]")
                            
                            # Agregar a vistos para no repetir la alerta inmediatamente
                            seen_connections.add(conn_signature)
            
            # Pausa antes del siguiente escaneo
            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\n[*] Monitor detenido por el usuario.")

if __name__ == "__main__":
    monitor_connections()