# -*- coding: utf-8 -*-
import suds
import base64

url="http://www.ocrwebservice.com/services/OCRWebService.asmx?WSDL"

def create_input_image(client, path, filename):
	input_image = client.factory.create("OCRWSInputImage")
	input_image.fileName=filename

	f = open(path + "/" + filename, "rb")
	input_image.fileData=base64.b64encode(f.read())
	f.close()

	return input_image

def create_settings(client):
	settings = client.factory.create("OCRWSSettings")
	settings.ocrLanguages = [ 'ENGLISH' ]
	settings.convertToBW = False
	settings.outputDocumentFormat = "DOC"
 	settings.createOutputDocument = True
	settings.getOCRText = True
 	settings.multiPageDoc = True
	settings.pageNumbers = "all pages"
	settings.ocrZones = []
	settings.ocrWords = False

	return settings

def read_textline_file(filename):
	f = open(filename, "r")
	contents = f.readline()
	f.close()

	return contents.replace("\n","")

def handle_response(path, response):
	if not hasattr(response, "errorMessage"): 
		f = open(path +"/" + response.fileName, "w")
		f.write(base64.b64decode(response.fileData))
		f.close()
		print response.fileName + " ready."
	else:
		print response.errorMessage

def main():
	global url

	client = suds.client.Client(url)

	license = read_textline_file(".license")
	user = read_textline_file(".user")
	input_image = create_input_image(client, "test" , "sample.pdf") 
	settings = create_settings(client)

	response=client.service.OCRWebServiceRecognize(user, license, input_image, settings)
	handle_response("output", response)	

if __name__ == "__main__":
	main()



