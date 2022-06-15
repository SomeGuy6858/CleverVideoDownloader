import os
import os.path
import PySimpleGUI as sg
from pytube import YouTube
import ffmpeg
import subprocess

#FileExtensions = [".mp3", ".mp4", ".ogg", ".mkv"]

file_list_column = [
    [
        sg.Text("Save Location"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    
]

layout = [[sg.Text("Please Input the Desired Link"),
sg.Text(""), sg.InputText()],
[sg.Column(file_list_column)],
[sg.Combo([".mp3",".mp4",".ogg",".mkv"], size = (20, 4), readonly = True,default_value= ".mp4", key = "-COMBO1-")],
[sg.Text("Resolution:"), sg.Combo(["144p","240p","480p","720p","1080p", "1440p", "4K"], default_value= "1080p", key= "-COMBO2-")],
[sg.Checkbox("Audio Only?", default= False, key= "-YESNO-")],
[sg.Button("Confirm"), sg.Button("Cancel")]]



window = sg.Window("Downloader", layout)
while True:
    event, values = window.read()
    #print(values["-FOLDER-"])
    if event == "Confirm":
        link = YouTube(str(values[0]))
        if values["-YESNO-"] == True:
            audio = link.streams.filter(only_audio = True).first()
            out_fileAudio = audio.download(output_path=values["-FOLDER-"])
            base, ext = os.path.splitext(out_fileAudio)
            newFileAudio = base + "audio" + values["-COMBO1-"]
            os.rename(out_fileAudio, newFileAudio)
        if values["-YESNO-"] == False:
            audio = link.streams.filter(only_audio = True).first()
            out_fileAudio = audio.download(output_path=values["-FOLDER-"])
            base, ext = os.path.splitext(out_fileAudio)
            newFileAudio = base + "audio" + values["-COMBO1-"]
            os.rename(out_fileAudio, newFileAudio)
            video = link.streams.filter(resolution= values["-COMBO2-"]).first()
            out_file = video.download(output_path=values["-FOLDER-"])
            base, ext = os.path.splitext(out_file)
            newFileVideo = base + values["-COMBO1-"]
            os.rename(out_file, newFileVideo)
            VideoName = os.path.basename(newFileVideo)
            AudioName = os.path.basename(newFileAudio)
            input_video = ffmpeg.input(values["-FOLDER-"]+ "\\" + VideoName)
            input_audio = ffmpeg.input(values["-FOLDER-"]+ "\\" +AudioName)
            OutPath = values["-FOLDER-"]
            print(OutPath)
            print(VideoName)
            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(OutPath + "\\" + "compiled" + VideoName).run()

    if event == "Cancel":
     break
    elif event == sg.WIN_CLOSED:
        break
    #print('Test', values[])
