import numpy as np
import pyaudio
import re
import os
import wave
from scipy import signal

class ProAcces:
    def __init__(self, sr=44100, f_base=115.0, speed=0.08):
        self.sr = sr
        self.f_base = f_base
        self.speed = speed
        self.rules = {} 
        self.user_dict = []
        self.pitch_style = "classic" 
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.sr, output=True)
        self.rhv_dll = None

        # Intentar preparar el puente con RHVoice (DLL en Windows, .so en Android/Linux)
        try:
            import ctypes
            lib_name = "RHVoice.dll" if os.name == 'nt' else "libRHVoice.so"
            lib_paths = [lib_name, os.path.join("libs", lib_name), os.path.join(os.path.dirname(__file__), lib_name)]
            for path in lib_paths:
                if os.path.exists(path):
                    self.rhv_dll = ctypes.cdll.LoadLibrary(path)
                    break
        except: pass

        # TABLA AVANZADA DE PARÁMETROS (Basada en Klatt / SpeechBox)
        self.params = {
            'a': {'cf': [750, 1180, 2400, 3500, 4500], 'cb': [140, 90, 150, 250, 200], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'e': {'cf': [480, 1900, 2500, 3500, 4500], 'cb': [66, 67, 150, 250, 200], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'i': {'cf': [240, 2250, 3000, 4000, 5000], 'cb': [50, 100, 140, 250, 200], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'o': {'cf': [500, 900, 2300, 3300, 4300], 'cb': [90, 100, 200, 250, 200], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'u': {'cf': [280, 750, 2200, 3200, 4200], 'cb': [70, 110, 140, 250, 200], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'l': {'cf': [310, 1050, 2880, 3300, 4500], 'cb': [55, 75, 210, 300, 350], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'g': {'cf': [200, 1800, 2400, 3300, 4500], 'cb': [66, 130, 200, 450, 800], 'v_amp': 0.9, 'asp': 0.1, 'fric': 0.5, 'pa': [0.05, 0.55, 0.65, 0.2, 0.1]},
            'b': {'cf': [200, 1100, 2150, 3300, 4500], 'cb': [66, 90, 140, 600, 1000], 'v_amp': 0.9, 'asp': 0, 'fric': 1.0, 'pa': [0.2, 0.25, 0.14, 0.06, 0.03]},
            'C': {'cf': [300, 2200, 2850, 3300, 4500], 'cb': [275, 120, 220, 450, 800], 'v_amp': 0, 'asp': 0.1, 'fric': 0.9, 'pa': [0.1, 0.8, 0.75, 0.3, 0.1]},
            'f': {'cf': [340, 1100, 2080, 3300, 4500], 'cb': [220, 100, 150, 600, 1200], 'v_amp': 0, 'asp': 0, 'fric': 1.0, 'pa': [0, 0, 0, 0, 0], 'bypass': 0.9},
            'p': {'cf': [400, 850, 2100, 3300, 4500], 'cb': [300, 150, 180, 600, 1000], 'v_amp': 0, 'asp': 0.3, 'fric': 0.5, 'pa': [0.3, 0.4, 0.3, 0.18, 0.1]},
            'j': {'cf': [290, 2000, 2920, 3300, 4500], 'cb': [65, 200, 400, 280, 300], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            't': {'cf': [380, 1700, 2650, 3300, 4500], 'cb': [300, 95, 175, 350, 500], 'v_amp': 0, 'asp': 0.4, 'fric': 0.8, 'pa': [0.08, 0.15, 0.3, 0.48, 0.48]},
            'x': {'cf': [250, 1400, 2600, 3300, 4500], 'cb': [160, 180, 250, 500, 1000], 'v_amp': 0.1, 'asp': 0.45, 'fric': 0.8, 'pa': [0.05, 1.0, 0.4, 0.4, 0.1]},
            'R_GER': {'cf': [250, 1400, 2600, 3300, 4500], 'cb': [160, 180, 250, 500, 1000], 'v_amp': 0.3, 'asp': 0.5, 'fric': 0.7, 'pa': [0.1, 0.8, 0.5, 0.3, 0.1]},
            'R_ANG': {'cf': [310, 1200, 1620, 3300, 4500], 'cb': [77, 80, 155, 300, 350], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            's': {'cf': [320, 1390, 2530, 3300, 4500], 'cb': [220, 60, 150, 350, 500], 'v_amp': 0, 'asp': 0, 'fric': 0.9, 'pa': [0, 0, 0, 0, 0.8]},
            'S': {'cf': [2500, 3500, 5000, 6500, 8000], 'cb': [200, 200, 200, 200, 200], 'v_amp': 0, 'asp': 0.2, 'fric': 0.8},
            'R_LAT': {'cf': [450, 1100, 2900, 3900, 4900], 'cb': [80, 90, 130, 320, 400], 'v_amp': 0.8, 'asp': 0, 'fric': 0.1},
            'r': {'cf': [200, 1600, 2200, 3300, 4500], 'cb': [66, 75, 127, 320, 400], 'v_amp': 0.9, 'asp': 0, 'fric': 0.08},
            'n': {'cf': [280, 1550, 2740, 3300, 4500], 'cb': [90, 260, 225, 300, 350], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'm': {'cf': [280, 1100, 2500, 3300, 4500], 'cb': [50, 200, 120, 300, 350], 'v_amp': 0.9, 'asp': 0, 'fric': 0},
            'an': {'cf': [550, 1050, 2400, 3500, 4500], 'cb': [120, 80, 150, 250, 200], 'v_amp': 0.9},
            'en': {'cf': [400, 1500, 2500, 3500, 4500], 'cb': [100, 100, 150, 250, 200], 'v_amp': 0.9},
            'in': {'cf': [250, 2000, 2700, 3700, 4700], 'cb': [80, 100, 150, 250, 200], 'v_amp': 0.9},
            'on': {'cf': [400, 800, 2100, 3100, 4100], 'cb': [100, 100, 150, 250, 200], 'v_amp': 0.9},
            'un': {'cf': [280, 700, 2100, 3100, 4100], 'cb': [80, 100, 150, 250, 200], 'v_amp': 0.9}
        }

    def cargar_diccionario_nvda(self, ruta="default.dic"):
        if not os.path.exists(ruta): return
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                campos = linea.strip().split('\t')
                if len(campos) >= 2 and (len(campos) < 3 or campos[2] == "1"):
                    self.user_dict.append({'p': campos[0], 'r': campos[1], 'c': campos[3] == "1" if len(campos) > 3 else False})

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
        if lang == 'es':
            t = t.replace('que', 'ke').replace('qui', 'ki').replace('ce', 'se').replace('ci', 'si')
            t = t.replace('z', 's').replace('h', '').replace('v', 'b').replace('ll', 'y')
            t = t.replace('ñ', 'ni').replace('j', 'x').replace('ge', 'xe').replace('gi', 'xi')
            t = t.replace('x', 'ks').replace('ü', 'u').replace('güe', 'gwe').replace('güi', 'gwi')
        elif lang == 'en':
            t = re.sub(r'([aeiou])([b-df-hj-np-tv-z])e\b', r'\1\1\2', t) 
            t = t.replace('th', 'z').replace('sh', 'S').replace('ch', 'C').replace('ph', 'f')
            t = t.replace('igh', 'ai').replace('ight', 'ait').replace('tion', 'SOn')
            t = t.replace('ee', 'i').replace('oo', 'u').replace('ea', 'i').replace('ay', 'ei').replace('ai', 'ei')
            t = t.replace('ck', 'k').replace('wh', 'w').replace('wr', 'r').replace('ow', 'au').replace('ou', 'au')
        elif lang == 'ru':
            cirilico = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'ye','ё':'yo','ж':'z','з':'s','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'x','ц':'ts','ч':'C','ш':'S','щ':'S','ъ':'','ы':'i','ь':'i','э':'e','ю':'yu','я':'ya'}
            for char, fon in cirilico.items(): t = t.replace(char, fon)
        elif lang == 'de':
            t = t.replace('ei', 'ai').replace('ie', 'i').replace('sch', 'S').replace('ch', 'x').replace('v', 'f').replace('w', 'b').replace('z', 'ts')
        elif lang == 'fr':
            t = t.replace('ou', 'u').replace('oi', 'wa').replace('eau', 'o').replace('au', 'o').replace('ai', 'e').replace('ei', 'e').replace('qu', 'k').replace('gn', 'ni').replace('ch', 'S')
        elif lang == 'pt':
            t = t.replace('ão', 'on').replace('ã', 'an').replace('õ', 'on').replace('nh', 'ni').replace('lh', 'y').replace('ch', 'S')
        for entry in self.user_dict:
            flags = 0 if entry['c'] else re.IGNORECASE
            t = re.sub(rf'\b{re.escape(entry["p"])}\b', entry['r'], t, flags=flags)
        if lang in self.rules:
            for orig, dest in self.rules[lang]: t = t.replace(orig, dest)
        palabras = t.split(); res = []
        for p in palabras:
            if p.startswith('r'): p = 'R_LAT' + p[1:]
            if p.endswith('r'): p = p[:-1] + 'R_LAT'
            res.append(p.replace('rr', 'R_LAT'))
        return " ".join(res)

    def _tokenizar(self, texto_f):
        patron = r'R_LAT|R_GER|R_ANG|an|en|in|on|un|[a-zãõNSCxkzBCFGPLJPT]'
        return re.findall(patron, texto_f)

    def _generar_fuente_lf(self, f0_contour, num_samples, jitter_amt=0.005):
        tp_rel = 0.413; te_rel = 0.552; ta_rel = 0.04
        jitter = 1.0 + jitter_amt * np.random.normal(0, 1, num_samples)
        f0_inst = f0_contour * jitter
        fase = np.cumsum(f0_inst) / self.sr
        phi = fase % 1.0
        wg = np.pi / tp_rel; alpha = 0.002
        fuente = np.zeros(num_samples)
        mask_ap = phi < te_rel
        t_ap = phi[mask_ap]
        fuente[mask_ap] = np.exp(alpha * t_ap) * np.sin(wg * t_ap)
        mask_ret = ~mask_ap
        t_ret = phi[mask_ret] - te_rel
        epsilon = 1.0 / ta_rel
        amp_te = np.exp(alpha * te_rel) * np.sin(wg * te_rel)
        exp_max = 1.0 - np.exp(-epsilon * (1.0 - te_rel))
        fuente[mask_ret] = amp_te * (np.exp(-epsilon * t_ret) - np.exp(-epsilon * (1.0 - te_rel))) / exp_max
        return fuente + np.random.normal(0, 0.02, num_samples)

    def _aplicar_high_shelf(self, audio, gain_db=4.0, fc=2500.0):
        A = 10**(gain_db/40); w0 = 2*np.pi*fc/self.sr; alpha = np.sin(w0)/2*np.sqrt((A+1/A)*(1/0.7-1)+2)
        cos_w0 = np.cos(w0); sqrt_A_alpha = 2*np.sqrt(A)*alpha
        return signal.lfilter([A*((A+1)+(A-1)*cos_w0+sqrt_A_alpha), -2*A*((A-1)+(A+1)*cos_w0), A*((A+1)+(A-1)*cos_w0-sqrt_A_alpha)], [(A+1)-(A-1)*cos_w0+sqrt_A_alpha, 2*((A-1)-(A+1)*cos_w0), (A+1)-(A-1)*cos_w0-sqrt_A_alpha], audio)

    def _calcular_contorno_f0(self, num_tokens, total_samples, es_pregunta):
        t_ms = np.linspace(0, total_samples/self.sr, total_samples)
        f0 = np.full(total_samples, self.f_base)
        if self.pitch_style == "fujisaki":
            f0 = self.f_base * np.exp(-0.0003 * t_ms * 1000)
            acentos = np.zeros_like(t_ms)
            acentos[int(len(t_ms)*0.1):int(len(t_ms)*0.2)] = 30
            acentos[int(len(t_ms)*0.7):int(len(t_ms)*0.8)] = 20
            f0 += acentos
            if es_pregunta: f0[-int(len(f0)*0.1):] *= 1.5
        elif self.pitch_style == "hts_simulated":
            f0 = self.f_base * np.exp(-0.0002 * t_ms * 1000)
            f0 *= (1.0 + 0.01 * np.sin(2 * np.pi * 5 * t_ms))
            if es_pregunta: f0[-int(len(f0)*0.15):] = np.linspace(f0[-int(len(f0)*0.15)], self.f_base*1.6, int(len(f0)*0.15))
        elif self.pitch_style == "espeak":
            steps = 5; chunk = total_samples // steps
            for i in range(steps): f0[i*chunk:(i+1)*chunk] = self.f_base * (1.1 - (i*0.05))
            if es_pregunta: f0[-chunk:] *= 1.3
        elif self.pitch_style == "klatt":
            split = total_samples // 4
            f0[:split] = np.linspace(self.f_base, self.f_base+40, split)
            f0[split:3*split] = self.f_base+40
            f0[3*split:] = np.linspace(self.f_base+40, self.f_base-10, total_samples - 3*split)
            if es_pregunta: f0[-split:] = np.linspace(self.f_base-10, self.f_base+60, split)
        elif self.pitch_style == "impulse":
            f0 = self.f_base - (t_ms * 10)
            for i in range(1, num_tokens, 3):
                idx = int((i/num_tokens) * total_samples)
                f0[idx:min(idx+500, total_samples)] += 25 * (1.0 - (i/num_tokens))
        else:
            f0 = np.linspace(self.f_base, self.f_base*0.8, total_samples)
            if es_pregunta: f0[-int(len(f0)*0.2):] = np.linspace(f0[-int(len(f0)*0.2)], self.f_base*1.4, int(len(f0)*0.2))
        return f0

    def _sintetizar_fonema(self, fonema, f0_contour):
        num_s = len(f0_contour); dur = num_s / self.sr; t = np.linspace(0, dur, num_s, endpoint=False)
        p = self.params.get(fonema, self.params['a'])
        cf = p.get('cf', [500, 1500, 2500, 3500, 4500]); cb = p.get('cb', [100, 100, 100, 100, 100])
        pa = p.get('pa', [0, 0, 0, 0, 0]); v_amp = p.get('v_amp', 0.9)
        asp_amp = p.get('asp', 0); fric_amp = p.get('fric', 0); bypass = p.get('bypass', 0)
        modulacion = np.ones(num_s)
        if fonema == 'R_LAT':
            freq_golpe = 25
            modulacion = (np.sin(2 * np.pi * freq_golpe * t) + 1) / 2
            modulacion = np.where(modulacion > 0.6, 1.0, modulacion * 0.3 + 0.1)
        elif fonema == 'r':
            modulacion = 1.0 - 0.8 * np.exp(-((t - dur/2)**2) / (2 * 0.005**2))
        fuente_voz = self._generar_fuente_lf(f0_contour, num_s) * v_amp * modulacion
        fuente_cascada = fuente_voz + np.random.normal(0, 0.5, num_s) * asp_amp
        audio_cascada = fuente_cascada
        for i in range(len(cf)):
            b, a = signal.iirpeak(cf[i], cf[i]/cb[i], fs=self.sr)
            audio_cascada = signal.lfilter(b, a, audio_cascada)
        ruido_fric = np.random.normal(0, 0.5, num_s) * fric_amp
        audio_paralelo = np.zeros(num_s)
        for i in range(len(pa)):
            if pa[i] > 0:
                b, a = signal.iirpeak(cf[i], cf[i]/cb[i], fs=self.sr)
                audio_paralelo += signal.lfilter(b, a, ruido_fric) * pa[i]
        audio = (audio_cascada * (1.0 - bypass)) + audio_paralelo + (ruido_fric * bypass)
        if fonema not in 'skCxszSCftpx': audio = self._aplicar_high_shelf(audio, gain_db=6.0, fc=3000.0)
        env = np.ones(num_s); at = int(num_s * 0.1); env[:at] = np.linspace(0, 1, at); env[-at:] = np.linspace(1, 0, at)
        audio *= env
        if np.max(np.abs(audio)) > 0: audio = (audio / np.max(np.abs(audio))) * 0.7
        return (audio * 32767).astype(np.int16)

    def sintetizar_texto(self, texto, lang='es'):
        tokens = self._tokenizar(self._procesar_texto(texto, lang))
        total_samples = 0; token_durs = []
        for i, f in enumerate(tokens):
            d = 0.04 if f in 'ptkr' else (self.speed * 1.5 if ('R_' in f or f in 'CS') else self.speed)
            if self.pitch_style == "hts_simulated":
                if f in 'aeiou': d *= 1.3
                if i == 0 or i == len(tokens) - 1: d *= 1.2
            ns = int(self.sr * d); token_durs.append(ns); total_samples += ns
        f0_master = self._calcular_contorno_f0(len(tokens), total_samples, '?' in texto)
        audio_completo = []; curr = 0
        for i, f in enumerate(tokens):
            ns = token_durs[i]
            audio_completo.append(self._sintetizar_fonema(f, f0_master[curr:curr+ns]))
            curr += ns
        return np.concatenate(audio_completo)

    def hablar(self, texto, lang='es'):
        self.stream.write(self.sintetizar_texto(texto, lang).tobytes())

    def guardar_wav(self, texto, filename, lang='es'):
        audio = self.sintetizar_texto(texto, lang)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(self.sr); wf.writeframes(audio.tobytes())

    def detener(self):
        self.stream.stop_stream(); self.stream.close(); self.p.terminate()
