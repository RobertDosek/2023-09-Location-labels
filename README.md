# Location Label Printing Tool

This Python script serves as a tool for generating location labels with QR codes. Developed using the Tkinter GUI library, the script facilitates the creation of labels for different formats and purposes.

## Features:

### QR Code Generation:
- Utilizes the `qrcode` library to generate QR codes containing location data.

### Label Formats:
#### Zebra Labels:
- 2 x A7 on A6
- 1 x A7 on A7
#### Ricoh Labels:
- 1 x A4 on A4
#### Store Shelf Labels:
- Designed for shelf placement in a store
#### Upper Shelf Labels:
- Custom format for upper shelves

### Font Handling:
- Registers custom fonts (`calibri.ttf` and `calibrib.ttf`) for label text.

### DPI Awareness:
- Ensures compatibility with high-DPI displays on Windows.
### CSV Data Loading:
- Reads location data from a CSV file (`locations.csv`).
### GUI Interface:
- Implements a user-friendly interface using Tkinter, allowing users to select label formats and initiate the printing process.
### Result Output:
- Outputs generated labels as a PDF file (`tisk_lokaci.pdf`) in a specified output folder.

## Dependencies:

- `labels`: A library for defining label formats.
- `tkinter`: GUI library for creating the user interface.
- `qrcode`: Library for generating QR codes.
- `reportlab`: Used for PDF generation.
- Azure `ttk` theme for a more modern look.

## Using the Application:

1. **Graphical User Interface (GUI):**
   - The Tkinter-based GUI will open, featuring the application's main interface.

2. **Format Selection:**
   - Use the dropdown menu to select the desired label format. Options include Zebra labels (2 x A7 on A6, 1 x A7 on A7), Ricoh labels (1 x A4 on A4), store shelf labels, and custom upper shelf labels.

3. **Initiate Printing:**
   - Click the "Tisknout" (Print) button to start the label generation process.

4. **Output Display:**
   - The generated labels will be saved as a PDF file named `tisk_lokaci.pdf` in the specified output folder (`vystup` by default).

5. **View Labels:**
   - The tool will attempt to open the generated PDF automatically in the default PDF reader. If not, locate the PDF file in the output folder and open it using a PDF viewer.

