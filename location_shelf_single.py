# Original code for printing only single label on Zebra 57x32mm

import labels
import os.path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics import shapes
import csv
import qrcode

specs = labels.Specification(57, 32, 1, 1, 57, 32)

base_path = os.path.dirname(__file__)

registerFont(TTFont('Calibri', os.path.join(base_path, 'calibri.ttf')))
registerFont(TTFont('Calibri_bold', os.path.join(base_path, 'calibrib.ttf')))


def write_qr_code(label, width, height, data):
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
    label.add(shapes.String(width / 2.0+30, height-52, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=20))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    # label.add(shapes.Image(width / 2.0 - 180, height - 550, 360, 360, qr_image))
    label.add(shapes.Image(width / 2.0 - 74, height - 70, 50, 50, qr_image))


# Load location data from a CSV file
location_list = []
with open('locations.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        location_list.append(row[0])

sheet = labels.Sheet(specs, write_qr_code, border=True)

for pos in location_list:
    sheet.add_label(pos)

sheet.save('tisk_shelf_single.pdf')
