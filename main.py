import base64
import ctypes
import json
import os
import paramiko
import shlex
import subprocess
import sys
import time
import sys
from PIL import Image, ImageTk
from tkinter import *
from tkinter.filedialog import askopenfilename


def transmission_web(mt, data):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(json['transmission_server_ip'], username=json[
                   'username'], password=json['password'])
    if mt == "t":
        ftp_client = client.open_sftp()
        ftp_client.put(data, "/tmp/" + os.path.basename(data))
        ftp_client.close()
        data = shlex.quote("/tmp/" + os.path.basename(data))

    stdin, stdout, stderr = client.exec_command(
        'transmission-remote -a ' + data)
    root = Tk()
    root.title("Torrent selector")
    root.iconbitmap("icon.ico")
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))
    response = ""
    for line in stdout:
        response = response + line.strip('\n')
    client.close()
    response_text = Label(root, text=response)
    response_text.pack()
    root.after(1500, lambda: root.destroy())
    root.mainloop()
    sys.exit()


def stage_3(root, mt, y, z):
    root.destroy()
    if mt == "m":
        if y == "q":
            os.system('START ' + json["qbittorrent_exe_path"] + ' ' + z)
            sys.exit()

        elif y == "t":
            transmission_web(mt, z)
    elif mt == "t":
        if y == "q":
            subprocess.Popen([json["qbittorrent_exe_path"], z])
            sys.exit()

        elif y == "t":
            transmission_web(mt, z)


def stage_2(root, mt, z):
    root.destroy()
    root = Tk()
    root.title("Torrent selector")
    root.iconbitmap("icon.ico")
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))
    qt_image = Image.open("qb.png")
    qt_img = ImageTk.PhotoImage(qt_image.resize((50, 50)))
    qb_image = Label(root, image=qt_img)
    qb_image.bind("<Button-1>", lambda a: stage_3(root, mt, "q", z))
    qb_image.grid(row=0, sticky=W)

    qb_name = Label(root, text="Qbittorent")
    qb_name.grid(row=0, column=1)
    qb_name.bind("<Button-1>", lambda a: stage_3(root, mt, "q", z))

    tr_image = Image.open("tr.png")
    tr_img = ImageTk.PhotoImage(tr_image.resize((50, 50)))
    tr_image = Label(root, image=tr_img)
    tr_image.bind("<Button-1>", lambda a: stage_3(root, mt, "t", z))
    tr_image.grid(row=1, sticky=W)

    tr_name = Label(root, text="Transmission")
    tr_name.grid(row=1, column=1)
    tr_name.bind("<Button-1>", lambda a: stage_3(root, mt, "t", z))

    root.mainloop()


def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(13)
    data = ctypes.c_wchar_p(pcontents).value
    ctypes.windll.user32.CloseClipboard()
    return data


def magnet_input(root):
    root.destroy()
    root = Tk()
    root.title("Torrent selector")
    root.iconbitmap("icon.ico")
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    clip = winGetClipboard()
    e = Entry(root)
    if "magnet" in clip:
        e.insert(0, clip)
    e.pack()
    b = Button(root, text="Submit",
               command=lambda: stage_2(root, "m", e.get()))
    b.pack()
    root.mainloop()


def torrent_file(b):
    filename = askopenfilename()
    b.configure(text=filename)


def torrent(root):
    root.destroy()
    root = Tk()
    root.title("Torrent selector")
    root.iconbitmap("icon.ico")
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))
    b = Button(root, text="File")
    b.pack()
    l = Label(text="")
    l.pack()
    s = Button(root, text="Submit",
               command=lambda: stage_2(root, "t", b['text']))
    s.pack()
    b.configure(command=lambda: torrent_file(b))
    root.mainloop()

with open("config.json") as json_file:
    json = json.load(json_file)

if len(sys.argv) >= 2:
    if "magnet" in str(sys.argv[1]):
        root = Tk()
        stage_2(root, "m", str(sys.argv[1]))
        root.mainloop()
        sys.exit()


root = Tk()
root.title("Torrent selector")
root.iconbitmap("icon.ico")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))


torrent_image = Image.open("torrent.png")
torrent_img = ImageTk.PhotoImage(torrent_image.resize((50, 50)))
torrent_image = Label(root, image=torrent_img)
torrent_image.bind("<Button-1>", lambda a: torrent(root))
torrent_image.grid(row=0, sticky=W)

torrent_name = Label(root, text="Torrent File")
torrent_name.bind("<Button-1>", lambda a: torrent(root))
torrent_name.grid(row=0, column=1)

magnet_image = Image.open("magnet.png")
magnet_img = ImageTk.PhotoImage(magnet_image.resize((50, 50)))
magnet_image = Label(root, image=magnet_img)
magnet_image.bind("<Button-1>", lambda a: magnet_input(root))
magnet_image.grid(row=1, sticky=W)

magnet_name = Label(root, text="Magnet Link")
magnet_name.bind("<Button-1>", lambda a: magnet_input(root))
magnet_name.grid(row=1, column=1)

root.mainloop()
