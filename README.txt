QRGenie is a app made by Zachory Pelletier. Created using Gemini Pro 3 Pro Preview AI model using Google AI Studio.

File Mapping for QRGenie
QRGenie/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── page1.html      (Main Generator)
    ├── page2.html      (Batch Generator)
    ├── page3.html      (Instructions)
    ├── page4.html      (About)
    └── page5.html      (Main Layout)
    
QRGenie AI prompt:
Build a Flask (Python) web application called 'QRGenie'.

Design Theme:
Use Bootstrap 5 'Cyborg' theme but enforce a strict Purple (#BB86FC) and Black (#000000) color scheme via CSS overrides. No light mode option.

File Structure:

    app.py: Main logic using flask, qrcode, and pillow to serve Base64 images via API.

    templates/page1.html: Main Generator (Single QR) - Allows Text, Size, Border, Shape, FG Color, BG Color editing.

    templates/page2.html: Batch Generator - Takes 10 lines of text. Features a 'Global Settings' bar (Size, Shape, Basic Color) with a button labeled 'Apply Settings To All' (purple text). Generates a grid of QR cards. Each card has a Red 'X' delete button and an 'Edit' button to change that specific QR's color/shape.

    templates/page3.html: Instructions page.

    templates/page4.html: About page.

    templates/page5.html: Base layout file containing the Navbar and Footer.

Specific Logic:

    Batch Generator must allow deleting generated items individually.

    Batch Generator must allow applying global settings to all existing items or editing items individually.

    Batch Generator background color for QR codes should be locked to White for scanability.

    Ensure Template filenames are strictly page1.html through page5.html.