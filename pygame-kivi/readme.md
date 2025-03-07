# Nano Games

A simple Kivy-based application featuring two mini-games:
1. Number Guessing Game  
2. Stone-Paper-Scissor

## Features
- Guess a random number and get hints on how high or low your guess is.
- Play Stone-Paper-Scissor and keep track of wins and losses.

## Requirements
- Python 3
- Kivy
- Optional: Buildozer (for packaging into an Android APK)

## Installation
1. Clone or download the repository.  
2. Install dependencies:  
   ```bash
   pip install kivy
   ```

## Additional Applications

### Bakery Shop Management
A Kivy-based application for managing a bakery shop, including order management and viewing order history.

#### Features
- Add customer details and order items.
- Calculate total items and amount.
- Save orders to JSON files.
- View order history by date.
- Export order history to PDF (requires `fpdf` module).

#### Requirements
- Python 3
- Kivy
- Optional: fpdf (for exporting to PDF)

#### Installation
1. Navigate to the `bakeryshop` folder.
2. Install dependencies:
   ```bash
   pip install kivy fpdf
   ```

### QR Code Generator
A Kivy-based application for generating and saving QR codes.

#### Features
- Input URL or text to generate QR code.
- Customize QR code size, border, error correction level, fill color, and background color.
- Preview QR code in real-time.
- Save generated QR code as PNG file.

#### Requirements
- Python 3
- Kivy
- qrcode
- Optional: validators (for URL validation)

#### Installation
1. Navigate to the `qrgenerator` folder.
2. Install dependencies:
   ```bash
   pip install kivy qrcode validators
   ```