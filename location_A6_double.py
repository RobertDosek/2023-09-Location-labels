# Original code for printing only two A7 on A6

import labels
import os.path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics import shapes
import csv
import qrcode

RESULT_NAME = "tisk_A6_double"
RESULT_FOLDER = "results"

specs = labels.Specification(150, 98, 2, 1, 75, 98, corner_radius=0)

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
    label.add(shapes.String(width / 2.0, height - 80, location, textAnchor="middle",
                            fontName="Calibri_bold", fontSize=55))

    # Create an image of the QR code and add it to the label
    qr_image = qr.make_image(fill_color="black", back_color="white")
    label.add(shapes.Image(width / 2.0 - 58, height - 270, 120, 120, qr_image))


# Load location data from a CSV file
def load_locations():
    locations = []
    with open('locations.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            locations.append(row[0])
        return locations


sheet = labels.Sheet(specs, write_qr_code, border=False)

location_list = load_locations()

for pos in location_list:
    sheet.add_label(pos)

result_file = f'{RESULT_FOLDER}/{RESULT_NAME}.pdf'

sheet.save(result_file)

if os.path.exists(result_file):
    os.system(f'start {result_file}')

