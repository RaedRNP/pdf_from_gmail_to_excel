import os

def deleting():
    #os.chdir('./Download')
    if os.listdir('.') is not []:
        files = [f for f in os.listdir('.')
                 if os.path.isfile(f)]
        for f in files:
            if "PROFORMA" in f:
                os.remove(f)
            
    print("---------- Empty folder ----------")
    
if __name__ == "__main__":
    deleting()