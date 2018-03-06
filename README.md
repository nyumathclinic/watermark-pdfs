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

    $ pip install PyYaml
    $ pip install pdf
    $ pip install pyPDF
    $ pip install Reportlab
    $ pip install nameparser
    
## Script

Download the python script.  Or, you can clone the full github repository.

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
