import os
import sys
from proacces import ProAcces

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("   PROACCES TTS v1.5 - NVDA DICTIONARY COMPATIBLE")
    print("="*50)
    
    engine = ProAcces()
    
    # Cargar Diccionario compatible con NVDA
    if os.path.exists("default.dic"):
        engine.cargar_diccionario_nvda("default.dic")
        print("[✓] Diccionario NVDA cargado.")
    
    lang = input("Seleccione idioma (es/pt/en/ru/de) [es]: ") or "es"
    if engine.cargar_idioma(lang):
        print(f"[✓] Reglas de '{lang}' cargadas.")
    
    print("\nEscriba su texto (o 'salir'):")
    try:
        while True:
            t = input(f"({lang}) > ")
            if t.lower() in ['salir', 'exit']: break
            if t.strip(): engine.hablar(t, lang=lang)
    finally:
        engine.detener()

if __name__ == "__main__":
    main()