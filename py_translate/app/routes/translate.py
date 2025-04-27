from flask import Blueprint, request, jsonify
from app.routes.common.responses import ResponseMessages
from app.routes.common.translate_models import SUPPORTED_LANGUAGES, SELECTED_MODEL, LANGID_TO_M2M100
from app.utils.request_check import request_body_none_check
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.settings import MAX_TEXT_LENGTH
import inspect
import langid
import torch

import logging

logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print("ERROR: Root logger had no handlers. Logging unavailable.")

translate_blueprint = Blueprint('translate_blueprint', __name__)

_device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Device type: {_device.upper()}")
_tokenizer = AutoTokenizer.from_pretrained(SELECTED_MODEL)
_model = AutoModelForSeq2SeqLM.from_pretrained(SELECTED_MODEL).to(_device)


def to_google_lang_code(code):
    return "no" if code in ["nb", "nn"] else code

def detect_language(text):
    """Determines the language of the text and returns the code M2M100"""
    lang, conf = langid.classify(text)
    return LANGID_TO_M2M100.get(lang, lang), conf  # Convert the code if necessary.

@translate_blueprint.route("/translate", methods=["POST"])
def translate():
    func_name = inspect.currentframe().f_code.co_name

    try:
        json_dict = request.get_json(force=True)
    except Exception as e:
        error_type = type(e).__name__
        error_string = f'Error in {func_name}: {error_type}: {e}'
        return ResponseMessages.error_400(str(error_string))

    try:

        if json_dict is not None:
            text, error_string = request_body_none_check(json_dict=json_dict, key_name="q")
            if error_string != '':
                return ResponseMessages.error_400(str(error_string))

            target_lang, error_string = request_body_none_check(json_dict=json_dict, key_name="target")
            if error_string != '':
                return ResponseMessages.error_400(str(error_string))

            if len(text)>MAX_TEXT_LENGTH:
                return ResponseMessages.error_400(f"Input text for translation is more then {MAX_TEXT_LENGTH} symbols. Current length is {len(text)} symbols.")

            detected_lang, _ = detect_language(text)
            if (detected_lang not in SUPPORTED_LANGUAGES[SELECTED_MODEL]
                    or target_lang not in SUPPORTED_LANGUAGES[SELECTED_MODEL]):
                logger.error(f"Detected language: {detected_lang} ---> Target language: {target_lang}")
                return ResponseMessages.error_400("Unsupported language pair")

            # translation
            inputs = _tokenizer(text, return_tensors="pt", src_lang=detected_lang)  # Source language
            inputs = {k: v.to(_model.device) for k, v in inputs.items()}

            max_length = 100 if _device == "cpu" else 200
            num_beams = 3 if _device == "cpu" else None

            with torch.no_grad():
                outputs = _model.generate(
                    **inputs,
                    forced_bos_token_id=_tokenizer.lang_code_to_id[target_lang],   # Target language
                    max_length=max_length,
                    num_beams=num_beams,
                    early_stopping=True,
                    # top_k=30,    # We allow the model to choose from the 30 most likely options
                    # top_p=0.95,  # Nucleus sampling (more creative)
                    #repetition_penalty=1.2  # Avoiding repetitions
                )

            translated_text = _tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Google API v2 compatible format
            return jsonify({
                "data": {
                    "translations": [{
                        "translatedText": translated_text,
                        "detectedSourceLanguage": to_google_lang_code(detected_lang)  # Autodetect
                    }]
                }
            })

        else:
            return ResponseMessages.error_400("No content")

    except Exception as e:
        return ResponseMessages.error_500(str(e))

@translate_blueprint.route("/detect", methods=["POST"])
def detect_route():
    func_name = inspect.currentframe().f_code.co_name

    try:
        json_dict = request.get_json(force=True)
    except Exception as e:
        error_type = type(e).__name__
        error_string = f'Error in {func_name}: {error_type}: {e}'
        return ResponseMessages.error_400(str(error_string))

    try:

        if json_dict is not None:
            text, error_string = request_body_none_check(json_dict=json_dict, key_name="q")
            if error_string != '':
                return ResponseMessages.error_400(str(error_string))

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

        else:
            return ResponseMessages.error_400("No content")

    except Exception as e:
        return ResponseMessages.error_500(str(e))

@translate_blueprint.route("/languages", methods=["GET"])
def list_languages():
    """Returns a list of supported languages"""
    try:
        return jsonify({
            "data": {
                "languages": [
                    {"code": code, "name": name}
                    for code, name in SUPPORTED_LANGUAGES[SELECTED_MODEL].items()
                ]
            }
        })
    except Exception as e:
        return ResponseMessages.error_500(str(e))