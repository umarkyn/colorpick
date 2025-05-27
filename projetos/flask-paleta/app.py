import os
import time
from flask import Flask, render_template, request
from colorthief import ColorThief

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
CSS_PATH = os.path.join(BASE_DIR, 'static', 'paleta.css')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def rgb_para_hex(rgb):
    return '#%02x%02x%02x' % rgb

@app.route('/')
def index():
    versao_css = int(time.time())
    return render_template('index.html', versao_css=versao_css)

@app.route('/upload', methods=['POST'])
def upload():
    if 'foto' not in request.files:
        return 'Nenhuma imagem enviada.'

    file = request.files['foto']
    if file.filename == '':
        return 'Nome do arquivo está vazio.'

    if file:
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(caminho_arquivo)

        color_thief = ColorThief(caminho_arquivo)
        paleta = color_thief.get_palette(color_count=5)
        paleta_hex = [rgb_para_hex(cor) for cor in paleta]

        css_gerado = ""
        for i, cor in enumerate(paleta_hex):
            css_gerado += f".cor-{i} {{ background-color: {cor}; }}\n"

        with open(CSS_PATH, 'w') as f:
            f.write(css_gerado)

        caminho_para_html = '/' + os.path.relpath(caminho_arquivo, BASE_DIR).replace('\\', '/')
        versao_css = int(time.time())

        return render_template('index.html', caminho=caminho_para_html, cores=range(len(paleta_hex)), versao_css=versao_css)

    return 'Erro ao processar o arquivo.'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
