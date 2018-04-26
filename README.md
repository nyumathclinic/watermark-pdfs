Sort and watermark PDFs exported by GradeScope

# Installation

Clone this github repository to your machine.

## Python virtual environment

Use the [`pipenv`](https://docs.pipenv.org/#install-pipenv-today) command to manage a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).

On macOS with MacPorts:

    $ sudo port install pipenv

On macOS with HomeBrew:

    $ sudo brew install pipenv

On generic Unix, [install pip](https://pip.pypa.io/en/stable/installing/) if not installed and use:

    $ pip install pipenv

Then, within this project directory, run:

    $ pipenv install .

## Helper packages

The `pipenv install` command above should import the packages below into the virtual environment automatically:

  * PyYaml 
  * pdf
  * pyPDF
  * ReportLab
  * nameparser
    
## Script

The `pipenv install` command above will also install an executable module called `watermarkGradeScopeExport.py`.  This is normally what you would run.

# Usage

Within the project folder, run:

$ pipenv shell

This will activate the virtual environment.  You'll get a message such as:

    Spawning environment shell (/bin/bash). Use 'exit' to leave.
    bash-3.2$ . /Users/matthew/.local/share/virtualenvs/watermark-pdfs-bOgaLKHv/bin/activate
    (watermark-pdfs-bOgaLKHv) bash-3.2$

From now on, until you run `exit`, the script `watermarkGradeScopeExport.py` is in scope.  

You will need to download submissions from a (presumably graded) Gradescope assignment.  

1. Go to the assignment and click "Review Grades" on the left menu column.
2. Look for the "Export Submissions" button in the bottom toolbar.
3. It takes some time, so you'll get a "please wait..." screen.  Once it's finished, you'll get a download link on the webpage, and through email.
4. Download the `submissions.zip` file.
5. Unzip it into some working directory.  You should see a directory called `assignment_nnnnn_export`, with a bunch of PDFs and a YAML (`.yml`) file.  

Change into that directory and run `watermarkGradeScopeExport.py`.  If all goes well, you'll get a directory for each student, with their watermarked PDF therein.

If you'd rather not use the pipenv shell, you can run the script out of its
vitual environment directory.  This requires some extra typing and tabbing:

    $ /Users/matthew/.local/share/virtualenvs/watermark-pdfs-bOgaLKHv/bin/watermarkGradeScopeExport.py

(Use the directory indicated the first time you run `pipenv shell`)  You can
also do fancy things like

    * make a shell alias to that long file path
    * make a symbolic link from one of the directories in `$PATH` to the
      virtual environment, or
    * add the virtual environment's `bin` directory to your `$PATH` 
      environment variable in your `.login` or `.profile` or similar
      file


