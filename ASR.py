import platform as plat
import sys
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage


class ASR(object):
    def __init__(self, AM_path = 'model_speech', LM_path = 'model_language'):
        AM = ModelSpeech()
        AM.LoadModel(AM_path)

        LM = ModelLanguage(LM_path)
        LM.LoadModel()

    def decode(wav_file):
        ids = AM.RecognizeSpeech_FromFile(wav_file)
        words = LM.SpeechToText(ids)
        return words


asr = ASR()
w = asr.decode('output.wav')
print(w)


