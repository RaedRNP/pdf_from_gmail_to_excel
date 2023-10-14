from pypdf import PdfReader
import os
import re
import pandas as pd

os.chdir('./Download')

def organizer():

    list_of_files = os.listdir()
    sdf = []

    for file in list_of_files:
        reader = PdfReader(file)
        page = reader.pages[0]
        text = page.extract_text()
        
        cliente = re.search(r"Cliente:\s+(.+)\s", text).group().split("\n")[0].split(":  ")[1].split(" (")[0]
        fecha = re.search(r"Factura:\s+(.+)\s", text).group().split("\n")[1]
        nota = re.search(r"Vendedor:\s+(.+)\s", text).group().split("\n")[1].replace(" ", "")
        sub_total = re.search(r"..........\s%\sI.V.A.:", text).group().split("\n")[0].replace(" ", "")
        
        preparado = re.search(r"PREPARADO", text)
        avena = re.search(r"AVENA", text)
        pila = re.search(r"PILA", text)
        
        if preparado is not None:
            s = [f"{cliente} (PREPARADO)", f"FACT- {nota}", fecha, sub_total]
            sdf.append(s)
            continue
        
        if avena is not None:
            s = [f"{cliente} (AVENA)", f"FACT- {nota}", fecha, sub_total]
            sdf.append(s)
            continue
        
        if pila is not None:
            s = [f"{cliente} (PILAS)", f"FACT- {nota}", fecha, sub_total]
            sdf.append(s)
            continue
        
        
        s = [cliente, f"FACT- {nota}", fecha, sub_total]
        sdf.append(s)

    sdf = sorted(sdf, key=lambda f: f[1])

    d = pd.DataFrame(data=sdf, columns="Cliente,Nota,Emision,Monto".split(","))

    d.to_excel("/home/raed/Desktop/automate/some.xlsx", sheet_name="page", engine="openpyxl")
