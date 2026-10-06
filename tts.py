# Usage:
# python tts.py test1.srt
# python tts.py test1.srt -v Samantha
# python tts.py test1.srt --voice "Daniel" -o out.wav

import parsesrt,os,pyttsx3, time
from pydub import AudioSegment as adseg, silence
from pydub import effects

import subprocess

import argparse, subprocess

parser = argparse.ArgumentParser(description="Convert an SRT file into a timed audio track using macOS say.")
parser.add_argument("srt", help="path to the input .srt file")
parser.add_argument("-v", "--voice", default=None, help="voice name for say (list them with: say -v '?')")
parser.add_argument("-o", "--output", default="full2.wav", help="output audio file (default: full2.wav)")
args = parser.parse_args()

srtpath = args.srt
voice = args.voice
sppath = os.path.splitext(os.path.basename(srtpath))[0] + "_speech"
threads=[]

parsesrt.parse(srtpath)
print(len(parsesrt.lns), "subtitles parsed")
# time.sleep(2)

if not os.path.exists(sppath):
    os.makedirs(sppath)

def ttsx(x):
    out = os.path.join(sppath, f"{x}.aiff")
    cmd = ["say"]
    if voice:
        cmd += ["-v", voice]
    cmd += ["-o", out, "--", parsesrt.lns[x]]
    subprocess.run(cmd, check=True)

def getTime(st:str,idx:int)->int:
    a=st.split(" --> ")[idx]
    hh=int(a.split(":")[0])
    mm=int(a.split(":")[1])
    ss=int(a.split(":")[2].replace(",",""))
    # print(hh,mm,ss)
    totalmillisecs=hh*60*60*1000+mm*60*1000+ss
    return totalmillisecs

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def compile():
    nl=len(parsesrt.lns.keys())
    print("Compilation started") 
    holder=adseg.empty()
    lastime=0
    printProgressBar(0, 100, prefix = 'Compiling:', suffix = 'Complete', length = 50)
    newtime=getTime(parsesrt.tsmp[1],0)
    slc=adseg.silent(newtime)
    # lastime=getTime(parsesrt.tsmp[i+1],1)
    holder=holder.append(slc, crossfade=0)
    for i in range(1,nl+1):
        crsfade=0
        # lastime=getTime(parsesrt.tsmp[i+1],1)
        startime=getTime(parsesrt.tsmp[i],0)
        endtime=getTime(parsesrt.tsmp[i],1)
        sublength=endtime-startime
        if not i+1>nl:
            nextime=getTime(parsesrt.tsmp[i+1],0)
        if i==nl:
            nextime=endtime
        midlength=nextime-endtime
        # compensate=midlength*0.25
        part = remove_trailing_silence(adseg.from_file(os.path.join(sppath, str(i) + ".aiff")))
        # if (len(part) + len(holder))>endtime:
        if len(part) > sublength:
            new_speed=len(part)/(sublength)
            part=part.speedup(new_speed,150,0)

        holder=holder.append(part, crossfade=crsfade)
        diff = nextime-len(holder)
        # blanktrack=nextime-endtime
        slc=adseg.silent(diff)
        holder=holder.append(slc, crossfade=crsfade)
        # compensate=(lastime-newtime)-len(part)
        # lastime-=compensate
        printProgressBar(i, nl, prefix = 'Compiling:', suffix = 'Complete', length = 50)

    holder.export(args.output, format="wav")
    print("compilation finished")
# # for key in parsesrt.tsmp.keys():
# #     part=adseg.from_file(os.path.join(sppath,str(key)+".wav"))
# #     holder=holder.append(part)

def remove_trailing_silence(sound):
    endtrim=silence.detect_leading_silence(sound.reverse())
    return sound[:len(sound)-endtrim]


print("TTS started")
start_time = time.time()
nl=len(parsesrt.lns.keys())

printProgressBar(0, 100, prefix = 'TTS:', suffix = 'Converted', length = 50)
for key in parsesrt.lns.keys():
    # print(key)
    ttsx(key) #--SKIP FOR TESTING
    printProgressBar(key, nl, prefix = 'TTS:', suffix = 'Converted', length = 50)

print("tts finished")

print("TTS converted in %s seconds " % (time.time() - start_time))

start_time = time.time()

compile()

print("Compiled in %s seconds " % (time.time() - start_time))
