#!/usr/bin/env python3
# scan_and_report.py
# Uso: python3 scan_and_report.py 192.168.1.10 1 1024 output.csv

import socket
import csv 
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime 

def scan_port(target, port, timeout=0.6): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    # Inicializa el banner con un valor por defecto para puertos cerrados
    banner_info = "Closed/Filtered" 

    try: 
        s.connect((target, port)) 
        
        # --- LÓGICA DE BANNER GRABBING ---
        try:
            # Establece un timeout más corto para la recepción del banner
            s.settimeout(0.5) 
            
            # Intenta recibir hasta 1024 bytes de datos
            data = s.recv(1024)
            
            # Decodifica, limpia y captura solo la primera línea del banner
            banner_info = data.decode('utf-8', errors='ignore').strip().split('\n')[0]
            
            # Si el banner está vacío después de limpiar (ej. solo recibe un byte vacío)
            if not banner_info: 
                banner_info = "Open (No Banner Info)" 

        except socket.timeout:
            banner_info = "Open (No Immediate Banner)"
        except Exception as e:
            # Maneja otros errores de recepción (ej. Connection Reset)
            banner_info = f"Open (Error: {type(e).__name__})" 
        # ---------------------------------
        
        s.close() 
        # Devuelve el puerto, True (abierto) y la info del banner
        return (port, True, banner_info) 

    except Exception: 
        s.close()
        # Devuelve el puerto, False (cerrado/filtrado) y el valor por defecto
        return (port, False, banner_info)

""" Explicacion de la función scan_port():
1) Crea un objeto socket y lo asigna a la variable s.
2) socket.AF_INET indica la familia de direcciones IPv4.
3) socket.SOCK_STREAM indica un socket orientado a conexión (stream), es decir TCP.
Resultado: s es un socket TCP/IPv4 que puede usarse para connect(), bind(), listen(), send() y recv() (comportamiento por defecto en modo bloqueo a menos que cambies opciones como settimeout()).
Alternativas: AF_INET6 para IPv6, SOCK_DGRAM para UDP.
"""

def main(): # Función principal. Acá se maneja la entrada y salida del programa.
    if len(sys.argv) < 5: # Verifica que se pasen los argumentos necesarios.
        print("Uso: python3 scan_and_report.py <target> <port_start> <port_end> <output.csv>") # Mensaje de uso
        sys.exit(1) # Sale del programa con código de error 1.

    target = sys.argv[1] # Dirección IP o hostname objetivo
    start = int(sys.argv[2]) # Puerto inicial
    end = int(sys.argv[3]) # Puerto final
    out_file = sys.argv[4] # Archivo de salida CSV
    ports = range(start, end + 1) # Rango de puertos a escanear

    results = [] # Lista para almacenar resultados
    with ThreadPoolExecutor(max_workers=200) as exe: # Usa "hilos" para escanear puertos en paralelo
        future_to_port = {exe.submit(scan_port, target, p): p for p in ports} # Mapea futuros a puertos
        for fut in as_completed(future_to_port): # Itera sobre los futuros a medida que se completan
            p = future_to_port[fut] # Obtiene el puerto correspondiente al futuro
            try: # Intenta obtener el resultado del futuro
                port, is_open = fut.result() # Obtiene el resultado del escaneo
                results.append((port, is_open)) # Almacena el resultado
            except Exception as e: # Maneja excepciones
                results.append((p, False)) # Si hay error, marca el puerto como cerrado

    # write CSV
    timestamp = datetime.now().isoformat() # Marca de tiempo del escaneo
    with open(out_file, "w", newline="") as f: # Abre el archivo CSV para escritura
        writer = csv.writer(f) # Crea un escritor CSV
        writer.writerow(["target", "scan_time", "port", "open"]) # Escribe la cabecera
        for port, openflag in sorted(results): # Escribe los resultados
            writer.writerow([target, timestamp, port, openflag]) # Escribe cada fila

    open_ports = [p for p,op in results if op] # Lista de puertos abiertos
    print(f"Scan completo. Puertos abiertos: {open_ports}") # Muestra los puertos abiertos
    print(f"Reporte: {out_file}") # Muestra el archivo de reporte

if __name__ == "__main__": 
    main() 
