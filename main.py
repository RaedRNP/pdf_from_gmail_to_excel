from pdf_downloader import pdf_downloader_main
from info_copying import organizer
import os

def main():
    os.chdir("./Download")
    files = [f for f in os.listdir(".")
             if os.path.isfile(f)]
    for f in files:
        if "PROFORMA" in f:
            os.remove(f)
            
    print("Done")
    
if __name__ == "__main__":
    main()