import numpy as np
import pyaudio
import re
import os
from scipy import signal

class ProAcces:
    def __init__(self, sr=44100, f_base=115.0, speed=0.08):
        self.sr = sr
        self.f_base = f_base
        self.speed = speed
        self.rules = {} 
        self.user_dict = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.sr, output=True)
        
        # TABLA MAESTRA DE FORMANTES (Alfabeto Universal ProAcces)
        self.formantes = {
            'a': [730, 1090, 2440], 'e': [440, 1800, 2550], 'i': [270, 2200, 2800],
            'o': [440, 850, 2250],  'u': [300, 700, 2200],
            'an': [550, 1050, 2400], 'en': [400, 1500, 2500], 'in': [250, 2000, 2700],
            'on': [400, 800, 2100],  'un': [280, 700, 2100],
            'p': [700, 1200, 2500], 't': [3000, 4000, 6000], 'k': [1500, 2500, 4000],
            'b': [200, 1000, 2000], 'd': [250, 1700, 2500], 'g': [300, 1500, 2200],
            's': [4500, 6500, 8500], 'S': [2500, 3500, 5000], 'C': [2000, 3000, 4500],
            'l': [380, 1500, 2500], 'N': [280, 1900, 3100], 'm': [280, 900, 2200],
            'n': [250, 1500, 2500], 'x': [3500, 5000, 7000], 'z': [4000, 5500, 7500],
            'R_LAT': [450, 1100, 2900], 'R_GER': [420, 1000, 2200], 'R_ANG': [350, 1100, 1550]
        }

    def cargar_diccionario_nvda(self, ruta="default.dic"):
        """Carga diccionarios compatibles con formato NVDA (.dic)"""
        if not os.path.exists(ruta): return
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                campos = linea.strip().split('\t')
                if len(campos) >= 2 and (len(campos) < 3 or campos[2] == "1"):
                    self.user_dict.append({
                        'p': campos[0], 
                        'r': campos[1], 
                        'c': campos[3] == "1" if len(campos) > 3 else False
                    })

    def cargar_idioma(self, lang_code):
        path = f"lang/{lang_code}.syn"
        if not os.path.exists(path): return False
        self.rules[lang_code] = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if '->' in line and not line.startswith('#'):
                    orig, dest = line.strip().split('->')
                    self.rules[lang_code].append((orig.strip(), dest.strip()))
        return True

    def _procesar_texto(self, texto, lang):
        t = texto.lower()
        # 1. Diccionario de Usuario (NVDA Style)
        for entry in self.user_dict:
            flags = 0 if entry['c'] else re.IGNORECASE
            t = re.sub(rf'\b{re.escape(entry["p"])}\b', entry['r'], t, flags=flags)
        
        # 2. Reglas de Idioma (.syn)
        if lang in self.rules:
            for orig, dest in self.rules[lang]:
                t = t.replace(orig, dest)
        
        # 3. Lógica Global de la R
        palabras = t.split()
        res = []
        for p in palabras:
            if p.startswith('r'): p = 'R_LAT' + p[1:]
            if p.endswith('r'): p = p[:-1] + 'R_LAT'
            res.append(p.replace('rr', 'R_LAT'))
        return " ".join(res)

    def _tokenizar(self, texto_f):
        patron = r'R_LAT|R_GER|R_ANG|an|en|in|on|un|[a-zãõNSCxkz]'
        return re.findall(patron, texto_f)

    def _sintetizar_fonema(self, fonema, f0, es_final=False, es_pregunta=False):
        dur = self.speed
        if fonema in 'ptk': dur = 0.04
        elif 'R_' in fonema or fonema in 'CS': dur *= 1.5
        
        num_s = int(self.sr * dur)
        t = np.linspace(0, dur, num_s, endpoint=False)
        
        # PROSODIA (Modulación de Frecuencia Fundamental)
        f0_mod = f0
        if es_final:
            f0_mod = f0 * (1.2 if es_pregunta else 0.8)
        
        # GENERACIÓN DE FUENTE
        if fonema == 'R_LAT':
            f0_vibrato = f0_mod + 5 * np.sin(2 * np.pi * 35 * t)
            fuente = signal.sawtooth(2 * np.pi * np.cumsum(f0_vibrato) / self.sr)
            fuente *= (signal.square(2 * np.pi * 28 * t, duty=0.45) + 1) / 2
        elif fonema == 'R_GER':
            fuente = (signal.sawtooth(2 * np.pi * f0_mod * t) * 0.5) + (np.random.normal(0, 0.4, num_s) * 0.5)
        elif fonema in 'skCxsz':
            fuente = np.random.normal(0, 0.3, num_s)
        elif fonema in 'ptk':
            fuente = np.zeros(num_s)
            fuente[int(num_s*0.6):] = np.random.normal(0, 0.5, num_s - int(num_s*0.6))
        else:
            fuente = signal.sawtooth(2 * np.pi * f0_mod * t)

        # FILTROS Y NASALIZACIÓN
        f_target = self.formantes.get(fonema, [500, 1500, 2500])
        audio = np.zeros(num_s)
        es_nasal = fonema in ['an', 'en', 'in', 'on', 'un']
        
        for i, freq in enumerate(f_target):
            q = (100 if es_nasal else 130) if i == 0 else 60
            b, a = signal.iirpeak(freq, freq/q, fs=self.sr)
            canal = signal.lfilter(b, a, fuente)
            if es_nasal and i == 0: # Resonancia nasal extra
                bn, an = signal.iirpeak(250, 250/50, fs=self.sr)
                canal += signal.lfilter(bn, an, fuente) * 0.4
            audio += canal

        # Envolvente
        env = np.ones(num_s)
        at = int(num_s * 0.1)
        env[:at] = np.linspace(0, 1, at); env[-at:] = np.linspace(1, 0, at)
        audio *= env
        if np.max(np.abs(audio)) > 0: audio = (audio / np.max(np.abs(audio))) * 0.7
        return (audio * 32767).astype(np.int16)

    def hablar(self, texto, lang='es'):
        es_pregunta = '?' in texto
        texto_limpio = self._procesar_texto(texto, lang)
        tokens = self._tokenizar(texto_limpio)
        
        for i, f in enumerate(tokens):
            es_final = (i >= len(tokens) - 2) # Los últimos fonemas de la frase
            chunk = self._sintetizar_fonema(f, self.f_base, es_final, es_pregunta)
            self.stream.write(chunk.tobytes())
        # Pausa final
        self.stream.write(np.zeros(int(self.sr * 0.1), dtype=np.int16).tobytes())

    def detener(self):
        self.stream.stop_stream(); self.stream.close(); self.p.terminate()