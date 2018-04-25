

import os

# GUI module
import tkinter as tk

# Path formating module
from pathlib import Path

# module for executing the node.js script
from subprocess import Popen

# Support module for displaying images in tkinter
from PIL import Image, ImageTk

# Module used to generate qr codes
import qrcode

# Imports the Data class.
from script.storage import Data

# Data class stores and manages URL and titles of websites visited by user.
appData = Data()


def prev(panel):
    """
    Description: acceses previous data element from appData and render output to the user.
    :param panel: referance to the label where to render the qrcode.
    :return None:
    """
    try:
        # Access previous entry from appData.
        prev_entry = appData.prev()

        # Generate the Qr code from URL entry.
        create_code(prev_entry[0])

        # Display Qr image to the user.
        renderQr(panel, img)

        # Display title of website to the user.
        labelText.set(prev_entry[1])

    except TypeError:
        pass


def next(panel):
    """
    Description: acceses next data element from appData and render output to the user.
        :param panel: referance to the label where to render the qrcode.
        :return None:
    """
    try:
        # Access next entry from appData.
        next_entry = appData.next()

        # Generate the Qr code from URL entry.
        create_code(next_entry[0])

        # Display Qr image to the user.
        renderQr(panel, img)

        # Display title of website to the user.
        labelText.set(next_entry[1])

    except TypeError:
        pass


def viewData():
    """
    Description: Print to the console all data in storage.
        :return None:
    """
    appData.viewData()


def getData():
    """
    Description: Read data from history.txt and return URL and Title of website.
        :return url, title:
    """
    path = Path("data/history.txt")

    file = open(path, mode='r')

    # get title from file.
    title = file.readline().rstrip("\n")

    # get url from file.
    url = file.readline().rstrip("\n")

    return url, title


def create_code(url):
    """
    Description: Encode a URL string into a PNG file.
        :param url:
        :return None:
    """
    if url is None:
        pass
    else:
        # QR code parameters for encoding output file.
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Pass in URL data in string format.
        qr.add_data(url)

        qr.make(fit=True)

        # create image binary
        img = qr.make_image(fill_color="black", back_color="white")

        path = Path("image/qr.png")

        # Save image binary to folder as PNG file
        img.save(path)


def renderQr(panel, img):
    """
    Description: Display the PNG encoded file in Tkinter
        :param panel:
        :param img:
        :return None:
    """
    path = Path("image/qr.png")

    # Display image on screen
    img = ImageTk.PhotoImage(Image.open(path))

    panel.configure(image=img)

    # keep a reference image object
    panel.image = img


def manageData(data):
    """
    Description: Accepts data from file and determines if valid data, stores new data in
    appData class and renders Qr code only if data added does not exist in appData.
        :param data: touple (Url,title)
        :return None:
    """
    # if data is empty do nothing.
    if data == ('', ''):
        pass
    else:
        # If data exists in appData do nothing
        if data in appData.storage:
            pass

        else:
            # add data to the appData
            appData.add(data)

            print("ENTRY ADDED:", data, "\n")

            create_code(data[0])

            renderQr(panel, img)

            labelText.set(data[1])


def terminateApp():
    """
    Description: Performs cleanupp operation on App exit.
        :Return None:
    """
    path = Path("data/history.txt")

    # clear the history.txt file of data
    open(path, 'w').close()

    # kill any existing running Javascript process.
    NODE_PROCCESS.kill()

    # terminate the Tkinter Gui
    window.destroy()

    print("APP TERMINATED")


def main():
    """
    Description: Main running process.

    """
    global NODE_PROCCESS

    # Creates the node procces to fetch Chrome history and store in history.txt
    NODE_PROCCESS = Popen(["node", "node/getHistory.js"])

    # Read data from history.txt
    data = getData()

    manageData(data)

    # main loop repeats main function every 3 seconds
    window.after(3000, main)


"""tKinter GUI Section"""


# Create main window.
window = tk.Tk()
window.title('QuickLink')
window.geometry(newGeometry="500x550")
window.resizable(width=False, height=False)

# root is your root window
window.protocol('WM_DELETE_WINDOW', terminateApp)

# Three frames for title, qr code, buttons.
head = tk.Frame(window)
head.pack(side="top")
top = tk.Frame(window)
top.pack()
bottom = tk.Frame(window)
bottom.pack(side="bottom")

# place text

text = "QuickLink will generate QR links as you browse the web"
labelText = tk.StringVar()
labelText.set(text)
labelDir = tk.Label(head, textvariable=labelText, height=2)
labelDir.pack(side="top")

# place image

path = Path("image/logo.png")
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image=img)
panel.configure(width="500", height="450", bg="white")
panel.image = img  # keep a reference
panel.pack(side="top", fill="both", expand="yes")

# place buttons

view_data_button = tk.Button(
    window,
    text="View Data",
    width=10,
    height=2,
    command=lambda: viewData())
view_data_button.pack(in_=bottom, side="left")

next_button = tk.Button(
    window,
    text="Next",
    width=10,
    height=2,
    command=lambda: next(panel))
next_button.pack(in_=bottom, side="left")

prev_button = tk.Button(
    window,
    text="Previous",
    width=10,
    height=2,
    command=lambda: prev(panel))
prev_button.pack(in_=bottom, side="right")


# initialize main process within main loop

main()

window.mainloop()
