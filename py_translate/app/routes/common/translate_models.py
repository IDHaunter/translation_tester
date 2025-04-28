from app.settings import SELECTED_MODEL, M2M100_418, M2M100_1200

# Language codes matching langid → M2M100
LANGID_TO_M2M100 = {
    "nb": "no",  # Bokmål → common code
    "nn": "no",  # Nynorsk → common code
}

# Languages for model M2M100
SUPPORTED_LANGUAGES_M2M100 = {
    "af": "afrikaans",
    "am": "amharic",
    "ar": "arabic",
    "az": "azerbaijani",
    "be": "belarusian",
    "bg": "bulgarian",
    "bn": "bengali",
    "ca": "catalan",
    "cs": "czech",
    "cy": "welsh",
    "da": "danish",
    "de": "german",
    "el": "greek",
    "en": "english",
    "es": "spanish",
    "et": "estonian",
    "fa": "persian",
    "fi": "finnish",
    "fr": "french",
    "gu": "gujarati",
    "he": "hebrew",
    "hi": "hindi",
    "hr": "croatian",
    "hu": "hungarian",
    "id": "indonesian",
    "is": "icelandic",
    "it": "italian",
    "ja": "japanese",
    "jv": "javanese",
    "ka": "georgian",
    "kk": "kazakh",
    "km": "khmer",
    "kn": "kannada",
    "ko": "korean",
    "lo": "lao",
    "lt": "lithuanian",
    "lv": "latvian",
    "mk": "macedonian",
    "ml": "malayalam",
    "mn": "mongolian",
    "mr": "marathi",
    "ms": "malay",
    "my": "burmese",
    "ne": "nepali",
    "nl": "dutch",
    "no": "norwegian",
    "nb": "norwegian bokmål",
    "nn": "norwegian nynorsk",
    "pa": "punjabi",
    "pl": "polish",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "si": "sinhala",
    "sk": "slovak",
    "sl": "slovenian",
    "sq": "albanian",
    "sr": "serbian",
    "sv": "swedish",
    "sw": "swahili",
    "ta": "tamil",
    "te": "telugu",
    "th": "thai",
    "tl": "tagalog",
    "tr": "turkish",
    "uk": "ukrainian",
    "ur": "urdu",
    "vi": "vietnamese",
    "zh": "chinese"
}

# Language support across supported models
SUPPORTED_LANGUAGES = {
    M2M100_418: SUPPORTED_LANGUAGES_M2M100,
    M2M100_1200: SUPPORTED_LANGUAGES_M2M100,  # equal with "base"
}
