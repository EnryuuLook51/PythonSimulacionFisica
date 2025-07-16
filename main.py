# =============================================================================
# MAIN.PY - SIMULADOR DE IMPACTO VEHICULAR
# =============================================================================
# Archivo principal que coordina todos los módulos del simulador

import sys
import os
from calculos_fisica import simular_colision
from interfaz_gradio import crear_interface
from utils import imprimir_inicio

def main():
    """
    Función principal que inicializa y ejecuta el simulador
    """
    try:
        # Mostrar información de inicio
        imprimir_inicio()
        
        # Crear y lanzar la interfaz
        demo = crear_interface()
        
        # Configuración de lanzamiento
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            debug=False,
            show_error=True,
            quiet=False
        )
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        print("💡 Posibles soluciones:")
        print("   1. Verificar que el puerto 7860 esté disponible")
        print("   2. Reinstalar gradio: pip install --upgrade gradio")
        print("   3. Usar un puerto diferente modificando 'server_port'")
        print("   4. Verificar que todos los módulos estén en el mismo directorio")
        sys.exit(1)

if __name__ == "__main__":
    main()