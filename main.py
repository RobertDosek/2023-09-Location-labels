import labels
import tkinter as tk
from tkinter import ttk
import os
import csv
import qrcode
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics import shapes
import tkinter.messagebox as messagebox
import time


# Constants for result name and folder paths
RESULT_NAME = "tisk_lokaci"
INPUT_FOLDER = r"C:\Users\burimex.skladexpedic\Desktop\Tisk_stitku\vstup"
OUTPUT_FOLDER = r"C:\Users\burimex.skladexpedic\Desktop\Tisk_stitku\vystup"
# OUTPUT_FOLDER = "results"

base_path = os.path.dirname(__file__)

# Register fonts used in the PDFs
registerFont(TTFont("Calibri", os.path.join(base_path, "ad_fonts", "calibri.ttf")))
registerFont(TTFont("Calibri_bold", os.path.join(base_path, "ad_fonts", "calibrib.ttf")))


# Set DPI awareness for Windows
def dpi_awareness():
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


# Load location data from a CSV file
def load_locations():
    locations = []
    csv_file_path = os.path.join(INPUT_FOLDER, 'locations.csv')

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            locations.append(row[0])
        return locations


# Function to handle the print button click event
def on_print_button_click():
    option = selected_format.get()
    if option == "2 x A7 na A6 (Zebra)":
        specs = labels.Specification(152, 98, 2, 1, 73, 98, corner_radius=0, left_margin=6)
        sheet = labels.Sheet(specs, write_qr_a7, border=False)
    elif option == "1 x A7 na A7 (Zebra)":
        specs = labels.Specification(76, 102, 1, 1, 76, 102, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a7, border=False)
    elif option == "1 x A4 na A4 (Ricoh)":
        specs = labels.Specification(297, 210, 1, 1, 297, 210, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_a4, border=False)
    elif option == "Na regál na prodejně":
        specs = labels.Specification(210, 297, 3, 8, 64, 34, corner_radius=0)
        sheet = labels.Sheet(specs, write_qr_shelf, border=False)
    else:
        specs = labels.Specification(57, 32, 1, 1, 57, 32, corner_radius=0)
        sheet = labels.Sheet(specs, write_upper_shelf, border=False)

    location_list = load_locations()

    for pos in location_list:
        sheet.add_label(pos)

    result_file = os.path.join(OUTPUT_FOLDER, f'{RESULT_NAME}.pdf')

    sheet.save(result_file)

    if os.path.exists(result_file):
        os.system(f'start {result_file}')
        time.sleep(1)
        messagebox.showinfo("Info:", "Štítky k tisku vygenerovány!")
    else:
        messagebox.showinfo("Chyba:", "Štítky k tisku se nepodařilo vygenerovat!")


# Generate labels for A7 format
def write_qr_a7(label, width, height, data):
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
        down_arrow_path = os.path.join(base_path, "pictures", "arrow_down_circle.png")
        down_arrow_image = shapes.Image(width / 2.0 - 20, height - 145, 40, 40, down_arrow_path)
        label.add(down_arrow_image)

    # Up arrow when xxxxBx location
    elif location[-2] == "B":
        up_arrow_path = os.path.join(base_path, "pictures", "arrow_up_circle.png")
        up_arrow_image = shapes.Image(width / 2.0 - 20, height - 145, 40, 40, up_arrow_path)
        label.add(up_arrow_image)


# Generate labels for A4 format
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


# Generate labels for shop shelf
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


# Generate labels for store upper shelf
def write_upper_shelf(label, width, height, data):
    location = data

    # Add the position text
    label.add(shapes.String(width / 2.0, height - 78, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=100))


# Initialize DPI awareness for high-DPI displays
dpi_awareness()

# Create GUI
root = tk.Tk()
root.title("Tisk lokací - Svět Karavanů")
root.geometry("350x250")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon_path = os.path.join(base_path, 'pictures', 'logo_svet_karavanu_01.png')
icon = tk.PhotoImage(file=icon_path)
root.wm_iconphoto(False, icon)

# Style from external theme (Azure theme)
style = ttk.Style(root)

# Set the theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

print_decision_label = ttk.Label(root, text="Vyber, co chceš tisknout:", font=("-size", 11, "-weight", "bold"))
print_decision_label.pack(padx=20, pady=(30, 15))

options = ["", "2 x A7 na A6 (Zebra)", "1 x A7 na A7 (Zebra)", "1 x A4 na A4 (Ricoh)", "Na regál na prodejně",
           "Tisk horních polic"]
selected_format = tk.StringVar()
selected_format.set(options[1])

option_menu = ttk.OptionMenu(root, selected_format, *options)
option_menu.pack(padx=100)

# # Wrapper frame for showing and hiding manual input of products (not used yet)
# wrapper_frame = ttk.Frame(root)
# wrapper_frame.pack(padx=10, pady=5)

print_button = ttk.Button(root, text="Tisknout", command=on_print_button_click)
print_button.pack(pady=50)

root.mainloop()
