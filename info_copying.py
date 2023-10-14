from pypdf import PdfReader
import os
import re
import pandas as pd


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
        sub_total = re.search(r"I.V.A.:\s+(.+)\s", text).group().split("\n")[1].replace(" ", "")
        
        preparado = re.search(r"PREPARADO", text)
        
        if preparado is not None:
            s = [f"{cliente} (PREPARADO)", f"FACT- {nota}", fecha, sub_total]
            sdf.append(s)
            continue
        
        s = [cliente, f"FACT- {nota}", fecha, sub_total]
        sdf.append(s)

    sdf = sorted(sdf, key=lambda f: f[1])

    d = pd.DataFrame(data=sdf, columns="Cliente,Nota,Emision,Monto".split(","))

    d.to_excel("/home/raed/Desktop/automate/some.xlsx", sheet_name="page", engine="openpyxl")


if __name__ == "__main__":
    organizer()