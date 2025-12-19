QRGenie is an app made by Zachory Pelletier. Created using Gemini 3 Pro Preview AI model using Google AI Studio.

QRGenie is a sophisticated, dark-themed Flask web application developed by Zachory Pelletier that features real-time single and batch QR code generation with advanced shape, border, and color customization options.

Design Theme:
Use Bootstrap 5 'Cyborg' theme but enforce a strict Purple (#BB86FC) and Black (#000000) color scheme via CSS overrides. Default Dark mode only.

File Mapping for QRGenie

QRGenie/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html       (Main Layout)
    ├── index.html      (Home / QR Generator)
    ├── page1.html      (Batch QR Generator)
    ├── page2.html      (Instructions)
    └── page3.html      (About)

Requirements:
Flask==3.0.3
gunicorn==23.0.0
python-dotenv==1.0.1
qrcode
Pillow

AI Prompt:

Project: Build a Flask (Python) web application called 'QRGenie'.

Design Theme:
Use Bootstrap 5 'Cyborg' theme but enforce a strict Purple (#BB86FC) and Black (#000000) color scheme via CSS overrides. No light mode option.

File Structure & Functionality:

    app.py: Main logic using Flask, qrcode, and Pillow (PIL) to process text into Base64 QR code images via API.

    templates/base.html: Base layout file containing the Purple-themed Navbar (centered links), Footer, and "Welcome to QRGenie! A QR Code Generator App By Zachory Pelletier!" header.

    templates/index.html: QR Code Generator (Home).
        Features real-time live preview using JS Fetch API.
        Customization options for Size, Border, Shape (Square, Rounded, Circle, Gapped, Vertical, Horizontal), Body Color, and Background Color.

    templates/page1.html: Batch QR Code Generator.
        Allows entering up to 10 lines of text.
        Features a 'Global Settings' bar (Size, Shape, Basic Color) with a button labeled 'Apply Settings To All' (purple text).
        Generates a grid of live previews.
        Background color forced to white for batch items.
        Allows individual deletion (Red 'X') and individual editing/downloading of QR codes.

    templates/page2.html: Instructions page explaining the 5-step process.

    templates/page3.html: About page crediting Zachory Pelletier and explaining the tech stack.

Specific Logic Implemented:

    Batch Constraints: Strict 10-line limit with error handling.
    
    Dynamic Editing: JavaScript logic to edit batch items individually or apply global settings to all.
    
    Shape Drawers: Uses qrcode.image.styles.moduledrawers to render specific shapes (Circles, Gapped, etc.).

    Theme: Strict CSS overrides for all Bootstrap components to ensure a high-contrast Black/Purple aesthetic.