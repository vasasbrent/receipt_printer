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

**Status: Completed**

Notes: 
* To be done in function `format_message` in `print_script.py`
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

## Migrate Theme Colors to CSS Variables

**Status: Not Started**

* Currently theme background colors are set via `document.body.style.backgroundColor` in the JS switch statement in `script.js`
* Move theme color definitions to CSS custom properties (e.g. `--theme-bg-note`, `--theme-bg-poem`, etc.) in `style.css`
* JS should apply a theme class or data attribute to `body` instead of setting inline styles directly
* This allows other CSS rules (e.g. the helper dialog button) to derive colors from theme variables without JS involvement

## Helper Dialog

**Status: Specify**

**Note:** Depends on "Migrate Theme Colors to CSS Variables" — implement that first so the button and dialog can derive their colors from CSS theme variables.

* Clickable SVG question mark icon (`site/front/images/`, provided during implementation) which:
  * Is fixed to the top-right corner of the viewport
    * Size is a named CSS variable (e.g. `--help-btn-size`) for easy tuning
    * Should occupy a minimal percentage of the screen
  * Is present regardless of whether a theme is selected
  * Does not attract undue attention
    * Color matches the theme background at a different shade
      * Darker if the theme background is light, lighter if dark
      * When no theme is selected, background is white — use a light gray
  * Brings up a dialog which:
    * Is a stylized rectangular box anchored near the top of the screen
    * Centered horizontally, 90% viewport width, height is content-driven (no min-height)
    * Has an angular wedge (CSS triangle / clip-path) pointing toward the question mark button
    * Background color matches the question mark button color (same shade) — to be adjusted after review
    * Contains the text: "Pick a theme, write your message, and hit send! Your words will be magically teleported through the ether and printed on a receipt in my living room. Feel free to sign it or stay anonymous."
  * Dialog is dismissed by any keypress or any click/tap

## Feedback on Printer Status

**Status: Not Started**

Online status and paper roll fullness (if available)
They are available, this will be a fun one.

## Replace Dev Popup Messages

**Status: Not Started**

If something in the pipeline isn't working the user should just get a generic message.
