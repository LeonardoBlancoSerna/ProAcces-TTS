import os
import sys
from proacces import ProAcces

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("   PROACCES TTS v2.0 - MULTI-PITCH & WAV EXPORT")
    print("="*50)
    
    engine = ProAcces()
    
    # Cargar Diccionario compatible con NVDA
    if os.path.exists("default.dic"):
        engine.cargar_diccionario_nvda("default.dic")
        print("[✓] Diccionario NVDA cargado.")
    
    # Selección de Idioma
    lang = input("Seleccione idioma (es/pt/en/ru/de/fr) [es]: ") or "es"
    if engine.cargar_idioma(lang):
        print(f"[✓] Reglas de '{lang}' cargadas.")

    # Selección de Estilo de Tono
    print("\nEstilos de Tono disponibles:")
    print("1. Classic (Lineal)")
    print("2. Fujisaki (Eloquence style)")
    print("3. eSpeak (Stepped style)")
    print("4. Klatt (Hat pattern)")
    print("5. Impulse (Rhythmic)")
    print("6. HTS Simulated (Human-like rhythm)")
    print("7. HTS RHVoice (Real HTS - Requires DLL)")
    style_idx = input("Seleccione estilo [1]: ") or "1"
    styles = {
        "1": "classic", "2": "fujisaki", "3": "espeak", 
        "4": "klatt", "5": "impulse", "6": "hts_simulated", "7": "hts_rhv"
    }
    engine.pitch_style = styles.get(style_idx, "classic")
    
    if engine.pitch_style == "hts_rhv" and not engine.rhv_dll:
        print("[!] Advertencia: RHVoice.dll no encontrada. Usando HTS Simulated en su lugar.")
        engine.pitch_style = "hts_simulated"
    
    print(f"[✓] Estilo '{engine.pitch_style}' seleccionado.")

    # Selección de Modo de Salida
    print("\nModo de salida:")
    print("1. Hablar en tiempo real")
    print("2. Guardar a archivo WAV")
    mode = input("Seleccione modo [1]: ") or "1"

    print(f"\n--- Iniciando síntesis en modo {'AUDIO' if mode == '1' else 'ARCHIVO'} ---")
    print("Escriba su texto (o 'salir'):")
    
    try:
        while True:
            t = input(f"({lang} - {engine.pitch_style}) > ")
            if t.lower() in ['salir', 'exit']: break
            if not t.strip(): continue

            if mode == "1":
                engine.hablar(t, lang=lang)
            else:
                filename = f"output_{len(os.listdir('.'))}.wav"
                engine.guardar_wav(t, filename, lang=lang)
                print(f"[✓] Guardado en: {filename}")
    finally:
        engine.detener()

if __name__ == "__main__":
    main()
