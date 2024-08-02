# Babylonian pandemonium
Babylonian pandemonium is an application that allows to work with hidden data: ciphers, metadata, stegonograms, etc. It's possible to encode and decode data.

## Ideas for implementation:
- Grand Prix cipher for grids from 2x2 to 36x36
- Caesar cipher with shift by ASCII table (symbols 33-126) and by alphabet
- Mathematical puzzle about remainders
- Modified DNA cipher (parser for decode and encode)

## _v.0.0.2_
## Features

- Menu Ciphers with submenus Encode and Decode (same functionality for now)
- Blank menu Steganography and Help (call F1)
- Creating a new tab when one of the Help menu Ciphers is invoked
- Start window for Caesar cipher
- Grand Prix and Caesar ciphers window with almost full functionality
  - Number of words/Shift input validation
  - Text with words for dictionary input validation
  - Re-encode plain text ability
- Quit with Esc, Fullscreen with F11
- Tabs closing button in window

## _v.0.0.3_
## Implementation plan

* [ ] Numbering of tabs with the same name (or naming in dialog window)
* [ ] Pop-up menu for left-clicking on text widget to save to file
* [ ] Add close button to tab
* [ ] Add ability to select modes to Caesar: alphabet and ASCII
* [ ] Messagebox for empty input of number of words/shift

