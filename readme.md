# 🎙️ ProAcces TTS (v1.0)
**The Formant-Based Speech Synthesizer with the "Perfect R".**

ProAcces is a lightweight, open-source Text-To-Speech (TTS) engine written in Python. Unlike modern neural-network-based TTS, ProAcces uses **pure formant synthesis**, a classic technique from the 90s (reminiscent of the legendary *Eloquence* engine) that ensures extreme speed, low resource consumption, and high intelligibility.

---

## 🌍 Internationalization Note
> **Note:** This documentation is provided in English to reach the global developer community. However, the original developer is **Hispanic**. While English is preferred for international expansion, we fully welcome and encourage **Issues, Discussions, and Comments in Spanish**.

---

## ✨ Why ProAcces?
Most modern open-source synthesizers (like eSpeak) often struggle with Romance languages, specifically the "R" sound. ProAcces was born from the need for a truly natural-sounding Hispanic and European phonetic engine.

### 🎸 The ProAcces Signature: "The Triple R"
We have implemented three distinct mechanical-acoustic models for the letter "R", a feature rarely seen in open-source projects:

1.  **Alveolar Trill (Latin/Cyrillic):** The classic Spanish "RR" or Russian "р". It uses a 30Hz pulse-width modulation (PWM) to simulate the physical vibration of the tongue against the palate.
2.  **Uvular Fricative (Germanic/French):** The "raspy" R. A voiced-frictional hybrid that mimics the vibration of the uvula (exaggerated "J" sound).
3.  **Alveolar Approximant (English):** The "liquid" R. A clean, retroflex sound with a specific drop in the 3rd formant (F3) below 2000Hz.

---

## 🚀 Supported Alphabets & Languages
- **Latin Alphabet:** Full support for Spanish (Official) and Portuguese (Beta with nasal vowels `ã`, `õ`).
- **Cyrillic Alphabet:** Automatic detection for Russian and Bulgarian phonemes (mapping `р` to Alveolar Trill).
- **Germanic/English Rules:** Specific phonetic profiles for English and German "R" variants.

---

## 🛠️ Installation & Usage

### 1. Requirements
- Python 3.x
- `numpy`
- `scipy`
- `pyaudio`

### 2. Setup
Clone the repository and install dependencies:
```bash
git clone [https://github.com/YOUR_USER/ProAcces.git](https://github.com/YOUR_USER/ProAcces.git)
cd ProAcces
pip install -r requirements.txt
###3. Run the App
Launch the official terminal interface:
Bash
python ProAcces-app-voice.py
##🤝 Contributing
ProAcces is a community-driven project. We are looking for contributors to help with:
• 
New Language Rules: Create or improve phonetic rule mappings.
• 
Phonetic Refinement: Tuning F1, F2, and F3 frequencies for better clarity in different voices.
• 
Bug Reporting: Found a word that sounds robotic or "clipped"? Open an Issue.
• 
New Alphabets: Help us bring ProAcces to more scripts around the world.
Communication
• 
English: Preferred for code comments and international reach.
• 
Español: ¡Totalmente bienvenido! Si te sientes más cómodo reportando errores o discutiendo mejoras en español, por favor hazlo. El corazón del proyecto es hispano y valoramos enormemente el feedback en nuestra lengua materna.
 
##📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
Developed with ❤️ by the ProAcces Community.
## 🤝 Acknowledgments & Community Credits

ProAcces is built on the shoulders of giants. We believe in the power of open-source collaboration and standardization to improve accessibility worldwide.

Special thanks to the **NV Access** team and the **NVDA (NonVisual Desktop Access)** project [@nvaccess](https://github.com/nvaccess/nvda). 

### Why we support the .dic format:
To ensure a seamless experience for users and developers in the accessibility community, **ProAcces** has adopted a dictionary system compatible with the **NVDA `.dic` format**. 

* **Legacy Support:** Users can import their existing custom dictionaries from NVDA directly into ProAcces.
* **Familiarity:** We use the same tab-separated structure (`Pattern [tab] Replacement [tab] Active [tab] Case`) to reduce the learning curve.
* **Inspiration:** The commitment of NV Access to providing free, high-quality access to technology has been a primary inspiration for the development of this engine.

We encourage all NVDA power users to test their custom dictionaries with our engine and provide feedback!