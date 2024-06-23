class intToHexColor:
    def __init__(self):
        return None

    def convertInt(intValue100):
        intValue255 = int((intValue100*255)/100)
        newHex = hex(intValue255)
        if(len(newHex)==4):
            newStr = "#00"+newHex[2]+newHex[3]+"00"
        else:
            newStr = "#000"+newHex[2]+"00"

        return newStr
    
    
    


if __name__ == "__main__":
    print(intToHexColor.convertInt(75))