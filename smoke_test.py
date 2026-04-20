import sys
import os

# Asegurar que el script encuentre el motor
sys.path.append(os.getcwd())
from proacces import ProAcces

def test_engine():
    print("Iniciando prueba de ProAcces TTS v2.1...")
    try:
        # 1. Instanciación
        engine = ProAcces()
        print("[✓] Motor instanciado correctamente.")

        # 2. Prueba de Idioma
        if engine.cargar_idioma("es"):
            print("[✓] Idioma 'es' cargado.")
        else:
            print("[X] Error al cargar idioma 'es'.")

        # 3. Prueba de Estilos de Tono
        estilos = ["classic", "fujisaki", "espeak", "klatt", "impulse", "hts_simulated"]
        for estilo in estilos:
            engine.pitch_style = estilo
            # Intentamos sintetizar una palabra simple (sin reproducir audio para evitar colgar el CI)
            audio = engine.sintetizar_texto("Hola", lang="es")
            if len(audio) > 0:
                print(f"[✓] Estilo '{estilo}' sintetizado con éxito ({len(audio)} muestras).")
            else:
                print(f"[X] Estilo '{estilo}' generó audio vacío.")

        # 4. Prueba de exportación WAV
        filename = "test_output.wav"
        engine.guardar_wav("Prueba de sintetizador exitosa", filename, lang="es")
        if os.path.exists(filename) and os.path.getsize(filename) > 44:
            print(f"[✓] Archivo WAV generado correctamente: {filename}")
            os.remove(filename)
        else:
            print("[X] Fallo al generar archivo WAV.")

        print("\n--- TEST FINALIZADO CON ÉXITO ---")
        engine.detener()
        return True

    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if not test_engine():
        sys.exit(1)
