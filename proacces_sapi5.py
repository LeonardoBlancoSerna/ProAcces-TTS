import win32com.server.register
import pythoncom
from proacces import ProAcces

class ProAccesSAPI5:
    _public_methods_ = ['Speak', 'Stop', 'Pause', 'Resume']
    _reg_progid_ = "ProAcces.TTS"
    _reg_clsid_ = "{YOUR-GUID-HERE-GENERATED-BY-PYTHON}" # El Action generará uno

    def __init__(self):
        self.engine = ProAcces()

    def Speak(self, text, flags):
        self.engine.hablar(text)

    def Stop(self):
        self.engine.detener()

if __name__ == "__main__":
    win32com.server.register.UseCommandLine(ProAccesSAPI5)
