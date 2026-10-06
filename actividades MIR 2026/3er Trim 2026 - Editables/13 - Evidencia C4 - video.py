# =====================================================
# Recibe numero de sensor por Serial y reproduce Audio/Video
# Requiere: pip install pyserial python-vlc
# =====================================================
import serial
import serial.tools.list_ports
import vlc
import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- Variables Globales ---
PUERTO_SERIAL = ""
archivos_asignados = {} 
programa_corriendo = True  # Flag para detener el hilo del Arduino

# --- Estado de los reproductores ---
video_activo = False
instancia_vlc = vlc.Instance("--no-video-title-show", "--quiet")
reproductor_audio = instancia_vlc.media_player_new()
reproductor_video = None
hilo_video = None
ventana_video = None
arduino = None

# =====================================================
# INTERFAZ DE CONFIGURACIÓN INICIAL
# =====================================================
def iniciar_configuracion():
    global PUERTO_SERIAL, archivos_asignados
    
    ventana_config = tk.Tk()
    ventana_config.title("Configuración de Sensores")
    ventana_config.geometry("550x450")
    ventana_config.eval('tk::PlaceWindow . center')

    variables_rutas = {}

    def seleccionar_archivo(num_sensor):
        if num_sensor == 5:
            tipos = [("Video", "*.mp4 *.avi *.mkv *.mov *.mpeg")]
        else:
            tipos = [("Audio", "*.mp3 *.wav *.opus *.ogg *.m4a")]
        
        ruta = filedialog.askopenfilename(
            title=f"Selecciona archivo para Sensor {num_sensor}", 
            filetypes=tipos + [("Todos los archivos", "*.*")]
        )
        if ruta:
            variables_rutas[num_sensor].set(ruta)

    def guardar_y_continuar():
        global PUERTO_SERIAL
        PUERTO_SERIAL = combo_puertos.get()
        
        if not PUERTO_SERIAL:
            messagebox.showwarning("Falta COM", "Por favor selecciona el puerto COM.")
            return

        for i in range(1, 8):
            ruta = variables_rutas[i].get()
            if ruta:
                archivos_asignados[i] = ruta

        ventana_config.destroy()

    tk.Label(ventana_config, text="1. Puerto COM:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    puertos = [port.device for port in serial.tools.list_ports.comports()]
    combo_puertos = ttk.Combobox(ventana_config, values=puertos, width=15)
    if puertos: combo_puertos.current(0)
    combo_puertos.pack(pady=5)

    tk.Label(ventana_config, text="2. Asigna los archivos a cada sensor:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
    frame_archivos = tk.Frame(ventana_config)
    frame_archivos.pack(fill="x", padx=20)

    for i in range(1, 8):
        fila = tk.Frame(frame_archivos)
        fila.pack(fill="x", pady=2)
        tipo_texto = "(Video)" if i == 5 else "(Audio)"
        tk.Label(fila, text=f"Sensor {i} {tipo_texto}:", width=15, anchor="w").pack(side="left")
        var_ruta = tk.StringVar()
        variables_rutas[i] = var_ruta
        tk.Entry(fila, textvariable=var_ruta, state="readonly", width=40).pack(side="left", padx=5)
        tk.Button(fila, text="Buscar...", command=lambda num=i: seleccionar_archivo(num)).pack(side="left")

    tk.Button(ventana_config, text="Iniciar Programa", command=guardar_y_continuar, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=20)
    ventana_config.mainloop()

# =====================================================
# FUNCIONES DE REPRODUCCIÓN
# =====================================================

def cerrar_ventana_video():
    global ventana_video
    if ventana_video:
        ventana_video.destroy()
        ventana_video = None

def reproducir_video_en_hilo(archivo_video):
    global video_activo, reproductor_video, ventana_video
    ventana_video = tk.Tk()
    ventana_video.configure(background="black")
    ventana_video.attributes("-fullscreen", True)
    ventana_video.attributes("-topmost", True)
    
    handle = ventana_video.winfo_id()
    reproductor_video = instancia_vlc.media_player_new()
    reproductor_video.set_media(instancia_vlc.media_new(archivo_video))
    reproductor_video.set_hwnd(handle)
    reproductor_video.play()

    while video_activo:
        ventana_video.update()
        estado = reproductor_video.get_state()
        if estado in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            break
        time.sleep(0.05)

    reproductor_video.stop()
    cerrar_ventana_video()

def reproducir(numero_sensor):
    global video_activo, reproductor_video, hilo_video
    if numero_sensor not in archivos_asignados: return
    archivo = archivos_asignados[numero_sensor]

    if numero_sensor == 5:
        if not video_activo:
            video_activo = True
            hilo_video = threading.Thread(target=reproducir_video_en_hilo, args=(archivo,), daemon=True)
            hilo_video.start()
        else:
            video_activo = False
        return

    reproductor_audio.stop()
    reproductor_audio.set_media(instancia_vlc.media_new(archivo))
    reproductor_audio.play()

# =====================================================
# BUCLE DE ARDUINO (EN HILO SEPARADO)
# =====================================================
def bucle_arduino():
    global programa_corriendo, arduino
    print(f"Escuchando Arduino en {PUERTO_SERIAL}...")
    while programa_corriendo:
        try:
            if arduino and arduino.in_waiting > 0:
                linea = arduino.readline().decode("utf-8").strip()
                if linea.isdigit():
                    num = int(linea)
                    if 1 <= num <= 7: reproducir(num)
        except:
            break
        time.sleep(0.1)

# =====================================================
# VENTANA DE CONTROL FINAL
# =====================================================
def finalizar_todo():
    """Detiene todo inmediatamente sin preguntar."""
    global programa_corriendo, arduino
    programa_corriendo = False
    if arduino: 
        arduino.close()
    reproductor_audio.stop()
    if reproductor_video: 
        reproductor_video.stop()
    ventana_control.destroy()

# --- EJECUCIÓN ---
iniciar_configuracion()

if PUERTO_SERIAL:
    try:
        arduino = serial.Serial(PUERTO_SERIAL, baudrate=9600, timeout=1)
        time.sleep(2)
        
        # Iniciar lectura del Arduino en segundo plano
        hilo_arduino = threading.Thread(target=bucle_arduino, daemon=True)
        hilo_arduino.start()

        # Crear pequeña ventana de control
        ventana_control = tk.Tk()
        ventana_control.title("Programa Activo")
        ventana_control.geometry("300x150")
        ventana_control.attributes("-topmost", True) # Siempre visible
        
        tk.Label(ventana_control, text="El programa está funcionando", font=("Arial", 10)).pack(pady=10)
        tk.Label(ventana_control, text=f"Puerto: {PUERTO_SERIAL}", fg="blue").pack()
        
        btn_salir = tk.Button(ventana_control, text="DETENER Y SALIR", 
                              command=finalizar_todo, bg="red", fg="white", 
                              font=("Arial", 10, "bold"), padx=20, pady=10)
        btn_salir.pack(pady=20)

        ventana_control.protocol("WM_DELETE_WINDOW", finalizar_todo)
        ventana_control.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al Arduino: {e}")