"""need to install packages:
PyYaml
pyPDF2
Reportlab
nameparser
e.g. "pip install --user <package_name>"

To execute, export submissions from GradeScope, unzip folder.
Place script in directory with all sbumissions and submission_metadata.yml.
Adjust 
Exceute script; e.g. "python gradescope_Sakai.py".
A new folder called "upload" will be created with the organized submissions,
along with a grades.csv file.
You can transfer this folder via WebDAV to Sakai, or via Sakai Assignment portal.
"""

from PyPDF2 import PdfFileWriter, PdfFileReader 
from reportlab.pdfgen import canvas
from nameparser import HumanName
import yaml
import os
import re
import csv

"""These flags can be turned on or off depending on your preferences
"""
extension = "_exam1" # new pdf file will be named: netid+extension+".pdf"
watermark = 1 # if ture, will watermark student name to pdf; else it won't
sakai_assignment = 1 # if true, will structure for Sakai assignment upload; else Sakai file transfer
keep_grade_report = 1 # if true, keep the grade report; else purges ONLY THE FIRST PAGE* (*grade report may be 1+)



def update_PDF(pdf_file,new_name,path,watermark_text):
    """Receive a pdf_file, rename to new_name, store in path, and watermark with water_mark_text
    """
    
    # use reportlab to create a PDF that will be used 
    # as a watermark on another PDF.
    c= canvas.Canvas("watermark.pdf") # the watermark pdf
    c.setFont("Courier", 70) # watermark font/size
    c.setFillGray(0.3,0.3) # watermark color/transparency
    c.saveState() # save current canvas state
    c.translate(500,100) # position the canvas
    c.rotate(45) # rotate the canvas
    #c.drawCentredString(0, 0, watermark_text) # write text
    c.drawCentredString(0, 300, watermark_text)  # write text
    #c.drawCentredString(0, 600, watermark_text) # write text
    c.restoreState() # restore canvas state
    c.save()

    # initialize an output stream for the new, watermarked PDF
    output = PdfFileWriter()

    # read in the given PDF to memory that will have the watermark applied to it
    input1 = PdfFileReader(open(pdf_file, "rb")) 
    page_count = input1.getNumPages()
    
    # loop through every page of the given PDF file and watermark it
    for i in range(page_count):
        # skip the first page if keep_grade_report==0
        if(keep_grade_report==0):
            if(i==0):
                i=1
        page_i = input1.getPage(i) # open up the current page
        watermark = PdfFileReader(open("watermark.pdf", "rb")) # read in the watermark pdf to memory
        page_i.mergePage(watermark.getPage(0))# merge watermark pdf with page_i
        output.addPage(page_i) # add watermarked page_i to the output pdf

    # write the output of our new, watermarked PDF to the given given file name
    if not os.path.exists(path):
        os.makedirs(path)
    outputStream = open(path+new_name+".pdf", "wb") 
    output.write(outputStream) 
    outputStream.close()
    
def submitter_netid(email,sid):
    """Get the NetID of the submitter record.
    Sometimes we populate the Gradescope records by putting the NetID in the
    `sid` or Student ID field.  Other times we put the NYU N Number in the 
    `sid` field and NetID in the email address (with `@nyu.edu` appended).
    This function tries both.
    """
    netid_pattern = re.compile('[a-z]{1,4}[0-9]{1,5}')
    match = netid_pattern.search(sid)
    if match:
        return match.group(0)
    match = netid_pattern.search(email)
    if match:
        return match.group(0)
    raise ValueError("Could not find email address: %s" % submitter )


def name_last_first(name):
    """Takes a name and returns "Last, First Middle"
    """
    parsed_name = HumanName(name) # this is a smart parser that digests human names
    name = parsed_name.last+", "+parsed_name.first
    if(parsed_name.middle != ""):
        name = name+" "+parsed_name.middle
    return name


# initilaize a blank grades.csv file in the formate of Sakai assignments
if not os.path.exists("./upload/"):
    os.makedirs("./upload/")
with open('./upload/grades.csv','w') as fd:
    fd.write("\n\n")
with open('./upload/grades.csv', 'a', newline='') as csvfile:
    fieldnames = ['Display ID', 'ID', 'Last Name', 'First Name', 'grade', 'Submission date', 'Late submission']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# read GradeScope's YAML file in the current directory
submissions = yaml.load(open('submission_metadata.yml'))
"""Each item is the associated pdf file.
There is a 'submitters' entry with name, email, and sid.
There is also a 'score' entry with the grade.
"""

# go through each submission in the YAML file
for item in submissions:
    # only run the script for assignments with student names
    if(submissions[item][':submitters']!=None):
        pdf_file = item # pull the associated student pdf file name
        student_name = submissions[item][':submitters'][0][':name'] # pull student name
        email = submissions[item][':submitters'][0][':email'] # pull student eamil from GradeScope
        sid = submissions[item][':submitters'][0][':sid'] # pull student sid from GradeScope
        score = submissions[item][':score'] # pull student score
   
        student_name=name_last_first(student_name) # re-order the name string to "Last, First Middle"
        netid = submitter_netid(email,sid) # derive NYU NetID from either email or sid
        with open('./upload/grades.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'ID': netid, 'grade': score}) # write student score to grades.csv
   
        # this is the watermark text
        text_to_mark = ""
        if(watermark!=0):
            text_to_mark = student_name;
        
        # set the folder structure
        file_path = "./upload/"+netid+"/"
        if(sakai_assignment!=0):
            file_path = file_path+"Feedback Attachment(s)/"
            
        # send pdf to be renamed, watermarked, and stored in new directory
        update_PDF(pdf_file,netid+extension,file_path,text_to_mark)
