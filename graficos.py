# =============================================================================
# GRAFICOS.PY - MÓDULO DE VISUALIZACIÓN
# =============================================================================
# Este módulo contiene todas las funciones para crear gráficos

import numpy as np
import matplotlib.pyplot as plt

# Configurar matplotlib
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def crear_grafico_fuerza_tiempo(ax, t_sin, f_sin, t_con, f_con):
    """
    Crea el gráfico de evolución de fuerza vs tiempo
    
    Args:
        ax: Subplot de matplotlib
        t_sin, f_sin: Tiempo y fuerza sin cinturón
        t_con, f_con: Tiempo y fuerza con cinturón
    """
    tiempo_max = max(t_sin, t_con) * 1.5
    tiempo_sin = np.linspace(0, tiempo_max, 1000)
    tiempo_con = np.linspace(0, tiempo_max, 1000)
    
    fuerza_sin_array = np.where(tiempo_sin <= t_sin, f_sin, 0)
    fuerza_con_array = np.where(tiempo_con <= t_con, f_con, 0)
    
    ax.plot(tiempo_sin, fuerza_sin_array, 'r-', linewidth=3, label=f'Sin Cinturón ({f_sin:,.0f} N)')
    ax.plot(tiempo_con, fuerza_con_array, 'b-', linewidth=3, label=f'Con Cinturón ({f_con:,.0f} N)')
    ax.axvline(x=t_sin, color='red', linestyle='--', alpha=0.7, label=f'Fin impacto s/c: {t_sin:.3f}s')
    ax.axvline(x=t_con, color='blue', linestyle='--', alpha=0.7, label=f'Fin impacto c/c: {t_con:.3f}s')
    
    ax.set_xlabel('Tiempo (segundos)', fontsize=12)
    ax.set_ylabel('Fuerza (Newtons)', fontsize=12)
    ax.set_title('⏱️ Evolución de la Fuerza Durante el Impacto', fontsize=14)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(0, tiempo_max)

def crear_grafico_aceleracion_tiempo(ax, t_sin, a_sin, t_con, a_con):
    """
    Crea el gráfico de evolución de aceleración vs tiempo
    
    Args:
        ax: Subplot de matplotlib
        t_sin, a_sin: Tiempo y aceleración sin cinturón
        t_con, a_con: Tiempo y aceleración con cinturón
    """
    tiempo_max = max(t_sin, t_con) * 1.5
    tiempo_sin = np.linspace(0, tiempo_max, 1000)
    tiempo_con = np.linspace(0, tiempo_max, 1000)
    
    aceleracion_sin_array = np.where(tiempo_sin <= t_sin, a_sin, 0)
    aceleracion_con_array = np.where(tiempo_con <= t_con, a_con, 0)
    
    ax.plot(tiempo_sin, aceleracion_sin_array, 'r-', linewidth=3, label=f'Sin Cinturón ({a_sin:.1f} m/s²)')
    ax.plot(tiempo_con, aceleracion_con_array, 'b-', linewidth=3, label=f'Con Cinturón ({a_con:.1f} m/s²)')
    ax.axvline(x=t_sin, color='red', linestyle='--', alpha=0.7)
    ax.axvline(x=t_con, color='blue', linestyle='--', alpha=0.7)
    
    ax.set_xlabel('Tiempo (segundos)', fontsize=12)
    ax.set_ylabel('Aceleración (m/s²)', fontsize=12)
    ax.set_title('🚀 Evolución de la Aceleración Durante el Impacto', fontsize=14)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(0, tiempo_max)

def crear_grafico_barras_fuerza(ax, f_sin, f_con):
    """
    Crea el gráfico de barras comparando fuerzas
    
    Args:
        ax: Subplot de matplotlib
        f_sin, f_con: Fuerzas sin y con cinturón
    """
    bars = ax.bar(['Sin Cinturón', 'Con Cinturón'], [f_sin, f_con], 
                  color=['#ff6b6b', '#4ecdc4'], alpha=0.8)
    ax.set_ylabel('Fuerza Máxima (Newtons)', fontsize=12)
    ax.set_title('💥 Comparación de Fuerza de Impacto', fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Añadir valores encima de las barras
    for bar, value in zip(bars, [f_sin, f_con]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * max(f_sin, f_con), 
                f'{value:,.0f} N', ha='center', va='bottom', fontsize=11, weight='bold')

def crear_grafico_barras_g_force(ax, g_sin, g_con):
    """
    Crea el gráfico de barras comparando fuerzas G
    
    Args:
        ax: Subplot de matplotlib
        g_sin, g_con: Fuerzas G sin y con cinturón
    """
    bars = ax.bar(['Sin Cinturón', 'Con Cinturón'], [g_sin, g_con], 
                  color=['#ff6b6b', '#4ecdc4'], alpha=0.8)
    ax.set_ylabel('Fuerzas G', fontsize=12)
    ax.set_title('🌍 Comparación de Fuerzas G Experimentadas', fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Líneas de referencia para niveles de peligro
    ax.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Umbral Alto (20G)')
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Umbral Crítico (50G)')
    ax.legend()
    
    # Añadir valores encima de las barras
    for bar, value in zip(bars, [g_sin, g_con]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * max(g_sin, g_con), 
                f'{value:.1f} G', ha='center', va='bottom', fontsize=11, weight='bold')

def crear_grafico_comparacion_completa(ax, t_sin, f_sin, a_sin, t_con, f_con, a_con):
    """
    Crea el gráfico de comparación completa de todos los parámetros
    
    Args:
        ax: Subplot de matplotlib
        t_sin, f_sin, a_sin: Tiempo, fuerza y aceleración sin cinturón
        t_con, f_con, a_con: Tiempo, fuerza y aceleración con cinturón
    """
    # Calcular fuerzas G
    g_sin = a_sin / 9.81
    g_con = a_con / 9.81
    
    categorias = ['Fuerza\n(kN)', 'Aceleración\n(m/s²)', 'Fuerzas G', 'Tiempo\n(s)']
    valores_sin = [f_sin/1000, a_sin, g_sin, t_sin]  # Fuerza en kN para mejor visualización
    valores_con = [f_con/1000, a_con, g_con, t_con]
    
    x = np.arange(len(categorias))
    width = 0.35
    
    bars_sin = ax.bar(x - width/2, valores_sin, width, label='Sin Cinturón', 
                      color='#ff6b6b', alpha=0.8)
    bars_con = ax.bar(x + width/2, valores_con, width, label='Con Cinturón', 
                      color='#4ecdc4', alpha=0.8)
    
    ax.set_xlabel('Parámetros Físicos', fontsize=12)
    ax.set_ylabel('Valores', fontsize=12)
    ax.set_title('📊 Comparación Directa de Todos los Parámetros', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Añadir valores encima de cada barra
    for i, (bar_sin, bar_con, val_sin, val_con) in enumerate(zip(bars_sin, bars_con, valores_sin, valores_con)):
        # Formatear valores según el tipo
        if i == 0:  # Fuerza
            format_sin = f'{val_sin:.1f}'
            format_con = f'{val_con:.1f}'
        elif i == 1:  # Aceleración
            format_sin = f'{val_sin:.1f}'
            format_con = f'{val_con:.1f}'
        elif i == 2:  # Fuerzas G
            format_sin = f'{val_sin:.1f}'
            format_con = f'{val_con:.1f}'
        else:  # Tiempo
            format_sin = f'{val_sin:.3f}'
            format_con = f'{val_con:.3f}'
        
        ax.text(bar_sin.get_x() + bar_sin.get_width()/2, bar_sin.get_height() + 0.01 * max(max(valores_sin), max(valores_con)), 
                format_sin, ha='center', va='bottom', fontsize=10, weight='bold')
        ax.text(bar_con.get_x() + bar_con.get_width()/2, bar_con.get_height() + 0.01 * max(max(valores_sin), max(valores_con)), 
                format_con, ha='center', va='bottom', fontsize=10, weight='bold')

def crear_graficos(t_sin, f_sin, a_sin, t_con, f_con, a_con):
    """
    Función principal que crea todos los gráficos de la simulación
    
    Args:
        t_sin, f_sin, a_sin: Tiempo, fuerza y aceleración sin cinturón
        t_con, f_con, a_con: Tiempo, fuerza y aceleración con cinturón
    
    Returns:
        matplotlib.figure.Figure: Figura completa con todos los gráficos
    """
    # Crear figura con 5 subgráficos
    fig = plt.figure(figsize=(18, 16))
    fig.suptitle('🚗 Análisis Completo de Impacto Vehicular', fontsize=18, weight='bold')
    
    # Definir el grid de subplots
    ax1 = plt.subplot(3, 2, 1)  # Fuerza vs tiempo
    ax2 = plt.subplot(3, 2, 2)  # Aceleración vs tiempo
    ax3 = plt.subplot(3, 2, 3)  # Comparación fuerzas (barras)
    ax4 = plt.subplot(3, 2, 4)  # Fuerzas G (barras)
    ax5 = plt.subplot(3, 1, 3)  # Gráfico de comparación (ocupa toda la fila inferior)

    # Crear cada gráfico
    crear_grafico_fuerza_tiempo(ax1, t_sin, f_sin, t_con, f_con)
    crear_grafico_aceleracion_tiempo(ax2, t_sin, a_sin, t_con, a_con)
    crear_grafico_barras_fuerza(ax3, f_sin, f_con)
    crear_grafico_barras_g_force(ax4, a_sin / 9.81, a_con / 9.81)
    crear_grafico_comparacion_completa(ax5, t_sin, f_sin, a_sin, t_con, f_con, a_con)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig