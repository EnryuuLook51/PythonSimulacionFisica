# calculos_fisica.py
# =============================================================================
# CALCULOS_FISICA.PY - MÓDULO DE CÁLCULOS FÍSICOS
# =============================================================================
# Este módulo contiene todas las funciones relacionadas con los cálculos físicos

from graficos import crear_graficos
from textos import generar_analisis_completo
from animacion import generar_animaciones_colision

def calcular_tiempo_detencion_realista(velocidad_ms, tipo_impacto):
    """
    Calcula tiempos de detención más realistas basados en física real
    
    Args:
        velocidad_ms (float): Velocidad en m/s
        tipo_impacto (str): "sin_cinturon" o "con_cinturon"
    
    Returns:
        float: Tiempo de detención en segundos
    """
    if not isinstance(velocidad_ms, (int, float)):
        raise ValueError("La velocidad debe ser un número")
    if tipo_impacto == "sin_cinturon":
        return max(0.01, 0.015 + velocidad_ms * 0.002)
    else:  # con_cinturon
        tiempo_base = max(0.01, 0.015 + velocidad_ms * 0.002)
        factor_extension = 4 + (velocidad_ms / 30)
        return tiempo_base * factor_extension

def calcular_parametros_fisica(masa_cuerpo, velocidad_ms, tiempo_detencion):
    """
    Calcula los parámetros físicos para un escenario dado
    
    Args:
        masa_cuerpo (float): Masa en kg
        velocidad_ms (float): Velocidad en m/s
        tiempo_detencion (float): Tiempo de detención en segundos
    
    Returns:
        dict: Diccionario con todos los parámetros calculados
    """
    if not all(isinstance(x, (int, float)) for x in [masa_cuerpo, velocidad_ms, tiempo_detencion]):
        raise ValueError("Todos los parámetros deben ser números")
    if tiempo_detencion <= 0:
        raise ValueError("El tiempo de detención debe ser mayor a cero")
    
    delta_v = -velocidad_ms
    aceleracion = delta_v / tiempo_detencion
    fuerza = masa_cuerpo * aceleracion
    g_force = aceleracion / 9.81
    
    return {
        'aceleracion': aceleracion,
        'fuerza': fuerza,
        'g_force': g_force,
        'tiempo': tiempo_detencion
    }

def validar_parametros(masa_cuerpo, velocidad_kmh, tiempo_sin_cinturon=None, tiempo_con_cinturon=None):
    """
    Valida que los parámetros de entrada sean correctos
    
    Args:
        masa_cuerpo (float): Masa en kg
        velocidad_kmh (float): Velocidad en km/h
        tiempo_sin_cinturon (float, optional): Tiempo sin cinturón
        tiempo_con_cinturon (float, optional): Tiempo con cinturón
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not all(isinstance(x, (int, float)) for x in [masa_cuerpo, velocidad_kmh] if x is not None):
        return False, "❌ Error: Masa y velocidad deben ser números"
    if masa_cuerpo <= 0 or velocidad_kmh <= 0:
        return False, "❌ Error: La masa y velocidad deben ser mayores a cero"
    
    if tiempo_sin_cinturon is not None and tiempo_con_cinturon is not None:
        if not all(isinstance(x, (int, float)) for x in [tiempo_sin_cinturon, tiempo_con_cinturon]):
            return False, "❌ Error: Los tiempos deben ser números"
        if tiempo_sin_cinturon <= 0 or tiempo_con_cinturon <= 0:
            return False, "❌ Error: Los tiempos deben ser mayores a cero"
    
    return True, ""

def simular_colision(masa_cuerpo, velocidad_kmh, usar_tiempos_manuales, tiempo_con_cinturon_manual, tiempo_sin_cinturon_manual):
    """
    Ejecuta la simulación de colisión y genera gráficos y análisis textual.
    
    Args:
        masa_cuerpo (float): Masa del cuerpo en kg
        velocidad_kmh (float): Velocidad inicial en km/h
        usar_tiempos_manuales (bool): Si usar tiempos manuales o calculados
        tiempo_con_cinturon_manual (float): Tiempo manual con cinturón
        tiempo_sin_cinturon_manual (float): Tiempo manual sin cinturón
    
    Returns:
        tuple: (figura_matplotlib, texto_analisis, datos_simulacion)
    """
    try:
        # Validar parámetros básicos
        es_valido, mensaje_error = validar_parametros(masa_cuerpo, velocidad_kmh)
        if not es_valido:
            return None, mensaje_error, None
        
        # Convertir velocidad de km/h a m/s
        if not isinstance(velocidad_kmh, (int, float)):
            return None, "❌ Error: La velocidad debe ser un número válido", None
        velocidad_ms = float(velocidad_kmh) * 1000 / 3600

        # Decidir qué tiempos usar
        if usar_tiempos_manuales:
            es_valido, mensaje_error = validar_parametros(
                masa_cuerpo, velocidad_kmh, 
                tiempo_sin_cinturon_manual, tiempo_con_cinturon_manual
            )
            if not es_valido:
                return None, mensaje_error, None
            tiempo_sin_cinturon = float(tiempo_sin_cinturon_manual)
            tiempo_con_cinturon = float(tiempo_con_cinturon_manual)
            modo_calculo = "manual"
        else:
            tiempo_sin_cinturon = calcular_tiempo_detencion_realista(velocidad_ms, "sin_cinturon")
            tiempo_con_cinturon = calcular_tiempo_detencion_realista(velocidad_ms, "con_cinturon")
            modo_calculo = "realista"

        if not all(isinstance(x, (int, float)) for x in [tiempo_sin_cinturon, tiempo_con_cinturon]):
            return None, "❌ Error: Los tiempos calculados son inválidos", None

        # Calcular parámetros físicos
        parametros_sin = calcular_parametros_fisica(masa_cuerpo, velocidad_ms, tiempo_sin_cinturon)
        parametros_con = calcular_parametros_fisica(masa_cuerpo, velocidad_ms, tiempo_con_cinturon)

        # Crear gráficos
        fig = crear_graficos(
            tiempo_sin_cinturon, abs(parametros_sin['fuerza']), abs(parametros_sin['aceleracion']),
            tiempo_con_cinturon, abs(parametros_con['fuerza']), abs(parametros_con['aceleracion'])
        )

        # Generar análisis textual
        datos_simulacion = {
            'masa_cuerpo': masa_cuerpo,
            'velocidad_kmh': velocidad_kmh,
            'velocidad_ms': velocidad_ms,
            'modo_calculo': modo_calculo,
            'parametros_sin': parametros_sin,
            'parametros_con': parametros_con,
            'tiempo_sin_cinturon': tiempo_sin_cinturon,
            'tiempo_con_cinturon': tiempo_con_cinturon
        }
        
        analisis_texto = generar_analisis_completo(datos_simulacion)
        return fig, analisis_texto, datos_simulacion

    except Exception as e:
        return None, f"❌ Error en los cálculos: {str(e)}", None

def generar_animaciones(datos_simulacion):
    """
    Genera animaciones para los escenarios con y sin cinturón.
    
    Args:
        datos_simulacion (dict): Diccionario con los datos de la simulación
    
    Returns:
        tuple: (animacion_sin, animacion_con)
    """
    try:
        anim_sin, anim_con = generar_animaciones_colision(
            datos_simulacion['parametros_sin'],
            datos_simulacion['parametros_con'],
            datos_simulacion['velocidad_ms']
        )
        return anim_sin, anim_con
    except Exception as e:
        return None, f"❌ Error al generar animaciones: {str(e)}"