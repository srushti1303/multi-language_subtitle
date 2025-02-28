from googletrans import Translator

class TranslateModel:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, target_lang):
        translation = self.translator.translate(text, dest=target_lang)
        return translation.text  # Ensure this works
    
