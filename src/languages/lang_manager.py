import json
import os

#language manager using i18n
class LanguageManager:
    def __init__(self):
        self._lang_code = None
        self._lang_dir = None
        self.translations = {}

    @property
    def lang_code(self):
        return self._lang_code

    @lang_code.setter
    def lang_code(self, value):
        self._lang_code = value
        if self._lang_dir:
            self.load_language(value)

    @property
    def lang_dir(self):
        return self._lang_dir

    @lang_dir.setter
    def lang_dir(self, value):
        self._lang_dir = value
        if self._lang_code:
            self.load_language(self._lang_code)

    def load_language(self, lang_code):
        if not self._lang_dir:
            return
        lang_path = os.path.join(self._lang_dir, f"{lang_code}.json")
        try:
            with open(lang_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            self.translations = {}

    def set_language(self, lang_code):
        self.lang_code = lang_code

    def set_lang_dir(self, lang_dir):
        self.lang_dir = lang_dir

    def get_text(self, key, **kwargs):
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text
