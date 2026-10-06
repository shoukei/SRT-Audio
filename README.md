<h1> SRT-Audio </h1>

Create audio file from srt file.

## About this fork

This is a fork of https://github.com/magnusjwatson2786/SRT-Audio
modified to use the say command on Macs.


## Install
To install this program, clone it to your local machine and cd into it and:

```sh
python3.11 -m venv venv
source venv/bin/activate.fish # use from fish
pip install -r requirements.txt
```

## Usage examples
```
python tts.py test1.srt
python tts.py test1.srt -v Samantha
python tts.py test1.srt --voice "Fred" -o out.wav
```

## License

MIT

**Free Software, Hell Yeah!**

*Happy Coding!*

[//]: # (links)
    
   [Python]: <https://www.python.org/>
   [Pyttsx3]: <https://pypi.org/project/pyttsx3/>
   [Pydub]: <https://github.com/jiaaro/pydub>
   
