import os
import click
from api import TTS
import langdetect

    
@click.command()
@click.option('--ckpt_path', '-m', type=str, default=None, help="Path to the checkpoint file")
@click.option('--text', '-t', type=str, default=None, help="Text to speak")
@click.option('--output_dir', '-o', type=str, default="outputs", help="Path to the output")

def langdetector(text):
    lang = langdetect.detect(text)

    if lang == 'ko':
        language = 'KR'
        return language
    elif lang == 'ja':
        language = 'JP'
        return language
    elif lang == 'en':
        language = 'EN'
        return language
    elif lang == 'zh-cn':
        language = 'ZH'
        return language
    elif lang == 'es':
        language = 'ES'
        return language
    elif lang == 'fr':
        language = 'FR'
        return language


def main(ckpt_path, text, language, output_dir):
    if ckpt_path is None:
        raise ValueError("The model_path must be specified")
    
    language = langdetector(text)
    config_path = os.path.join(os.path.dirname(ckpt_path), 'config.json')
    model = TTS(language=language, config_path=config_path, ckpt_path=ckpt_path)
    
    for spk_name, spk_id in model.hps.data.spk2id.items():
        save_path = f'{output_dir}/{spk_name}/output.wav'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.tts_to_file(text, spk_id, save_path)

if __name__ == "__main__":
    main()
