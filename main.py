import tkinter
from tkinter.messagebox import showinfo
from tkinter.filedialog import askdirectory
import youtube_dl as ytdl
import time
from datetime import date

window = tkinter.Tk()
window.resizable = False

window.title = "YTDownloadWizard"

#the top label
top_label = tkinter.Label(window, font="Helvetica 18 bold")
top_label.config(text="YTDownloadWizard")
top_label.grid(row=0, column=1)

url_field = tkinter.Entry(window)
url_field.grid(row=1, column=1)

url_field_label = tkinter.Label(window, font="Helvetica 12")
url_field_label.config(text="Video URL", justify=tkinter.RIGHT)
url_field_label.grid(row=1, column=0)

def download():
    url = url_field.get()
    directory = askdirectory()
    ytdl_ops = {"outtmpl":(directory+"/YTDlWiz_"
                           +str(date.today())
                           +str(time.time())
                           +video_format.get())}
    with ytdl.YoutubeDL(ytdl_ops) as yt:
        try:
            yt.download([url])
            showinfo("Download Complete!")
        except:
            showinfo("Error!", "Failed to download. Make sure the URL is valid!")
            return

video_format = tkinter.StringVar()
download_button = tkinter.Button(window, text="Download", command=download)
download_button.grid(row=2, column=1)

def check_format():
    global video_format
    vf = video_format.get()
    if not (vf in [".mp4", ".mov"]):
        download_button_state = tkinter.DISABLED
    else:
        download_button_state = tkinter.NORMAL
    download_button['state'] = download_button_state

format_mp4 = tkinter.Radiobutton(value=".mp4", variable=video_format, text=".mp4", indicatoron=0,
                                 command=check_format)
format_mov = tkinter.Radiobutton(value=".mov", variable=video_format, text=".mov", indicatoron=0,
                                 command=check_format)
format_mp4.grid(row=3, column=0)
format_mov.grid(row=3, column=1)

check_format()

window.mainloop()
