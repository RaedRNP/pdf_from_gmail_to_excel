import os

os.chdir('./Download')

def deleting():
    if os.listdir('./Download') is not []:
        files = [f for f in os.listdir('./Download')
                 if os.path.isfile(f)]
        for f in files:
            if "PROFORMA" in f:
                os.remove(f)
            
    print("Done")
    