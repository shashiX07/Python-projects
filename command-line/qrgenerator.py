import qrcode
import argparse
import os
import random
import webbrowser
from PIL import Image
from datetime import datetime
import validators
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='qrcode_generator.log'
)

def validate_url(url):
    """Validate if the input is a URL."""
    if validators.url(url):
        return True
    return False

def generate_qr_code(data, 
                    output_name=None, 
                    size=10, 
                    border=4, 
                    fill_color="black", 
                    back_color="white", 
                    error_correction=qrcode.constants.ERROR_CORRECT_H):
    """
    Generate a QR code with customized parameters
    
    Parameters:
    - data: The URL or text to encode in the QR code
    - output_name: The filename for the saved QR code image
    - size: Size of the QR code (1-40)
    - border: Border size (quiet zone)
    - fill_color: Color of the QR code modules
    - back_color: Background color
    - error_correction: Error correction level
    
    Returns:
    - The filename of the saved QR code image
    """
    try:
        if output_name is None:
            num = random.randint(1000, 9999)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"qrimg_{timestamp}_{num}.png"
        elif not output_name.endswith(('.png', '.jpg', '.jpeg')):
            output_name += ".png"
            
        qr = qrcode.QRCode(
            version=size,
            error_correction=error_correction,
            box_size=10,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        img.save(output_name)
        logging.info(f"QR code generated successfully: {output_name}")
        
        return output_name
    except Exception as e:
        logging.error(f"Error generating QR code: {str(e)}")
        raise

def interactive_mode():
    """Run the QR code generator in interactive mode."""
    print("=" * 50)
    print("   QR Code Generator - Interactive Mode")
    print("=" * 50)

    while True:
        data = input("\nEnter the URL or text message: ")
        if data:
            break
        else:
            print("Input cannot be empty. Please try again.")

    if data.startswith(("http://", "https://")) and not validate_url(data):
        print("Warning: The URL you entered might not be valid.")
        proceed = input("Do you want to proceed anyway? (y/n): ").lower()
        if proceed != 'y':
            print("Operation cancelled.")
            return
    
    print("\nCustomization Options (press Enter for defaults):")
    
    output_name = input("Output filename (without extension): ")
    
    try:
        size_input = input("QR code size (1-40, default: 10): ")
        size = int(size_input) if size_input else 10
        if not 1 <= size <= 40:
            print("Invalid size. Using default (10).")
            size = 10
    except ValueError:
        print("Invalid input. Using default size (10).")
        size = 10
    
    try:
        border_input = input("Border size (default: 4): ")
        border = int(border_input) if border_input else 4
    except ValueError:
        print("Invalid input. Using default border (4).")
        border = 4
    
    fill_color = input("Fill color (default: black): ") or "black"
    back_color = input("Background color (default: white): ") or "white"
    
  
    error_correction_options = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M, 
        "Q": qrcode.constants.ERROR_CORRECT_Q,  
        "H": qrcode.constants.ERROR_CORRECT_H,  
    }
    
    print("Error correction levels:")
    print("L - Low (7% recovery)")
    print("M - Medium (15% recovery)")
    print("Q - Quartile (25% recovery)")
    print("H - High (30% recovery)")
    ec_input = input("Choose error correction level (L/M/Q/H, default: H): ").upper()
    
    error_correction = error_correction_options.get(ec_input, qrcode.constants.ERROR_CORRECT_H)
    
    try:
        output_file = generate_qr_code(
            data=data,
            output_name=output_name,
            size=size,
            border=border,
            fill_color=fill_color,
            back_color=back_color,
            error_correction=error_correction
        )
        
        print(f"\nQR Code generated successfully: {output_file}")
        
        if input("Would you like to open the QR code? (y/n): ").lower() == 'y':
            try:
                abs_path = os.path.abspath(output_file)
                webbrowser.open(f"file://{abs_path}")
            except Exception as e:
                print(f"Could not open the file: {str(e)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="QR Code Generator")
    
    parser.add_argument("-d", "--data", help="The URL or text to encode in the QR code")
    parser.add_argument("-o", "--output", help="Output filename (without extension)")
    parser.add_argument("-s", "--size", type=int, default=10, help="QR code size (1-40)")
    parser.add_argument("-b", "--border", type=int, default=4, help="Border size")
    parser.add_argument("-f", "--fill", default="black", help="Fill color")
    parser.add_argument("-bg", "--background", default="white", help="Background color")
    parser.add_argument("-e", "--error-correction", 
                        choices=["L", "M", "Q", "H"], 
                        default="H", 
                        help="Error correction level")
    parser.add_argument("--batch", help="Path to a text file with URLs/text to encode (one per line)")
    
    return parser.parse_args()

def main():
    """Main function to run the QR code generator."""
    args = parse_arguments()
    
    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                lines = f.readlines()
                
            print(f"Processing {len(lines)} QR codes in batch mode...")
            for i, line in enumerate(lines):
                data = line.strip()
                if data:
                    output_name = f"batch_qr_{i+1}.png"
                    generate_qr_code(
                        data=data,
                        output_name=output_name,
                        size=args.size,
                        border=args.border,
                        fill_color=args.fill,
                        back_color=args.background,
                        error_correction=ec_map[args.error_correction]
                    )
                    print(f"Generated: {output_name} - Data: {data[:30]}...")
            
            print("Batch processing completed!")
            return
                
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")
            return
    
    if args.data:
        try:
            output_file = generate_qr_code(
                data=args.data,
                output_name=args.output,
                size=args.size,
                border=args.border,
                fill_color=args.fill,
                back_color=args.background,
                error_correction=ec_map[args.error_correction]
            )
            print(f"QR Code generated successfully: {output_file}")
            return
        except Exception as e:
            print(f"Error: {str(e)}")
            return
    
    interactive_mode()

if __name__ == "__main__":
    main()