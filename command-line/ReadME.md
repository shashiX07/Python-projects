# Command-Line Utilities

This folder contains Python-based command-line tools for a bakery ordering system and two mini-games:  
1. A Bakery CLI to place and manage orders (including PDF receipts).  
2. A Stone-Paper-Scissor game.  
3. A Number Guessing game.
4. QR Code Generator

## Features

### Bakery CLI
- **Order Management**: Place customized orders with customer details and bills.  
- **Data Storage**: JSON-based storage, making the data easily accessible for further processing.  
- **Printing Orders**: View existing orders for a specific date and month.  
- **PDF Generation**: Convert orders into PDF files for easy sharing and record-keeping.  
- **Clear Screen**: Quickly clear the console to maintain a clean interface.

### Mini-Games
1. **Stone-Paper-Scissor**  
   - Simple text-based game with quick interactive response.  
   - Randomized computer moves for variety.  

2. **Number Guessing**  
   - User-friendly approach, guesses a random number within a chosen range.  
   - Fun way to practice Python’s random and conditional logic.

### QR Code Generator (Command-Line)
- **Single QR Generation**: Generate a QR code from given text or URL with customizable parameters like size, border, fill color, background color, and error correction level.
- **Interactive Mode**: If no arguments are provided, the script will prompt you for data and parameters.
- **Batch Mode**: Create multiple QR codes by processing input from a text file (one line per QR code).
- **Error Correction Options**: Choose from L, M, Q, or H for various levels of error recovery.

## Setup
1. Install Python 3.x.  
2. Optionally create and activate a virtual environment.  
3. Run:
   ```bash
   pip install -r requirements.txt
   ```

## Bakery CLI
Use the script "bakery.py" for command-line operations:
- Place orders:  
  ```sh
  python bakery.py order --customer "Alice" --order "Bread" --bill 5
  ```  
- Print orders:  
  ```sh
  python bakery.py print -d 8 -m Mar
  ```  
- Generate a PDF:  
  ```sh
  python bakery.py pdf -d 8 -m Mar
  ```  
- Clear screen:  
  ```sh
  python bakery.py clear
  ```

## Games
Use the script "game.py" for interactive mini-games:
- Number Guessing:
  ```sh
  python game.py number_guessing
  ```
- Stone-Paper-Scissor:
  ```sh
  python game.py stone_paper_scissor
  ```


## QR Generator
Use the script "qrgenerator.py" for Generating QR-Code:
- Interactive Mode (if no arguments are provided, the script prompts for necessary input):
 ```sh
 python qrgenerator.py
 ```
 ```sh
 Direct Mode (generate a single QR code by providing all parameters):
 ```
 ```sh
 python qrgenerator.py --data "Hello World" --output "hello_qr" --size 10 --border 4 --fill "black" --background "white" --error-correction "H"
 ```

 # parameters
  ---data: The text or URL to encode
  --output: Output filename (without extension; .png will be appended if missing).
  --size: Size (version) of the QR code (valid values: 1-40).
  --border: Border thickness around the QR code.
  --fill: Fill color for the QR code modules.
  --background: Background color for the QR code.
  --error-correction: Error correction level (choose from L, M, Q, H).

- Batch Mode (generate multiple QR codes from a file, one per line):
```sh
python qrgenerator.py --batch input_list.txt
```


## License
Use and modify these scripts freely for practice or personal projects.
```