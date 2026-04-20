# 🎙️ ProAcces TTS v2.0

**ProAcces TTS** es un motor de síntesis de voz híbrido de alto rendimiento, diseñado para ser ligero, nítido y extremadamente personalizable. Combina la velocidad de la síntesis por formantes con la inteligencia prosódica de los modelos paramétricos (HTS).

## ✨ Características Principales

*   **🚀 Motor de Síntesis Híbrido:** Implementa una arquitectura Klatt con filtros en cascada (vocales) y en paralelo (consonantes/fricativas).
*   **🧠 Inteligencia Prosódica (Cerebro/Cuerpo):**
    *   **Modo HTS Simulated:** Ritmo humano calculado mediante heurísticas de duración no lineal.
    *   **Modo HTS RHVoice:** Integración con la DLL de RHVoice para una entonación natural basada en modelos estadísticos.
*   **🎵 7 Estilos de Tono:** Classic, Fujisaki (estilo Eloquence), eSpeak, Klatt Hat-Pattern, Impulse, HTS Simulated y HTS Real.
*   **🌍 Multi-Idioma Real:**
    *   **Español:** Manejo avanzado de vibrantes (R/RR) y fonetización completa.
    *   **Inglés:** Lógica de vocales largas y "E" silenciosa.
    *   **Ruso:** Soporte nativo para escritura en Cirílico.
    *   **Otros:** Portugués (nasales), Alemán y Francés (R gutural).
*   **📖 Compatibilidad NVDA:** Carga directa de diccionarios `.dic` de NVDA.
*   **💾 Exportación WAV:** Opción para guardar la síntesis directamente en archivos de audio de alta fidelidad.

## 🛠️ Arquitectura Técnica

ProAcces separa el **Cerebro** (Prosodia) del **Cuerpo** (Audio):

1.  **Prosodia:** Los modelos (Fujisaki, Klatt, RHVoice) generan un contorno de F0 y duraciones.
2.  **Fuente Glotal:** Utiliza el modelo **LF (Liljencrants-Fant)** para una excitación vocal orgánica.
3.  **Filtrado:** Una red de filtros IIR modela las resonancias del tracto vocal en tiempo real.

## 🚀 Instalación

### Requisitos
*   Python 3.8+
*   Librerías: `numpy`, `scipy`, `pyaudio`

```bash
pip install -r requirements.txt
```

### Uso
Ejecuta la aplicación principal y sigue el menú interactivo:

```bash
python ProAcces-app-voice.py
```

## 🗺️ Roadmap (Futuro)

- [ ] **Multi-Motor Híbrido:** Selector dinámico entre síntesis de formantes y síntesis paramétrica estadística completa.
- [ ] **Variantes de Voz:** Soporte para cargar modelos `.htsvoice` externos (Elena, Leticia, etc.).
- [ ] **Interfaz Gráfica:** Implementación de un panel de control avanzado usando wxPython.

## 🤝 Créditos y Agradecimientos

Este proyecto no habría sido posible sin el increíble trabajo de la comunidad de código abierto y, en particular, de los siguientes repositorios:

*   **[TGSpeechBox](https://github.com/tgeczy/TGSpeechBox):** De quien hemos aprendido e implementado las avanzadas técnicas de síntesis por formantes (Klatt-style), permitiendo que ProAcces tenga una calidad de audio profesional.
*   **[RHVoice](https://github.com/rHVoice/RHVoice):** ProAcces incluye una copia de este motor para alimentar su estilo de tono **HTS RHV**, proporcionando una prosodia humana inigualable.

## 📄 Licencia
Este proyecto está bajo la licencia MIT. La integración con RHVoice está sujeta a los términos de licencia de RHVoice (LGPL).

---
*Desarrollado para la accesibilidad universal.*
