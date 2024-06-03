# BERT-MB-iSTFT-VITS

- Supported Language: Korean, Japanese, Chinese, English, French, Spanish

## Table of Contents 
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Create transcript](#create-transcript)
- [Preprocess](#preprocess)
- [Training](#training)
- [To-Do](#to-do)
- [References](#references)


## Prerequisites
- A Windows/Linux system with a minimum of `16GB` RAM.
- A GPU with at least `12GB` of VRAM.
- Python == 3.8
- Anaconda installed.
- PyTorch installed.
- CUDA 11.x installed.

Pytorch install command:
```sh
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
```

CUDA 11.7 install:
`https://developer.nvidia.com/cuda-11-7-0-download-archive`

---


## Installation 
1. **Create an Anaconda environment:**

```sh
conda create -n vits python=3.8
```

2. **Activate the environment:**

```sh
conda activate vits
```

3. **Clone this repository to your local machine:**

```sh
git clone https://github.com/project-elnino/BERT-MB-iSTFT-VITS.git
```

4. **Navigate to the cloned directory:**

```sh
cd BERT-MB-iSTFT-VITS
```

5. **Install the necessary dependencies:**

```sh
pip install -r requirements.txt
```


## Create transcript

```
path/to/audio_001.wav |<speaker_name>|<language_code>|<text_001>
```
- Example
```
../kss2/1/1_0000.wav|KR-default|KR|그는 괜찮은 척하려고 애쓰는 것 같았다.
```


## Preprocess
```sh
python preprocess.py --metadata ./metadata.list --config_path ./configs/config.json
```

If your speech file is either not `Mono / PCM-16`, the you should resample your .wav file first. 


## Setting json file in [configs](configs)

| Model | How to set up json file in [configs](configs) | Sample of json file configuration|
| :---: | :---: | :---: |
| iSTFT-VITS | ```"istft_vits": true, ```<br>``` "upsample_rates": [8,8], ``` | ljs_istft_vits.json |
| MB-iSTFT-VITS | ```"subbands": 4,```<br>```"mb_istft_vits": true, ```<br>``` "upsample_rates": [4,4], ``` | ljs_mb_istft_vits.json |
| MS-iSTFT-VITS | ```"subbands": 4,```<br>```"ms_istft_vits": true, ```<br>``` "upsample_rates": [4,4], ``` | ljs_ms_istft_vits.json |

- If you have done preprocessing, set "cleaned_text" to true. 
- Change `training_files` and `validation_files` to the path of preprocessed manifest files. 
- Select same `text_cleaners` you used in preprocessing step. 

## Training
```sh
python train.py -c <config> -m <folder>
```
Resume training from lastest checkpoint is automatic.

OR, Check [inference_cpu.py](inference_cpu.py)

```sh
python inference_cpu.py {model_name} {model_step}
```

## To-Do

- It is very UNSTABLE.

- Need to fix ```data_utils.py``` in TextAudioLoader class.

```
Traceback (most recent call last):
  File "train.py", line 334, in <module>
    main()
  File "train.py", line 58, in main
    mp.spawn(run, nprocs=n_gpus, args=(n_gpus, hps,))
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/multiprocessing/spawn.py", line 240, in spawn
    return start_processes(fn, args, nprocs, join, daemon, start_method='spawn')
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/multiprocessing/spawn.py", line 198, in start_processes
    while not context.join():
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/multiprocessing/spawn.py", line 160, in join
    raise ProcessRaisedException(msg, error_index, failed_process.pid)
torch.multiprocessing.spawn.ProcessRaisedException: 

-- Process 0 terminated with the following error:
Traceback (most recent call last):
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/multiprocessing/spawn.py", line 69, in _wrap
    fn(i, *args)
  File "/home/ori/Desktop/MB-iSTFT-VITS-Korean/train.py", line 130, in run
  File "/home/ori/Desktop/MB-iSTFT-VITS-Korean/train.py", line 151, in train_and_evaluate
    with autocast(enabled=hps.train.fp16_run):
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/dataloader.py", line 530, in __next__
    data = self._next_data()
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/dataloader.py", line 1224, in _next_data
    return self._process_data(data)
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/dataloader.py", line 1250, in _process_data
    data.reraise()
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/_utils.py", line 457, in reraise
    raise exception
AttributeError: Caught AttributeError in DataLoader worker process 0.
Original Traceback (most recent call last):
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/_utils/worker.py", line 287, in _worker_loop
    data = fetcher.fetch(index)
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/_utils/fetch.py", line 49, in fetch
    data = [self.dataset[idx] for idx in possibly_batched_index]
  File "/home/ori/anaconda3/envs/vits/lib/python3.8/site-packages/torch/utils/data/_utils/fetch.py", line 49, in <listcomp>
    data = [self.dataset[idx] for idx in possibly_batched_index]
  File "/home/ori/Desktop/MB-iSTFT-VITS-Korean/data_utils.py", line 94, in __getitem__
    return self.get_audio_text_pair(self.audiopaths_and_text[index])
AttributeError: 'TextAudioLoader' object has no attribute 'audiopaths_and_text'
```

## References
- [MasayaKawamura/MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS)
- [myshell-ai/MeloTTS](https://github.com/myshell-ai)
