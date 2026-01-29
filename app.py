from flask import Flask, render_template, request, send_file, url_for
import io

app = Flask(__name__)

try:
    from googletrans import Translator
    HAS_GOOGLETRANS = True
except Exception:
    HAS_GOOGLETRANS = False

try:
    from gtts import gTTS
    HAS_GTTS = True
except Exception:
    HAS_GTTS = False

FALLBACK = {
    'hello': 'ಹಲೋ',
    'hi': 'ಹಾಯ್',
    'thank you': 'ಧನ್ಯವಾದಗಳು',
    'thanks': 'ಧನ್ಯವಾದಗಳು',
    'yes': 'ಹೌದು',
    'no': 'ಇಲ್ಲ',
    'good': 'ಚೆನ್ನಾಗಿದೆ',
    'bad': 'ಕೆಟ್ಟದು',
    'please': 'ದಯವಿಟ್ಟು',
    'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಾ'
}


def translate_text(text: str) -> str:
    if not text:
        return ''

    if HAS_GOOGLETRANS:
        try:
            t = Translator()
            translated = t.translate(text, dest='kn')
            return translated.text
        except Exception:
            pass

    lowered = text.lower().strip()
    if lowered in FALLBACK:
        return FALLBACK[lowered]

    parts = text.split()
    out = []
    for w in parts:
        key = w.lower().strip('.,!?')
        out.append(FALLBACK.get(key, w))
    return ' '.join(out)


@app.route('/audio')
def audio():
    text = request.args.get('text', '').strip()
    lang = request.args.get('lang', 'kn')
    if not text:
        return ('', 400)

    # Prefer gTTS if available; it supports many languages including Kannada ('kn')
    if HAS_GTTS:
        try:
            tts = gTTS(text=text, lang=lang)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return send_file(buf, mimetype='audio/mpeg', as_attachment=False, download_name='translation.mp3')
        except Exception:
            pass

    # If gTTS not available, return 501 Not Implemented
    return ('TTS engine unavailable', 501)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    src = ''
    used = 'googletrans' if HAS_GOOGLETRANS else 'fallback'
    if request.method == 'POST':
        src = request.form.get('text', '').strip()
        result = translate_text(src)
    return render_template('index.html', result=result, src=src, used=used)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
