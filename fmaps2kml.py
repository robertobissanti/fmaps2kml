import os
import sys
import json
import tempfile
import shutil
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import random

def read_fmaps(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def json_to_kml(data):
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, 'Document')
    
    # Aggiunta dei marker come Placemark
    for marker in data['Markers']:
        placemark = ET.SubElement(document, 'Placemark')
        
        name = ET.SubElement(placemark, 'name')
        name.text = marker['Etichetta']
        
        description = ET.SubElement(placemark, 'description')
        description.text = marker['Denominazione']
        
        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = f"{marker['Coordinate']['lng']},{marker['Coordinate']['lat']}"
    
    # Aggiunta dei poligoni
    for feature in data.get('DrawnItems', {}).get('features', []):
        if feature['geometry']['type'] == 'Polygon':
            placemark = ET.SubElement(document, 'Placemark')
            
            style = ET.SubElement(placemark, 'Style')
            line_style = ET.SubElement(style, 'LineStyle')
            line_color = ET.SubElement(line_style, 'color')
            line_color.text = "ff" + random_color()[1:]  # KML uses aabbggrr format with aa for alpha
            line_width = ET.SubElement(line_style, 'width')
            line_width.text = "2"
            
            poly_style = ET.SubElement(style, 'PolyStyle')
            poly_color = ET.SubElement(poly_style, 'color')
            poly_color.text = "4c" + random_color()[1:]  # 4c is ~30% transparency in KML (hex)
            
            polygon = ET.SubElement(placemark, 'Polygon')
            outer_boundary_is = ET.SubElement(polygon, 'outerBoundaryIs')
            linear_ring = ET.SubElement(outer_boundary_is, 'LinearRing')
            coordinates = ET.SubElement(linear_ring, 'coordinates')
            
            coords = []
            for coord in feature['geometry']['coordinates'][0]:
                coords.append(f"{coord[0]},{coord[1]}")
            coordinates.text = ' '.join(coords)
    
    return ET.tostring(kml, encoding='utf-8', method='xml')

def save_kml(kml_content, output_path):
    with open(output_path, 'wb') as f:
        f.write(kml_content)

def select_fmaps_file():
    file_path = filedialog.askopenfilename(filetypes=[("FMAPS files", "*.fmaps")])
    if file_path:
        try:
            data = read_fmaps(file_path)
            print(f"Data read from file: {data}")  # Debugging line
            kml_content = json_to_kml(data)
            save_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
            if save_path:
                save_kml(kml_content, save_path)
                messagebox.showinfo("Success", f"File saved as {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def close_program():
    app.destroy()

def center_window(root, width=400, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Inizializzazione della finestra principale con ThemedTk
app = ThemedTk(theme="arc")
app.title("FMAPS to KML Converter")

# Centrare la finestra
center_window(app, 400, 200)

# Uso dei widget ttk per un aspetto più moderno
select_button = ttk.Button(app, text="Scegli il file fmaps", command=select_fmaps_file)
select_button.pack(pady=10)

close_button = ttk.Button(app, text="Chiudi", command=close_program)
close_button.pack(pady=10)

# Aggiungere una label in basso alla finestra
footer_label = ttk.Label(app, text="(c) 2024 Roberto Bissanti")
footer_label.pack(side=tk.BOTTOM, pady=5)

app.mainloop()