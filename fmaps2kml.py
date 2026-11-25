import os
import sys
import json
import xml.etree.ElementTree as ET
import random

def read_fmaps(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def to_kml_color(hex_color, alpha="ff"):
    """Convert a hex color ``#RRGGBB`` to the KML ``AABBGGRR`` format."""
    color = hex_color.lstrip('#')
    if len(color) != 6:
        raise ValueError("Invalid color format")
    r, g, b = color[0:2], color[2:4], color[4:6]
    return f"{alpha}{b}{g}{r}"

def json_to_kml(data):
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, 'Document')
    
    # Aggiunta dei marker come Placemark
    for marker in data.get('Markers', []):
        placemark = ET.SubElement(document, 'Placemark')
        
        name = ET.SubElement(placemark, 'name')
        name.text = str(marker.get('Etichetta', ''))
        
        description = ET.SubElement(placemark, 'description')
        description.text = str(marker.get('Denominazione', ''))
        
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
            line_color.text = to_kml_color(random_color(), "ff")  # KML uses aabbggrr format with aa for alpha
            line_width = ET.SubElement(line_style, 'width')
            line_width.text = "2"
            
            poly_style = ET.SubElement(style, 'PolyStyle')
            poly_color = ET.SubElement(poly_style, 'color')
            poly_color.text = to_kml_color(random_color(), "4c")  # 4c is ~30% transparency in KML (hex)
            
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


APP_TITLE = "FMAPS → KML"
APP_VERSION = "1.1.0"


def convert_file(input_path, output_path):
    """Convert an .fmaps file to KML. Returns (markers, polygons) counts."""
    data = read_fmaps(input_path)
    save_kml(json_to_kml(data), output_path)
    markers = len(data.get('Markers', []))
    polygons = sum(1 for f in data.get('DrawnItems', {}).get('features', [])
                   if f.get('geometry', {}).get('type') == 'Polygon')
    return markers, polygons


class App:
    def __init__(self, root):
        import tkinter as tk
        from tkinter import ttk
        self.tk, self.ttk = tk, ttk
        self.root = root
        root.title(APP_TITLE)
        root.minsize(520, 230)
        root.resizable(True, False)

        style = ttk.Style(root)
        if sys.platform.startswith('linux') and 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('Title.TLabel', font=('TkDefaultFont', 14, 'bold'))
        style.configure('Accent.TButton', padding=(14, 6))

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Seleziona un file .fmaps da convertire.")

        frm = ttk.Frame(root, padding=16)
        frm.pack(fill='both', expand=True)
        frm.columnconfigure(1, weight=1)

        ttk.Label(frm, text="Convertitore FMAPS → KML", style='Title.TLabel').grid(
            row=0, column=0, columnspan=3, sticky='w', pady=(0, 12))

        ttk.Label(frm, text="File fmaps:").grid(row=1, column=0, sticky='w', pady=4)
        ttk.Entry(frm, textvariable=self.input_var).grid(row=1, column=1, sticky='ew', padx=8)
        ttk.Button(frm, text="Sfoglia…", command=self.choose_input).grid(row=1, column=2)

        ttk.Label(frm, text="File KML:").grid(row=2, column=0, sticky='w', pady=4)
        ttk.Entry(frm, textvariable=self.output_var).grid(row=2, column=1, sticky='ew', padx=8)
        ttk.Button(frm, text="Sfoglia…", command=self.choose_output).grid(row=2, column=2)

        ttk.Separator(frm).grid(row=3, column=0, columnspan=3, sticky='ew', pady=12)

        ttk.Label(frm, textvariable=self.status_var, wraplength=480, foreground='#555').grid(
            row=4, column=0, columnspan=3, sticky='w')

        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=3, sticky='e', pady=(12, 0))
        ttk.Button(btns, text="Chiudi", command=root.destroy).pack(side='right')
        self.convert_btn = ttk.Button(btns, text="Converti", style='Accent.TButton',
                                      command=self.convert, state='disabled')
        self.convert_btn.pack(side='right', padx=(0, 8))

        ttk.Label(frm, text=f"v{APP_VERSION}  ·  © 2024 Roberto Bissanti",
                  foreground='#888').grid(row=6, column=0, columnspan=3, sticky='w', pady=(12, 0))

        self.input_var.trace_add('write', self._update_state)
        self.output_var.trace_add('write', self._update_state)
        root.bind('<Return>', lambda e: self.convert())
        root.bind('<Escape>', lambda e: root.destroy())
        self._center()

    def _center(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 3
        self.root.geometry(f"+{x}+{y}")

    def _update_state(self, *_):
        ok = self.input_var.get().strip() and self.output_var.get().strip()
        self.convert_btn.configure(state='normal' if ok else 'disabled')

    def choose_input(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Scegli il file fmaps",
            filetypes=[("File FMAPS", "*.fmaps"), ("JSON", "*.json"), ("Tutti i file", "*.*")])
        if path:
            self.input_var.set(path)
            self.output_var.set(os.path.splitext(path)[0] + ".kml")
            self.status_var.set("Pronto per la conversione.")

    def choose_output(self):
        from tkinter import filedialog
        cur = self.output_var.get()
        path = filedialog.asksaveasfilename(
            title="Salva KML come", defaultextension=".kml",
            initialdir=os.path.dirname(cur) or None,
            initialfile=os.path.basename(cur) or None,
            filetypes=[("File KML", "*.kml")])
        if path:
            self.output_var.set(path)

    def convert(self):
        from tkinter import messagebox
        src, dst = self.input_var.get().strip(), self.output_var.get().strip()
        if not (src and dst):
            return
        if not os.path.isfile(src):
            messagebox.showerror(APP_TITLE, f"File non trovato:\n{src}")
            return
        try:
            markers, polygons = convert_file(src, dst)
        except json.JSONDecodeError:
            messagebox.showerror(APP_TITLE, "Il file selezionato non è un file fmaps valido.")
            return
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Errore durante la conversione:\n{e}")
            return
        self.status_var.set(f"✔ Salvato {os.path.basename(dst)} — {markers} marker, {polygons} poligoni.")
        messagebox.showinfo(APP_TITLE, f"File salvato:\n{dst}\n\n{markers} marker, {polygons} poligoni.")


def main():
    # Uso da riga di comando: fmaps2kml input.fmaps [output.kml]
    if len(sys.argv) > 1:
        src = sys.argv[1]
        dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".kml"
        m, p = convert_file(src, dst)
        print(f"{dst}: {m} marker, {p} poligoni")
        return
    import tkinter as tk
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
