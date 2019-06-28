Sort and watermark PDFs exported by GradeScope

# Installation

## Virtual environment

Use a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

    $ virtualenv ~/Library/virtualenvs/wsm
    
(you can call it whatever you want and place it wherever you want.)  Activate the virtual environment:

    $ source ~/Library/virtualenvs/wsm/bin/activate
    (wsm):$ which python
    /Users/matthew/Library/virtualenvs/wsm/bin/python
    
Now anything you do is in the virtual environment, and won't require root access or cluttering your user
python library.

## Helper packages

Someday: package the script with an installer that does this automatically.

    $ pip install PyYaml==3.12
    $ pip install pdf
    $ pip install pyPDF2
    $ pip install Reportlab
    $ pip install nameparser
    
## Script

Download the python script.  Or, you can clone the full github repository.

# Options

Near the top of the script, there are 4 variables/flags you can adjust: extension, watermark, sakai_assignment, and keep_grade_report.

`extension` is a string that will be appended to the resultant PDF file in the format: `netid+extension+".pdf"`. You can modify the file name further within the code.

If `watermark = 0`, no watermark will be applied. If `watermark = 1`, a watermark of the student's name will be applied to every page of the PDF. You can easily change the watermark text within the code.

If `sakai_assignment = 0`, then the submissions will be organized as: `./upload/netid/netid+extension.pdf`. If `sake_assignment = 1`, then the submissions will be organized as: `./upload/netid/Feedback Attachment(s)/netid_extension.pdf`. Use the former if transferring to Sakai using the WebDAV protocol. Use the latter if you are uploading the the assignments through Sakai's assignment portal. Alternatively, you can further customize the path within the code.

If `keep_grade_report = 0`, then the first page of the pdf will be purged, which is usually the GradeScope grade report. Keep in mind, if the grade report is more than one page long, only the first page will be purged. If `keep_grade_report = 1`, then the first page will not be purged.    

# Usage

You will need to download submissions from a (presumably graded) Gradescope assignment.  

1. Go to the assignment and click "Review Grades" on the left menu column.
2. Look for the "Export Submissions" button in the bottom toolbar.
3. It takes some time, so you'll get a "please wait..." screen.  Once it's finished, you'll get a download link on the webpage, and through email.
4. Download the `submissions.zip` file.
5. Unzip it into some working directory.  You should see a directory called `assignment_nnnnn_export`, with a bunch of PDFs and a `.yml` file.  

Change into that directory and run:

    $ python path/to/script 

If all goes well, you'll get a directory for each student, with their watermarked PDF therein.
