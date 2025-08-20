def load_translations(language_code):
    import json
    import os

    # Define the path to the languages directory
    languages_dir = os.path.join(os.path.dirname(__file__), 'modals', 'languages')

    # Construct the file path for the requested language
    file_path = os.path.join(languages_dir, f"{language_code}.json")

    # Load the translations from the JSON file
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Translation file for language '{language_code}' not found.")

def translate(key, language_code='en'):
    translations = load_translations(language_code)
    return translations.get(key, key)  # Return the key if translation is not found

def available_languages():
    return ['en', 'es', 'fr']  # List of available language codes