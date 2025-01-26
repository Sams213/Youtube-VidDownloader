import customtkinter
from pytube import YouTube
from ffmpeg_progress_yield import FfmpegProgress
import tkinter
import threading
import os

listR = []
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

os.chdir(os.getcwd())

def videourlf(video,resvar):
    if entry.get()[0:16] not in "https://youtu.be/":
        finishlabel.configure(text='Enter a Youtube Link')
        return None
    return video.streams.filter(adaptive=True, res=resvar, mime_type='audio/mp4').first()

def download1():
    t = threading.Thread(target=downloadVideo, daemon=True)
    t.start()

def downloadVideo():
    if entry.get()[0:16] not in "https://youtu.be/":
        finishlabel.configure(text='Enter a Youtube Link : ')
        return None
    finishlabel.configure(text='')
    video = YouTube(entry.get(), on_progress_callback=on_progress)
    video.streams.filter(res=checkval.get()).first().download()
    if checkval.get() in ['1080p','1440p','2160p']:
        video.streams.get_audio_only().download(filename_prefix='audio ')
        os.chdir(os.getcwd())
        name = video.title
        cmd = [
            'ffmpeg', '-i', f'"{name}.mp4"', '-i', f'{name}.webm', '-c:v', 'copy', '-c:a', 'aac', 'output.mp4'
            ]
        ff = FfmpegProgress(cmd)
        progressbar.set(0)
        for progression in ff.run_command_with_progress():
            progressbar.set(progression/100)


def on_progress(stream, chunk, bytes_remaining):
    total = stream.filesize
    downloaded_bytes = total - bytes_remaining
    percentage = downloaded_bytes / total
    print(percentage)
    progressbar.set(percentage)

def hide_widget(widget):
    widget.pack_forget()

def showWidget(value):
    value.pack()

def check():
    t = threading.Thread(target=check1, daemon=True)
    t.start()
    labelvideo.configure(text=YouTube(entry.get()).title)

def check1():
    global listR 
    listR = list(set([stream.resolution for stream in YouTube(entry.get()).streams]))
    
    for i in listR:
        if i == None:
            listR.remove(i)
    
    for widget in widgets_dict.values():
        hide_widget(widget)
        
    for i in listR:
        if i in widgets_dict.keys():
            showWidget(widgets_dict[i])

main = customtkinter.CTk()
main.geometry("720x480")

main.title("Youtube Downloader")

checkval = tkinter.StringVar(value='')

label = customtkinter.CTkLabel(main, text="Insert Youtube Video Url Here",font=("Arial",18))
label.pack(pady=(25,0))
labelvideo = customtkinter.CTkLabel(main,text='',font=("Arial",14))
labelvideo.pack(pady=(0,5))

frame = customtkinter.CTkFrame(main)
frame.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0.5, anchor='center')
frame.pack()

url = tkinter.StringVar()
entry = customtkinter.CTkEntry(frame, width=410, height=20, textvariable=url)
entry.pack(padx=(50,50),pady=(20,10))

buttoncheck = customtkinter.CTkButton(frame, text='Ckeck', width=175, height=30, command=check)
buttoncheck.pack(pady=(10,10))

frame_radio = customtkinter.CTkFrame(frame, height=0)
frame_radio.place()
frame_radio.pack()

widgets_dict = {
    '144p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='144p', value='144p'),
    '240p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='240p', value='240p'),
    '360p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='360p', value='360p'),
    '480p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='480p', value='480p'),
    '720p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='720p', value='720p'),
    '1080p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='1080p', value='1080p'),
    '1440p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='1440p', value='1440p'),
    '2160p' : customtkinter.CTkRadioButton(frame_radio, variable=checkval, text='2160p', value='2160p'),
}

progressbar = customtkinter.CTkProgressBar(frame, width=520, height=6, bg_color='transparent')
progressbar.pack(pady=(10,0))
progressbar.set(0)

finishlabel = customtkinter.CTkLabel(main, text='')
finishlabel.pack()

button = customtkinter.CTkButton(main, text='Download', width=175, height=30, command=download1)
button.pack()

main.mainloop()