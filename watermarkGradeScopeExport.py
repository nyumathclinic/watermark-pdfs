#need to install PyYaml, pyPDF, Reportlab.pdfgen, nameparser
from PyPDF2 import PdfFileWriter, PdfFileReader 
from reportlab.pdfgen import canvas
from nameparser import HumanName
import yaml
import os
import re

#this function takes a pdf file 'fileToMark' (location) and watermarks each page
#with the given string 'textToMark'; it also accepts an auxillary string 'sid'
#in its current implication, it writes the new pdf file to the folder ./sid/
def watermarkPDF(fileToMark,textToMark,sid):
    #Use reportlab to create a PDF that will be used 
    #as a watermark on another PDF.
    c= canvas.Canvas("watermark.pdf") 
    c.setFont("Courier", 70)
    #color
    c.setFillGray(0.3,0.3)
    #set up canvas
    c.saveState()
    #location
    c.translate(500,100)
    #rotation
    c.rotate(45) 
    #c.drawCentredString(0, 0, "A WATERMARK!") 
    c.drawCentredString(0, 300, textToMark) 
    #c.drawCentredString(0, 600, "A WATERMARK!") 
    c.restoreState() 
    c.save()

    #initialize an output stream for the new, watermarked PDF
    output = PdfFileWriter()

    #read in the given PDF that will have the watermark applied to it
    input1 = PdfFileReader(open(fileToMark, "rb")) 
    page_count = input1.getNumPages()

    #loop through every page of the given PDF file
    for i in range(page_count):
        #open up the current page
        page1 = input1.getPage(i)
        #read in the watermark pdf created above by reportlab for the watermark
        watermark = PdfFileReader(open("watermark.pdf", "rb"))
        #apply the watermark by merging the two PDF pages
        page1.mergePage(watermark.getPage(0))
        #send the resultant PDF to the output stream
        output.addPage(page1)

    #write the output of our new, watermarked PDF to the given
    #location with given filename
    if not os.path.exists("./"+sid+"/"):
        os.makedirs("./"+sid+"/")
    outputStream = open("./"+sid+"/"+sid+"EX1"+".pdf", "wb") 
    output.write(outputStream) 
    outputStream.close()

def submitter_netid(submitter):
    """Get the NetID of the submitter record.

    Sometimes we populate the Gradescope records by putting the NetID in the
    `sid` or Student ID field.  Other times we put the NYU N Number in the 
    `sid` field and NetID in the email address (with `@nyu.edu` appended).
    This function tries both.
    """
    netid_pattern = re.compile('[a-z]{1,4}[0-9]{1,5}')
    match = netid_pattern.search(submitter[':sid'])
    if match:
        return match.group(0)
    match = netid_pattern.search(submitter[':email'])
    if match:
        return match.group(0)
    raise ValueError("Could not find email address: %s" % submitter )

#read in the GradeScope metadata for all of the submissions
#as a python dictionary
submissions = yaml.load(open('submission_metadata.yml'))

#go through each submission in the YAML file
for item in submissions:
    submissioni = submissions[item] #filename of submission
    submissionii = submissioni[':submitters'] #dictionary for that specific submission
    studentName = submissionii[0][':name'] #student name for that submission
    sid = submissionii[0][':sid'] #studentID for that submission
    netid = submitter_netid(submissionii[0])
    #change studentName to "Last, First Middle" because GradeScope does "First Middle Last"
    temp = HumanName(studentName) #this is a smart parser
    studentName = temp.last+", "+temp.first
    #if they have a middle name, add it
    if(temp.middle != ""):
        studentName = studentName+" "+temp.middle

    #watermark that submission with their name
    watermarkPDF(item,studentName,netid)
