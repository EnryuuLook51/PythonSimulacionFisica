# animacion.py
# =============================================================================
# ANIMACION.PY - MÓDULO DE ANIMACIÓN VISUAL
# =============================================================================
# Este módulo contiene funciones para generar animaciones mejoradas del movimiento durante la colisión

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import uuid
from matplotlib.patches import Ellipse, Rectangle

def generar_animacion(tiempo_detencion, aceleracion, velocidad_inicial, nombre_archivo, con_cinturon):
    """
    Genera una animación mejorada del movimiento del cuerpo durante la colisión y la guarda como MP4.
    
    Args:
        tiempo_detencion (float): Tiempo de detención en segundos
        aceleracion (float): Aceleración (negativa) en m/s²
        velocidad_inicial (float): Velocidad inicial en m/s
        nombre_archivo (str): Nombre base del archivo MP4 de salida
        con_cinturon (bool): Indica si se usa cinturón de seguridad
    
    Returns:
        str: Ruta al archivo MP4 generado
    """
    # Generar puntos de tiempo
    t = np.linspace(0, tiempo_detencion, 100)
    # Calcular posiciones usando x(t) = v0*t + (1/2)*a*t^2
    posicion = velocidad_inicial * t + 0.5 * aceleracion * t**2
    # Asegurar que las posiciones no sean negativas
    posicion = np.maximum(posicion, 0)
    # Calcular velocidades instantáneas: v(t) = v0 + a*t
    velocidades = velocidad_inicial + aceleracion * t
    # Calcular fuerzas instantáneas: F = m*a (usamos masa=70 kg para visualización)
    fuerzas = 70 * abs(aceleracion) * np.where(t <= tiempo_detencion, 1, 0)
    fuerzas_g = fuerzas / (70 * 9.81)

    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, max(posicion) * 1.5 if max(posicion) > 0 else 1.5)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('Distancia (m)', fontsize=12)
    ax.set_ylabel('Posición Y', fontsize=12)
    ax.set_title(f'Movimiento del Cuerpo ({"Con Cinturón" if con_cinturon else "Sin Cinturón"})', fontsize=14, weight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)

    # Fondo del vehículo (rectángulo gris)
    vehiculo = Rectangle((-0.5, -1), 2, 2, facecolor='lightgray', alpha=0.5)
    ax.add_patch(vehiculo)

    # Obstáculo (parabrisas/pared)
    obstaculo_x = max(posicion) * 1.2 if max(posicion) > 0 else 1.0
    ax.axvline(x=obstaculo_x, color='red', linestyle='--', alpha=0.7, label='Obstáculo')

    # Figura humana (cabeza: elipse, cuerpo: rectángulo)
    cabeza = Ellipse((0, 0.2), 0.2, 0.3, color='tan')
    cuerpo = Rectangle((-0.1, -0.3), 0.2, 0.5, color='tan')
    ax.add_patch(cabeza)
    ax.add_patch(cuerpo)

    # Cinturón de seguridad (si aplica)
    cinturon = None
    if con_cinturon:
        cinturon, = ax.plot([], [], 'k-', linewidth=3, label='Cinturón')
    
    # Texto dinámico para velocidad, fuerza y fuerzas G
    texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10, verticalalignment='top', 
                         bbox=dict(facecolor='white', alpha=0.8))

    ax.legend(loc='upper right')

    # Función de inicialización
    def init():
        cabeza.center = (0, 0.2)
        cuerpo.set_xy((-0.1, -0.3))
        if con_cinturon:
            cinturon.set_data([], [])
        texto_info.set_text('')
        return [cabeza, cuerpo, texto_info] + ([cinturon] if con_cinturon else [])

    # Función de animación
    def animate(i):
        x = posicion[i]
        cabeza.center = (x, 0.2)
        cuerpo.set_xy((x-0.1, -0.3))
        
        if con_cinturon:
            # Dibujar cinturón desde el hombro hasta la cadera
            cinturon.set_data([x-0.1, x+0.1], [0.4, -0.2])
        
        # Actualizar texto con información
        texto_info.set_text(
            f'Velocidad: {velocidades[i]:.1f} m/s\n'
            f'Fuerza: {fuerzas[i]:,.0f} N\n'
            f'Fuerzas G: {fuerzas_g[i]:.1f} G'
        )
        
        return [cabeza, cuerpo, texto_info] + ([cinturon] if con_cinturon else [])

    # Crear animación
    ani = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init, blit=True, interval=20)

    # Generar nombre de archivo único
    unique_filename = f"{nombre_archivo}_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join("animations", unique_filename)

    # Crear directorio si no existe
    os.makedirs("animations", exist_ok=True)

    # Guardar animación
    ani.save(output_path, writer='ffmpeg', fps=30)
    plt.close(fig)

    return output_path

def generar_animaciones_colision(parametros_sin, parametros_con, velocidad_ms):
    """
    Genera animaciones para los escenarios con y sin cinturón.
    
    Args:
        parametros_sin (dict): Parámetros físicos sin cinturón
        parametros_con (dict): Parámetros físicos con cinturón
        velocidad_ms (float): Velocidad inicial en m/s
    
    Returns:
        tuple: Rutas a los archivos MP4 (sin cinturón, con cinturón)
    """
    # Generar animación sin cinturón
    anim_sin = generar_animacion(
        tiempo_detencion=parametros_sin['tiempo'],
        aceleracion=parametros_sin['aceleracion'],
        velocidad_inicial=velocidad_ms,
        nombre_archivo="sin_cinturon",
        con_cinturon=False
    )
    
    # Generar animación con cinturón
    anim_con = generar_animacion(
        tiempo_detencion=parametros_con['tiempo'],
        aceleracion=parametros_con['aceleracion'],
        velocidad_inicial=velocidad_ms,
        nombre_archivo="con_cinturon",
        con_cinturon=True
    )
    
    return anim_sin, anim_con