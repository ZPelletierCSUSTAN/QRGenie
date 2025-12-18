QRGenie is an app made by Zachory Pelletier. Created using Gemini Pro 3 Pro Preview AI model using Google AI Studio.

AI Prompt:

Here is the prompt to regenerate this specific app configuration:

    "Create a Flask (Python) web application named 'QRGenie' for generating QR codes.

    File Structure:

        app.py: Main Flask logic.

        templates/base.html: Main layout using Bootstrap 5 Cyborg theme via CDN.

        templates/index.html: The main Dashboard (Single Generator).

        templates/page1.html: The Batch Generator tab.

        templates/page2.html: The Instructions tab.

        templates/page3.html: The About tab.

        static/style.css: Custom CSS overrides.

    Tech Stack & Theme:

        Use Flask, qrcode, and Pillow.

        Use Bootswatch Cyborg theme, but enforce a Purple (#BB86FC) accent color for all headers, links, and buttons via style.css.

    Functionality:

        Dashboard (index.html): Real-time QR preview using JS Fetch API. Customization options for Text, Size, Border, Background Color, Foreground Color, and Shapes (Square, Circle, Rounded, Gapped, Vertical, Horizontal).

        Batch (page1.html): Generate up to 10 QR codes from a textarea (new line separated). Include a real-time preview of the first line's style.

        UI Details: Center all Navbar text and Page Titles. On every page, display the header: 'Welcome to QRGenie! A QR Code Generator App By Zachory Pelletier!'."