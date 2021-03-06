# -*- coding: utf-8 -*-
import os
import fnmatch
import suds
import base64
import time
import urllib2
import sys

url="http://www.ocrwebservice.com/services/OCRWebService.asmx?WSDL"

def create_input_image(client, path, filename):
	input_image = client.factory.create("OCRWSInputImage")
	input_image.fileName=filename

	f = open(path + "/" + filename, "rb")
	input_image.fileData=base64.b64encode(f.read())
	f.close()

	return input_image

def create_settings(client, language):
	settings = client.factory.create("OCRWSSettings")
	settings.ocrLanguages = [ language ]
	settings.convertToBW = False
	settings.outputDocumentFormat = "PDF"
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

def batch_process_loop(user_name, license_key, src_path, output_path):
	global url

	client = suds.client.Client(url)
	settings = create_settings(client, "FINNISH")

	
	while True:
		try:
			for filename in os.listdir(src_path):
    				if fnmatch.fnmatch(filename, '*.pdf'):
        				if not os.path.exists(output_path + "/" + os.path.splitext(filename)[0] + ".pdf"):
						input_image = create_input_image(client, src_path , filename) 
						response=client.service.OCRWebServiceRecognize(user_name, license_key, input_image, settings)
						handle_response(output_path, response)
			print "Sleeping..."	
			time.sleep(30)
		except urllib2.URLError as urlError:
			print urlError
			pass
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise

def main():
	license_key = read_textline_file(".license")
	user_name = read_textline_file(".user")

	batch_process_loop(user_name, license_key, "test", "output") 

if __name__ == "__main__":
	main()



