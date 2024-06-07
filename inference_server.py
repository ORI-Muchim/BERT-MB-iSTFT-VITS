import os
import torch
import click
from flask import Flask, request, jsonify
from api import TTS
import langdetect
from datetime import datetime

app = Flask(__name__)

# Global variables to hold the model
model = None
language = None

def load_model(ckpt_path):
    global model, language
    config_path = os.path.join(os.path.dirname(ckpt_path), 'config.json')
    text = "안녕하세요. 만나서 반갑습니다."
    language = langdetector(text)
    model = TTS(language=language, config_path=config_path, ckpt_path=ckpt_path)


def langdetector(text):
    lang = langdetect.detect(text)
    language_map = {
        'ko': 'KR',
        'ja': 'JP',
        'en': 'EN',
        'zh-cn': 'ZH',
        'es': 'ES',
        'fr': 'FR'
    }
    return language_map.get(lang, 'EN')

@app.route('/synthesize', methods=['POST'])


def synthesize():
    data = request.json
    text = data.get('text')
    output_dir = data.get('output_dir', 'outputs')
    
    if text is None:
        return jsonify({'error': 'Text is required'}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for spk_name, spk_id in model.hps.data.spk2id.items():
        save_path = f'{output_dir}/{spk_name}/{timestamp}.wav'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.tts_to_file(text, spk_id, save_path)
    
    return jsonify({'message': 'Synthesis complete', 'output_dir': output_dir})

@click.command()
@click.option('--ckpt_path', '-m', type=str, default=None, help="Path to the checkpoint file")
@click.option('--host', '-h', type=str, default='0.0.0.0', help="Host to run the server on")
@click.option('--port', '-p', type=int, default=5000, help="Port to run the server on")


def main(ckpt_path, host, port):
    if ckpt_path is None:
        raise ValueError("The model_path must be specified")
    load_model(ckpt_path)
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
