import tkinter
import threading
from tkinter.messagebox import showinfo
from tkinter.filedialog import askdirectory
import youtube_dl as ytdl

window = tkinter.Tk()
window.resizable(False, False)

window.title("YTDownloadWizard")
window.config(bg="white")

btxt = tkinter.StringVar()
btxt.set(value="Download")

# the top label
top_label = tkinter.Label(window, font="Helvetica 18 bold", text="YTDownloadWizard", bg="white")
top_label.grid(row=0, column=0, columnspan=2)

url_field = tkinter.Entry(window, width=40, bg="white")
url_field.grid(row=1, column=1)

url_field_label = tkinter.Label(window, font="Helvetica 12", text="Video URL", justify=tkinter.RIGHT, bg="white")
url_field_label.grid(row=1, column=0)


def download():
    global btxt

    def progress_hook(d):
        global btxt
        if d['status'] == 'downloading':
            btxt.set(value=str(
                round(
            float(d['downloaded_bytes'])/
            float(d['total_bytes'])
            *100))+"%")
            download_button["state"] = tkinter.DISABLED
        else:
            btxt.set(value="Download")
            download_button["state"] = tkinter.NORMAL

    directory = askdirectory()
    url = url_field.get()
    ytdl_ops = {
        "outtmpl":(directory + "/%s.%s"%
                   (
                    ytdl.YoutubeDL({})
                         .extract_info(url=url, download=False)
                         .get("title", None),
                    video_format
                         .get()
                   )
                ),
        "progress_hooks":[progress_hook]
                }
    with ytdl.YoutubeDL(ytdl_ops) as yt:
        try:
            yt.download([url])
            showinfo("Download Complete!", "You can close the window.")
        except:
            showinfo("Error!", "Failed to download. Make sure the URL is valid!")
            return


def download_threader():
    thr = threading.Thread(target=download)
    thr.start()


video_format = tkinter.StringVar()
download_button = tkinter.Button(window, textvariable=btxt, command=download_threader, width=18, height=2, bd=0, bg="turquoise")
download_button.grid(row=2, column=0, columnspan=2, pady=5)


def check_format():
    global video_format
    vf = video_format.get()
    if not (vf in [".mp4", ".mov"]):
        download_button_state = tkinter.DISABLED
    else:
        download_button_state = tkinter.NORMAL
    download_button['state'] = download_button_state


format_mp4 = tkinter.Radiobutton(value=".mp4", variable=video_format, text=".mp4", indicatoron=0,
                                 command=check_format,  bd=0, bg="turquoise", activebackground="darkblue", selectcolor="blue")
format_mov = tkinter.Radiobutton(value=".mov", variable=video_format, text=".mov", indicatoron=0,
                                 command=check_format,  bd=0, bg="turquoise", activebackground="darkblue", selectcolor="blue")
format_mp4.grid(row=3, column=0, pady=1)
format_mov.grid(row=3, column=1, pady=1)

check_format()

window.mainloop()