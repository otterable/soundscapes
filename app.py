from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_url_path='/static')

def get_soundscapes():
    soundscapes = []
    soundscapes_path = os.path.join(app.static_folder, 'soundscapes')
    for folder in os.listdir(soundscapes_path):
        if os.path.isdir(os.path.join(soundscapes_path, folder)):
            soundscapes.append(folder)
    return soundscapes
    


@app.route('/')
def index():
    soundscapes = get_soundscapes()
    all_files = []

    for soundscape in soundscapes:
        soundscape_path = os.path.join(app.static_folder, 'soundscapes', soundscape)
        files = [file for file in os.listdir(soundscape_path) if file.lower().endswith(('.mp3', '.wav'))]
        all_files.extend(files)

    return render_template('index.html', soundscapes=soundscapes, files=all_files, selected='all')
    
@app.route('/sounds/all/')
def all_sounds():
    files = []
    for soundscape in soundscapes:
        soundscape_path = os.path.join(app.static_folder, 'soundscapes', soundscape)
        if os.path.exists(soundscape_path) and os.path.isdir(soundscape_path):
            for root, _, filenames in os.walk(soundscape_path):
                for filename in filenames:
                    if filename.lower().endswith(('.mp3', '.wav')):
                        file_path = os.path.join(root, filename)
                        files.append(file_path.replace(app.static_folder + '/soundscapes/', ''))
    
    return render_template('index.html', files=files, soundscapes=soundscapes)

@app.route('/sounds/<soundscape>/')
def sounds(soundscape):
    soundscape_path = os.path.join(app.static_folder, 'soundscapes', soundscape)
    files = [file for file in os.listdir(soundscape_path) if file.lower().endswith(('.mp3', '.wav'))]
    return render_template('index.html', soundscapes=get_soundscapes(), files=files, selected=soundscape)

@app.route('/sounds/<soundscape>/<filename>')
def play_sound(soundscape, filename):
    return send_from_directory(os.path.join('static', 'soundscapes', soundscape), filename)

if __name__ == '__main__':
    app.run(debug=True)
