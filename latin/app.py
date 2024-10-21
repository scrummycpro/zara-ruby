from flask import Flask, render_template, request
from googletrans import Translator
from googletrans.models import Translated

app = Flask(__name__)

# Initialize the translator
translator = Translator()

# Translation mappings
languages = {
    'he': 'Hebrew',
    'ar': 'Arabic',
    'el': 'Greek',
    'la': 'Latin'
}

# Store recent translations (in memory)
recent_translations = []

@app.route("/", methods=["GET", "POST"])
def index():
    translation_results = {}
    if request.method == "POST":
        sentence = request.form.get("sentence")
        if sentence:
            for lang_code, lang_name in languages.items():
                try:
                    # Translate the sentence and ensure the result is valid
                    translated = translator.translate(sentence, dest=lang_code)
                    if isinstance(translated, Translated) and translated.text:
                        translation_results[lang_name] = {
                            "forward": translated.text,
                            "backward": translated.text[::-1]  # Reverse the translated text
                        }
                    else:
                        translation_results[lang_name] = {
                            "forward": "Translation failed",
                            "backward": "Translation failed"
                        }
                except Exception as e:
                    translation_results[lang_name] = {
                        "forward": f"Error: {str(e)}",
                        "backward": f"Error: {str(e)}"
                    }
            # Add to recent translations
            recent_translations.append({"sentence": sentence, "results": translation_results})
            if len(recent_translations) > 5:  # Limit to 5 recent translations
                recent_translations.pop(0)
    return render_template("index.html", translation_results=translation_results)


@app.route("/recent", methods=["GET", "POST"])
def recent():
    search_query = request.form.get("search_query", "").lower()
    filtered_translations = []

    if search_query:
        # Filter the recent translations based on the search query
        for translation in recent_translations:
            if search_query in translation["sentence"].lower():
                filtered_translations.append(translation)
            else:
                for lang, result in translation["results"].items():
                    if search_query in result["forward"].lower() or search_query in result["backward"].lower():
                        filtered_translations.append(translation)
                        break
    else:
        filtered_translations = recent_translations

    return render_template("recent.html", recent_translations=filtered_translations, search_query=search_query)


if __name__ == "__main__":
    app.run(debug=True)
