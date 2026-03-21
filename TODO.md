# TODO

The list of things that must be done in order for the project to be finished.

## Create Deployment Script

**Status: Not Started**

* Form
  * Bash script
  * To be executed on the server (git used to get latest/specific files)
* Function
  * Copy files necessary to run the web app into appropriate locations
  * Verify operation has succeeded for all files

## Sender identity

**Status: Completed**

### Initial Spec

* Form
  * Optional name field in the frontend
* Function
  * In leiu of a provided name shall be populated with:
    * "Anonymous" for theme memo
    * A randomly chosen poet from a list of poets for theme poem
    * "Pass it on" for theme note
    * "Secret Admirer" for future theme love letter
  * Until populated, the default sender text will be visible with 50% opacity in the text box
  * Provided or default name/identity will be placed below the note
  * Additionally, the IP address and device info of the sender should be printed on the final line

### Revision Two

* Random poet should be populated in the front end
* Text in the signature box should be left justified

### Revision Three

* Not enough women in poet list
* randomPoet called twice, resulting in different poet printed than shown

## Message Formatting

**Status: Not Started**

To be done in function `format_message` in `print_script.py`

Notes: 
* The printer can print 42 monospace characters per line
* The front end is configured to only allow 38 characters per line
* Check for maximum newlines should occur after message has been formatted

Feature:
* Format the printed message to look exactly like it does on the front end when user hits send.
  * 38 characters per line max
  * 2 leading spaces, 2 trailing spaces
  * Line breaks not in the middle of words (should appear at spaces)
* Sender field shall be right justified
* IP and OS info shall be center justified and bracketed by "~" characters for decoration
