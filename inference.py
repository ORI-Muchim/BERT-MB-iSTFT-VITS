import os
import sys
import click
from api import TTS
import langdetect

@click.command()
@click.option('--ckpt_path', '-m', type=str, default=None, help="Path to the checkpoint file")
@click.option('--output_dir', '-o', type=str, default="outputs", help="Path to the output")


def main(ckpt_path, output_dir):
    if ckpt_path is None:
        raise ValueError("The model_path must be specified")
    
    text = "더불어민주당을 비롯한 야당은 이날 본회의를 단독 소집해 개의했고, 여당인 국민의힘은 이에 반발해 불참했다."
    
    language = langdetector(text)
    config_path = os.path.join(os.path.dirname(ckpt_path), 'config.json')
    model = TTS(language=language, config_path=config_path, ckpt_path=ckpt_path)
    
    for spk_name, spk_id in model.hps.data.spk2id.items():
        save_path = f'{output_dir}/{spk_name}/output.wav'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.tts_to_file(text, spk_id, save_path)


def langdetector(text):
    lang = langdetect.detect(text)
    
    if lang == 'ko':
        language = 'KR'
    elif lang == 'ja':
        language = 'JP'
    elif lang == 'en':
        language = 'EN'
    elif lang == 'zh-cn':
        language = 'ZH'
    elif lang == 'es':
        language = 'ES'
    elif lang == 'fr':
        language = 'FR'
    else:
        language = 'EN'  # Default to English if language not recognized
    
    return language

if __name__ == "__main__":
    main()
