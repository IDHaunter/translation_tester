from flask import Blueprint, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import langid
import torch

SELECTED_MODEL = "base"  # "base" / "large"

"""
NLLB-200, 196 languages, license (Creative Commons Attribution-NonCommercial 4.0)
    https://huggingface.co/facebook/nllb-200-distilled-600M
    https://huggingface.co/facebook/nllb-200-distilled-1.3B

M2M100, 100 languages, MIT
    https://huggingface.co/facebook/m2m100_418M
    https://huggingface.co/facebook/m2m100_1.2B
"""

MODELS = {
    "base": "facebook/m2m100_418M",
    "large": "facebook/m2m100_1.2B",
}

# Supported languages and their codes in M2M100
SUPPORTED_LANGUAGES = {
    "en": "english",
    "ru": "russian",
    "no": "norwegian",  # Common code for Norwegian
    "nb": "norwegian bokmål",
    "nn": "norwegian nynorsk"
}

# Language codes matching langid → M2M100
LANGID_TO_M2M100 = {
    "nb": "no",  # Bokmål → common code
    "nn": "no",  # Nynorsk → common code
}
# ========================

def to_google_lang_code(code):
    return "no" if code in ["nb", "nn"] else code

translate_blueprint = Blueprint('translate_blueprint', __name__)
model_cache = {}

def load_model():
    """Loads the model and tokenizer with caching"""
    if SELECTED_MODEL not in model_cache:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(MODELS[SELECTED_MODEL])
        model = AutoModelForSeq2SeqLM.from_pretrained(MODELS[SELECTED_MODEL]).to(device)
        model_cache[SELECTED_MODEL] = (tokenizer, model)
    return model_cache[SELECTED_MODEL]

def detect_language(text):
    """Determines the language of the text and returns the code M2M100"""
    lang, conf = langid.classify(text)
    return LANGID_TO_M2M100.get(lang, lang), conf  # Convert the code if necessary.

@translate_blueprint.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("q")
    target_lang = data.get("target")

    if not text or not target_lang:
        return jsonify({"error": "Missing 'q' or 'target' parameter"}), 400

    detected_lang, _ = detect_language(text)
    if detected_lang not in SUPPORTED_LANGUAGES or target_lang not in SUPPORTED_LANGUAGES:
        return jsonify({"error": "Unsupported language pair"}), 400

    # Loading the model and translation
    tokenizer, model = load_model()
    inputs = tokenizer(text, return_tensors="pt", src_lang=detected_lang)  # Source language
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    device_type = "gpu" if torch.cuda.is_available() else "cpu"
    max_length = 100 if device_type == "cpu" else 200
    num_beams = 3 if device_type == "cpu" else None

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],   # Target language
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True,
            # top_k=30,    # We allow the model to choose from the 30 most likely options
            # top_p=0.95,  # Nucleus sampling (more creative)
            #repetition_penalty=1.2  # Avoiding repetitions
        )

    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Google API v2 compatible format
    return jsonify({
        "data": {
            "translations": [{
                "translatedText": translated_text,
                "detectedSourceLanguage": to_google_lang_code(detected_lang)  # Автоопределение
            }]
        }
    })

@translate_blueprint.route("/detect", methods=["POST"])
def detect_route():
    data = request.get_json()
    text = data.get("q")

    if not text:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    try:
        language, confidence = detect_language(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "data": {
            "detections": [
                [
                    {
                        "language": to_google_lang_code(language),
                        "isReliable": confidence > 0.85,
                        "confidence": confidence
                    }
                ]
            ]
        }
    })

@translate_blueprint.route("/languages", methods=["GET"])
def list_languages():
    """Returns a list of supported languages"""
    return jsonify({
        "data": {
            "languages": [
                {"code": code, "name": name}
                for code, name in SUPPORTED_LANGUAGES.items()
            ]
        }
    })