# =============================================================================
# TEXTOS.PY - MÓDULO DE ANÁLISIS TEXTUAL
# =============================================================================
# Este módulo contiene todas las funciones para generar análisis textuales

def generar_explicacion_modo_calculo(datos):
    """
    Genera la explicación específica según el modo de cálculo utilizado
    
    Args:
        datos (dict): Diccionario con todos los datos de la simulación
    
    Returns:
        str: Texto explicativo del modo de cálculo
    """
    modo = datos['modo_calculo']
    tiempo_sin = datos['tiempo_sin_cinturon']
    tiempo_con = datos['tiempo_con_cinturon']
    
    if modo == "realista":
        return f"""
### 🔬 **Análisis Físico Realista Aplicado:**

**¿Cómo se determinaron los tiempos?**
- **Sin cinturón:** Tiempo calculado = **{tiempo_sin:.3f}s** (impacto directo contra tablero/parabrisas)
- **Con cinturón:** Tiempo calculado = **{tiempo_con:.3f}s** (cinturón extiende la desaceleración)

**🎯 Explicación física del cinturón:**
El cinturón de seguridad NO es solo una correa que te sostiene. Físicamente:
1. **Distribución de carga:** Reparte la fuerza sobre el torso (no solo el pecho)
2. **Extensibilidad:** El material del cinturón se estira ligeramente
3. **Sistema de frenado:** Mecanismo que permite extensión controlada durante el impacto
4. **Resultado:** Aumenta el tiempo de desaceleración de **{tiempo_sin:.3f}s** a **{tiempo_con:.3f}s**

**⚡ Principio físico clave:**
Según F = m × a, y a = Δv/Δt, al aumentar el tiempo (Δt) automáticamente se reduce la aceleración (a) y por tanto la fuerza (F).
"""
    else:
        return f"""
### ⚙️ **Modo Manual - Parámetros Definidos:**

**Tiempos utilizados:**
- **Sin cinturón:** **{tiempo_sin:.3f}s** (valor manual)
- **Con cinturón:** **{tiempo_con:.3f}s** (valor manual)

**📚 Interpretación educativa:**
En este modo, tú defines los tiempos para explorar el principio físico. En la realidad, el cinturón **causa** el aumento del tiempo por:
- Material extensible que absorbe energía
- Distribución de fuerzas sobre área mayor del cuerpo
- Sistemas de pretensores y limitadores de fuerza

**🎯 Principio demostrado:**
Al aumentar manualmente el tiempo de **{tiempo_sin:.3f}s** a **{tiempo_con:.3f}s**, observas cómo disminuye la fuerza según F = m × Δv/Δt.
"""

def calcular_factores_comparacion(datos):
    """
    Calcula los factores de comparación entre escenarios
    
    Args:
        datos (dict): Diccionario con todos los datos de la simulación
    
    Returns:
        dict: Diccionario con factores de comparación
    """
    p_sin = datos['parametros_sin']
    p_con = datos['parametros_con']
    
    return {
        'factor_reduccion_fuerza': abs(p_sin['fuerza']) / abs(p_con['fuerza']),
        'factor_reduccion_aceleracion': abs(p_sin['aceleracion']) / abs(p_con['aceleracion']),
        'factor_reduccion_tiempo': datos['tiempo_con_cinturon'] / datos['tiempo_sin_cinturon'],
        'reduccion_fuerza_pct': ((abs(p_sin['fuerza']) - abs(p_con['fuerza'])) / abs(p_sin['fuerza'])) * 100,
        'reduccion_aceleracion_pct': ((abs(p_sin['aceleracion']) - abs(p_con['aceleracion'])) / abs(p_sin['aceleracion'])) * 100,
        'reduccion_g_pct': ((abs(p_sin['g_force']) - abs(p_con['g_force'])) / abs(p_sin['g_force'])) * 100
    }

def determinar_nivel_riesgo(g_force):
    """
    Determina el nivel de riesgo basado en las fuerzas G
    
    Args:
        g_force (float): Fuerza G experimentada
    
    Returns:
        str: Nivel de riesgo con emoji
    """
    if abs(g_force) > 50:
        return '🔴 CRÍTICO'
    elif abs(g_force) > 20:
        return '🟡 ALTO'
    else:
        return '🟢 MODERADO'

def generar_seccion_resultados(datos):
    """
    Genera la sección de resultados de la simulación
    
    Args:
        datos (dict): Diccionario con todos los datos de la simulación
    
    Returns:
        str: Texto con los resultados formateados
    """
    p_sin = datos['parametros_sin']
    p_con = datos['parametros_con']
    t_sin = datos['tiempo_sin_cinturon']
    t_con = datos['tiempo_con_cinturon']
    
    return f"""
#### 🔴 **SIN Cinturón de Seguridad:**
- ⏱️ Tiempo de detención: **{t_sin:.3f} segundos**
- 💥 Fuerza de impacto: **{abs(p_sin['fuerza']):,.0f} Newtons**
- 📈 Aceleración: **{abs(p_sin['aceleracion']):.1f} m/s²**
- 🌍 **Fuerzas G:** **{abs(p_sin['g_force']):.1f} G**

#### 🔵 **CON Cinturón de Seguridad:**
- ⏱️ Tiempo de detención: **{t_con:.3f} segundos**
- 💥 Fuerza de impacto: **{abs(p_con['fuerza']):,.0f} Newtons**  
- 📈 Aceleración: **{abs(p_con['aceleracion']):.1f} m/s²**
- 🌍 **Fuerzas G:** **{abs(p_con['g_force']):.1f} G**
"""

def generar_seccion_analisis_resultados(datos, factores):
    """
    Genera la sección IV del análisis de resultados
    
    Args:
        datos (dict): Diccionario con todos los datos de la simulación
        factores (dict): Factores de comparación calculados
    
    Returns:
        str: Texto con el análisis de resultados
    """
    velocidad_kmh = datos['velocidad_kmh']
    masa_cuerpo = datos['masa_cuerpo']
    t_sin = datos['tiempo_sin_cinturon']
    t_con = datos['tiempo_con_cinturon']
    factor_reduccion_fuerza = factores['factor_reduccion_fuerza']
    factor_reduccion_aceleracion = factores['factor_reduccion_aceleracion']
    factor_reduccion_tiempo = factores['factor_reduccion_tiempo']
    reduccion_g_pct = factores['reduccion_g_pct']
    
    return f"""
#### 🎯 **IV. Análisis de Resultados - Principio Físico Fundamental:**

**📈 Interpretación de las Gráficas:**
- **Área bajo la curva:** Ambas tienen la misma área (mismo impulso: m × Δv)
- **Altura del pico:** Sin cinturón es **{factor_reduccion_fuerza:.1f}x más alta**
- **Duración:** Con cinturón dura **{factor_reduccion_tiempo:.1f}x más tiempo**

**🔬 Principio Físico Demostrado:**
```
F = m × a = m × (Δv/Δt)
```
- **Mismo cambio de velocidad (Δv):** De {velocidad_kmh} km/h a 0 km/h
- **Misma masa (m):** {masa_cuerpo} kg
- **Variable clave:** Tiempo de desaceleración (Δt)

**🎯 Resultado Observado:**
Al aumentar Δt de **{t_sin:.3f}s** a **{t_con:.3f}s**, automáticamente:
- La aceleración se reduce **{factor_reduccion_aceleracion:.1f}x**
- La fuerza se reduce **{factor_reduccion_fuerza:.1f}x**
- Las fuerzas G se reducen **{reduccion_g_pct:.1f}%**

**💡 Conclusión Física:**
El cinturón de seguridad salva vidas no por "sujetarte", sino por aumentar el tiempo de desaceleración, lo que reduce dramáticamente las fuerzas destructivas según las leyes fundamentales de la física.
"""

def generar_analisis_completo(datos):
    """
    Genera el análisis completo combinando todas las secciones
    
    Args:
        datos (dict): Diccionario con todos los datos de la simulación
    
    Returns:
        str: Texto completo del análisis
    """
    velocidad_kmh = datos['velocidad_kmh']
    velocidad_ms = datos['velocidad_ms']
    masa_cuerpo = datos['masa_cuerpo']
    modo_calculo = datos['modo_calculo']
    p_sin = datos['parametros_sin']
    p_con = datos['parametros_con']
    
    factores = calcular_factores_comparacion(datos)
    explicacion_modo = generar_explicacion_modo_calculo(datos)
    resultados = generar_seccion_resultados(datos)
    analisis_resultados = generar_seccion_analisis_resultados(datos, factores)
    
    return f"""
### 📊 Análisis de Simulación de Colisión

**Condiciones del impacto:**
- Velocidad inicial: **{velocidad_kmh} km/h** ({velocidad_ms:.1f} m/s)
- Masa del cuerpo: **{masa_cuerpo} kg**
- Modo de cálculo: **{modo_calculo.upper()}**

{explicacion_modo}

---

{resultados}

---

{analisis_resultados}

---

#### 🏆 **Resumen Cuantitativo:**
- **Extensión del tiempo:** **{factores['factor_reduccion_tiempo']:.1f}x mayor**
- **Reducción de fuerza:** **{factores['reduccion_fuerza_pct']:.1f}%**
- **Reducción de aceleración:** **{factores['reduccion_aceleracion_pct']:.1f}%**
- **Reducción de fuerzas G:** **{factores['reduccion_g_pct']:.1f}%**
- **Nivel de riesgo sin cinturón:** {determinar_nivel_riesgo(p_sin['g_force'])}
- **Nivel de riesgo con cinturón:** {determinar_nivel_riesgo(p_con['g_force'])}

> **⚠️ Referencia médica:** Fuerzas G superiores a 50G son típicamente letales para humanos.
"""