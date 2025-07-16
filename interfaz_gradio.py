# interfaz_gradio.py
# =============================================================================
# INTERFAZ_GRADIO.PY - MÓDULO DE INTERFAZ DE USUARIO
# =============================================================================
# Este módulo contiene la lógica para crear y lanzar la interfaz de usuario con Gradio

import gradio as gr
from calculos_fisica import simular_colision, generar_animaciones

def crear_interface():
    """
    Crea y configura la interfaz de usuario con Gradio
    
    Returns:
        gr.Blocks: Interfaz de Gradio configurada
    """
    with gr.Blocks(
        theme=gr.themes.Soft(), 
        title="Simulador de Colisión Vehicular",
        css="""
        .gradio-container {
            max-width: 1400px;
            margin: auto;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🚗 Simulador de Impacto Vehicular - Análisis Físico Completo
        
        Esta herramienta educativa demuestra **cómo** y **por qué** el cinturón de seguridad 
        salva vidas mediante principios fundamentales de la física.
        
        **📚 Conceptos aplicados:** F = m × a, Impulso, Cinemática, Fuerzas G
        
        **🆕 Nuevo:** Modo realista que calcula los tiempos según física real
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Parámetros de Simulación")
                
                masa_input = gr.Slider(
                    minimum=20, maximum=150, value=70, step=1,
                    label="👤 Masa del Cuerpo (kg)",
                    info="Peso típico de una persona adulta"
                )
                
                velocidad_input = gr.Slider(
                    minimum=10, maximum=200, value=50, step=5,
                    label="🏎️ Velocidad Inicial (km/h)",
                    info="Velocidad del vehículo antes del impacto"
                )
                
                modo_tiempo = gr.Radio(
                    choices=["Cálculo Realista", "Configuración Manual"],
                    value="Cálculo Realista",
                    label="🔬 Modo de Cálculo de Tiempos",
                    info="Realista: basado en física real. Manual: tú decides los tiempos"
                )
                
                with gr.Group(visible=False) as controles_manuales:
                    tiempo_con_cinturon_input = gr.Slider(
                        minimum=0.2, maximum=2.0, value=0.5, step=0.1,
                        label="⏱️ Tiempo de Frenado CON Cinturón (s)",
                        info="El cinturón extiende el tiempo de desaceleración"
                    )
                    
                    tiempo_sin_cinturon_input = gr.Slider(
                        minimum=0.01, maximum=0.5, value=0.1, step=0.01,
                        label="⏱️ Tiempo de Frenado SIN Cinturón (s)",
                        info="Impacto directo, tiempo muy corto"
                    )
                
                btn_simular = gr.Button("🚀 Ejecutar Simulación", variant="primary", size="lg")
                btn_animaciones = gr.Button("🎥 Generar Animaciones", variant="secondary", size="lg", visible=False)
                
                gr.Markdown("""
                ### 💡 Modos de Uso:
                
                **🔬 Modo Realista:**
                - Calcula tiempos basados en física real
                - Demuestra cómo el cinturón **causa** el aumento de tiempo
                - Más educativo para entender el principio físico
                
                **⚙️ Modo Manual:**
                - Tú defines los tiempos manualmente
                - Útil para explorar "¿qué pasaría si...?"
                - Permite ver el efecto puro de cambiar el tiempo
                """)

            with gr.Column(scale=2):
                gr.Markdown("### 📊 Resultados de la Simulación")
                plot_output = gr.Plot(label="Análisis Físico Completo")
                analisis_output = gr.Markdown(label="Análisis Detallado")
                datos_simulacion_state = gr.State()
                with gr.Row():
                    anim_sin_output = gr.Video(label="Animación: Sin Cinturón")
                    anim_con_output = gr.Video(label="Animación: Con Cinturón")

        # Función para mostrar/ocultar controles manuales
        def actualizar_controles(modo):
            return gr.update(visible=(modo == "Configuración Manual"))

        # Función para ejecutar la simulación
        def ejecutar_simulacion(masa, velocidad, modo, tiempo_con_manual, tiempo_sin_manual):
            if any(x is None for x in [masa, velocidad, modo]):
                return None, "❌ Error: Todos los parámetros deben tener valores válidos", None, gr.update(visible=True)
            if modo == "Configuración Manual" and any(x is None for x in [tiempo_con_manual, tiempo_sin_manual]):
                return None, "❌ Error: Los tiempos manuales deben tener valores válidos", None, gr.update(visible=True)
            usar_manual = (modo == "Configuración Manual")
            fig, analisis, datos = simular_colision(masa, velocidad, usar_manual, tiempo_con_manual, tiempo_sin_manual)
            return fig, analisis, datos, gr.update(visible=True)

        # Función para generar animaciones
        def ejecutar_animaciones(datos_simulacion):
            if datos_simulacion is None:
                return None, "❌ Error: No hay datos de simulación disponibles", None
            anim_sin, anim_con = generar_animaciones(datos_simulacion)
            return anim_sin, anim_con

        modo_tiempo.change(
            fn=actualizar_controles,
            inputs=[modo_tiempo],
            outputs=[controles_manuales]
        )

        btn_simular.click(
            fn=ejecutar_simulacion,
            inputs=[masa_input, velocidad_input, modo_tiempo, tiempo_con_cinturon_input, tiempo_sin_cinturon_input],
            outputs=[plot_output, analisis_output, datos_simulacion_state, btn_animaciones]
        )

        btn_animaciones.click(
            fn=ejecutar_animaciones,
            inputs=[datos_simulacion_state],
            outputs=[anim_sin_output, anim_con_output]
        )

        gr.Markdown("""
        ---
        ### 🔬 Explicación Científica Fundamental:
        
        **¿Por qué funciona el cinturón de seguridad?**
        
        La respuesta está en la ecuación fundamental: **F = m × a = m × (Δv/Δt)**
        
        **Componentes de la ecuación:**
        - **m:** Masa del cuerpo (constante)
        - **Δv:** Cambio de velocidad (constante - siempre de velocidad inicial a 0)
        - **Δt:** Tiempo de desaceleración (VARIABLE CLAVE)
        - **F:** Fuerza resultante (lo que causa lesiones)
        
        **El cinturón salva vidas porque:**
        1. **Aumenta Δt:** Extiende el tiempo de desaceleración
        2. **Reduce F:** Al aumentar Δt, automáticamente se reduce F
        3. **Distribuye fuerza:** Sobre área mayor del cuerpo
        4. **Absorbe energía:** Material extensible absorbe parte del impacto
        
        **🎯 Principio clave:** Misma energía + más tiempo = menos fuerza destructiva
        
        ---
        
        ### 📈 Interpretación de los Gráficos:
        
        **Gráfico de Fuerza vs Tiempo:**
        - Área bajo ambas curvas es igual (mismo impulso)
        - Pico más bajo con cinturón = menos daño
        - Duración más larga con cinturón = desaceleración gradual
        
        **Gráfico de Aceleración vs Tiempo:**
        - Muestra la tasa de cambio de velocidad
        - Pico más bajo = menos trauma al cuerpo
        - Relación directa con fuerzas G experimentadas
        
        **Comparación de Barras:**
        - Visualización directa de la reducción de fuerzas
        - Fuerzas G: referencia médica para supervivencia
        - Comparación cuantitativa de todos los parámetros
        """)

    return demo