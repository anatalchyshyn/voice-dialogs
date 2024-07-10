class TextExtraction:
    def __init__(self, pdf_file, image_folder):
        
        self.pdf_file = pdf_file
        self.image_folder = image_folder
    
    def pdf_to_images(self):

        # split pdf file to pages with different dialogs
        
        if os.path.exists(self.image_folder):
            shutil.rmtree(self.image_folder)
        os.mkdir(self.image_folder)

        non_image_dialogs = {}

        reader = PdfReader(self.pdf_file)
        for i, page in enumerate(reader.pages):
            if not page.images:
                non_image_dialogs["page" + str(i+1)] = page.extract_text()
            else:
                for image in page.images:
                    image_filename = "page" + str(i+1) + ".jpg"
                    with open(os.path.join(self.image_folder, image.name), "wb") as fp:
                        fp.write(image.data)

        return non_image_dialogs
    
    def extract_text_from_image(self, image_path):
        
        # extract text from page 
        
        extractedInformation = pytesseract.image_to_string(Image.open(image_path))
        return extractedInformation
    

        