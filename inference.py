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
    
    text = "거대 양당이 차기 지도부를 뽑는 전당대회를 앞두고 나란히 당헌·당규 손질에 나섰지만, 분위기는 사뭇 다릅니다."
    
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
