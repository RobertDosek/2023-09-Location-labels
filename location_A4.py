# Original code for printing only A4

import labels
import os.path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics import shapes
import csv
import qrcode


specs = labels.Specification(297, 210, 1, 1, 297, 210, corner_radius=1)

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
    label.add(shapes.String(width / 2.0, height - 140, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=150))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    # label.add(shapes.Image(width / 2.0 - 180, height - 550, 360, 360, qr_image))
    label.add(shapes.Image(width / 2.0 - 220, height - 600, 450, 450, qr_image))


# Load location data from a CSV file
location_list = []
with open('locations.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        location_list.append(row[0])

sheet = labels.Sheet(specs, write_qr_code, border=False)

for pos in location_list:
    sheet.add_label(pos)

sheet.save('tisk_A4.pdf')
