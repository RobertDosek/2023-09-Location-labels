import labels
import tkinter as tk
from tkinter import ttk
import os
import csv
import qrcode
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from reportlab.graphics import shapes
import tkinter.messagebox as messagebox
from dpi_awareness import dpi_awareness
from datetime import datetime
import time

dpi_awareness()

RESULT_NAME = "tisk_lokaci"
RESULT_FOLDER = "results"

base_path = os.path.dirname(__file__)
print(base_path)

registerFont(TTFont('Calibri', os.path.join(base_path, 'calibri.ttf')))
registerFont(TTFont('Calibri_bold', os.path.join(base_path, 'calibrib.ttf')))


def on_print_button_click():
    option = selected_format.get()
    if option == "1 x A6 na A6 - (Zebra)":
        specs = labels.Specification(148, 105, 1, 1, 148, 105, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a6_single, border=True)
    elif option == "2 x A7 na A6 (Zebra)":
        specs = labels.Specification(150, 98, 2, 1, 75, 98, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a7_double, border=True)
    elif option == "4 x A6 na A4 (Ricoh)":
        specs = labels.Specification(297, 210, 2, 2, 145, 100, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a6_multi, border=True)
    elif option == "1 x A4 na A4 (Ricoh)":
        specs = labels.Specification(297, 210, 1, 1, 297, 210, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a4, border=True)
    else:
        specs = labels.Specification(210, 297, 3, 8, 64, 34, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_shelf, border=True)

    location_list = load_locations()

    for pos in location_list:
        sheet.add_label(pos)

    result_file = f'{RESULT_FOLDER}/{RESULT_NAME}.pdf'

    sheet.save(result_file)

    if os.path.exists(result_file):
        os.system(f'start {result_file}')
        messagebox.showinfo("Info:", "Štítky k tisku vygenerovány!")
    else:
        messagebox.showinfo("Chyba:", "Štítky k tisku se nepodařilo vygenerovat!")


# Load location data from a CSV file
def load_locations():
    locations = []
    with open('locations.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            locations.append(row[0])
        return locations


def write_qr_a6_single(label, width, height, data):
    location = data
    print(location)
    print(location[-2])

    # Create a QR code with the location data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(location)
    qr.make(fit=True)

    # Add the position text
    label.add(shapes.String(width / 2.0, height - 90, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=100))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    label.add(shapes.Image(width / 2.0 - 80, height - 280, 160, 160, qr_image))


def write_qr_a7_double(label, width, height, data):
    location = data

    # Create a QR code with the location data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(location)
    qr.make(fit=True)

    # Add the position text
    label.add(shapes.String(width / 2.0, height - 80, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=55))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    label.add(shapes.Image(width / 2.0 - 60, height - 270, 120, 120, qr_image))

    # Down arrow when xxxxAx location
    if location[-2] == "A":
        down_arrow_path = os.path.join(base_path, 'arrow_down_circle.png')
        down_arrow_image = shapes.Image(width / 2.0 - 20, height - 145, 40, 40, down_arrow_path)
        label.add(down_arrow_image)

    # Up arrow when xxxxBx location
    elif location[-2] == "B":
        up_arrow_path = os.path.join(base_path, 'arrow_up_circle.png')
        up_arrow_image = shapes.Image(width / 2.0 - 20, height - 145, 40, 40, up_arrow_path)
        label.add(up_arrow_image)


def write_qr_a6_multi(label, width, height, data):
    location = data

    # Create a QR code with the location data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(location)
    qr.make(fit=True)

    # Add the position text
    label.add(shapes.String(width / 2.0, height - 90, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=100))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    label.add(shapes.Image(width / 2.0 - 80, height - 280, 160, 160, qr_image))


def write_qr_a4(label, width, height, data):
    location = data

    # Create a QR code with the location data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(location)
    qr.make(fit=True)

    # Add the position text
    label.add(shapes.String(width / 2.0, height - 180, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=150))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    # label.add(shapes.Image(width / 2.0 - 180, height - 550, 360, 360, qr_image))
    label.add(shapes.Image(width / 2.0 - 160, height - 550, 320, 320, qr_image))


def write_qr_shelf(label, width, height, data):
    location = data

    # Create a QR code with the location data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(location)
    qr.make(fit=True)

    # Add the position text
    label.add(shapes.String(width / 2.0 + 40, height - 56, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=26))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    label.add(shapes.Image(width / 2.0 - 90, height - 86, 80, 80, qr_image))


root = tk.Tk()
root.title("Tisk lokací - Svět Karavanů")
root.geometry("300x300")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Style from external theme (Azure theme)
style = ttk.Style(root)
# print(style.theme_names())
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# set the theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")


print_decision_label = ttk.Label(root, text="Vyber, co chceš tisknout?", font=("-size", 11, "-weight", "bold"))
print_decision_label.pack(padx=20, pady=(30, 15))


# radio buttons frame
print_option_frame = ttk.Frame(root)
print_option_frame.pack(padx=50)

options = ["", "1 x A6 na A6 - (Zebra)", "2 x A7 na A6 (Zebra)", "4 x A6 na A4 (Ricoh)", "1 x A4 na A4 (Ricoh)", "Na regál na prodejně"]
selected_format = tk.StringVar()
selected_format.set(options[1])

option_menu = ttk.OptionMenu(root, selected_format, *options)
option_menu.pack()

# Wrapper frame for showing and hiding manual input of products
wrapper_frame = ttk.Frame(root)
wrapper_frame.pack(padx=10, pady=5)

print_button = ttk.Button(root, text="Tisknout", command=on_print_button_click)
print_button.pack(pady=20)

root.mainloop()




