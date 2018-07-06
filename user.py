try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

#Comenta la siguiente linea si tienes tesseract dentro del PATH, si no especifica la direccion al ejecutable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

class Usuario:
    def __init__(self):
        self.name = "test"
        self.team = "none"
        self.friend_code = "0"
        self.verified = False
    
    def SetName(self,name):
        self.name = name
    def SetTeam(self,team):
        self.team = team
    def SetCode(self,code):
        self.friend_code = code
    def Verify_Name(self,image):
        OCR = pytesseract.image_to_string(Image.open(image))
        if self.name in OCR:
            self.verified = True
            return True
        else:
            return False

    def Verify_Code(self,image):
        OCR = pytesseract.image_to_string(Image.open(image))
        first = self.friend_code[0]
        pos = 0

        for position, item in enumerate(OCR):
            if item == first:
                pos = position
        
        code ="".join(OCR[pos:(pos+15)])

        print(code)

        if self.friend_code in OCR:
            return True
        else:
            for i in OCR:
                print(i)
            return False
