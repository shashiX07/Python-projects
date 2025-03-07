import os
import random
import webbrowser
import io
import logging
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

import qrcode
try:
    import validators
    HAS_VALIDATORS = True
except ImportError:
    HAS_VALIDATORS = False
    print("Warning: validators module not found. URL validation disabled.")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='qrcode_generator.log'
)

class QRWidget(BoxLayout):
    """Main widget for QR code generation and display"""
    qr_image = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(QRWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 10
        
        # Left panel for controls
        control_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        
        # Data input
        data_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        data_layout.add_widget(Label(text='URL or Text:', size_hint=(1, 0.2)))
        self.data_input = TextInput(hint_text='Enter URL or text', multiline=False)
        self.data_input.bind(text=lambda instance, value: Clock.schedule_once(lambda dt: self.update_preview(), 0.5))
        data_layout.add_widget(self.data_input)
        control_panel.add_widget(data_layout)
        
        # Parameters for QR code
        params_layout = GridLayout(cols=2, size_hint=(1, 0.6))
        
        # QR Size slider
        params_layout.add_widget(Label(text='Size:'))
        size_box = BoxLayout(orientation='horizontal')
        self.size_slider = Slider(min=1, max=40, value=10, step=1)
        self.size_slider.bind(value=self.on_slider_change)
        self.size_label = Label(text='10')
        size_box.add_widget(self.size_slider)
        size_box.add_widget(self.size_label)
        params_layout.add_widget(size_box)
        
        # Border size slider
        params_layout.add_widget(Label(text='Border:'))
        border_box = BoxLayout(orientation='horizontal')
        self.border_slider = Slider(min=0, max=10, value=4, step=1)
        self.border_slider.bind(value=self.on_slider_change)
        self.border_label = Label(text='4')
        border_box.add_widget(self.border_slider)
        border_box.add_widget(self.border_label)
        params_layout.add_widget(border_box)
        
        # Error correction level
        params_layout.add_widget(Label(text='Error Correction:'))
        self.ec_spinner = Spinner(
            text='H',
            values=('L', 'M', 'Q', 'H'),
            size_hint=(1, None),
            height=44
        )
        self.ec_spinner.bind(text=lambda instance, value: self.update_preview())
        params_layout.add_widget(self.ec_spinner)
        
        # Fill color
        params_layout.add_widget(Label(text='Fill Color:'))
        self.fill_color_btn = Button(text='Black', background_color=(0, 0, 0, 1))
        self.fill_color_btn.bind(on_release=lambda x: self.show_color_picker('fill'))
        params_layout.add_widget(self.fill_color_btn)
        self.fill_color = (0, 0, 0, 1)  # Default black
        
        # Background color
        params_layout.add_widget(Label(text='Background:'))
        self.bg_color_btn = Button(text='White', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        self.bg_color_btn.bind(on_release=lambda x: self.show_color_picker('background'))
        params_layout.add_widget(self.bg_color_btn)
        self.bg_color = (1, 1, 1, 1)  # Default white
        
        control_panel.add_widget(params_layout)
        
        # Action Buttons
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        save_btn = Button(text='Save QR Code')
        save_btn.bind(on_press=self.save_qr_code)
        buttons_layout.add_widget(save_btn)
        control_panel.add_widget(buttons_layout)
        
        # Right panel for QR code preview
        preview_panel = BoxLayout(orientation='vertical', size_hint=(0.6, 1))
        preview_panel.add_widget(Label(text='QR Code Preview', size_hint=(1, 0.1)))
        
        # QR code image
        self.qr_image = Image(size_hint=(1, 0.9))
        preview_panel.add_widget(self.qr_image)
        
        # Add both panels to the main widget
        self.add_widget(control_panel)
        self.add_widget(preview_panel)
        
        # Initialize default QR code
        Clock.schedule_once(lambda dt: self.update_preview(), 0.5)
    
    def on_slider_change(self, instance, value):
        """Handle slider value changes"""
        if instance == self.size_slider:
            self.size_label.text = str(int(value))
        elif instance == self.border_slider:
            self.border_label.text = str(int(value))
        self.update_preview()
    
    def show_color_picker(self, color_type):
        """Display a color picker popup"""
        popup_layout = BoxLayout(orientation='vertical')
        color_picker = ColorPicker()
        
        if color_type == 'fill':
            color_picker.color = self.fill_color
        else:
            color_picker.color = self.bg_color
        
        popup_layout.add_widget(color_picker)
        
        button_layout = BoxLayout(size_hint=(1, 0.1))
        close_button = Button(text='Select Color')
        
        def on_select(instance):
            if color_type == 'fill':
                self.fill_color = color_picker.color
                self.fill_color_btn.background_color = color_picker.color
                self.fill_color_btn.text = self.rgb_to_hex(color_picker.color)
            else:
                self.bg_color = color_picker.color
                self.bg_color_btn.background_color = color_picker.color
                self.bg_color_btn.text = self.rgb_to_hex(color_picker.color)
            
            self.update_preview()
            popup.dismiss()
        
        close_button.bind(on_release=on_select)
        button_layout.add_widget(close_button)
        
        popup_layout.add_widget(button_layout)
        
        popup = Popup(title=f'Choose {color_type} color',
                     content=popup_layout,
                     size_hint=(0.9, 0.9))
        popup.open()
    
    def rgb_to_hex(self, rgba):
        """Convert RGB color to hex string"""
        r, g, b, a = rgba
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    
    def validate_url(self, url):
        """Validate if the input is a URL."""
        if HAS_VALIDATORS:
            return validators.url(url)
        # Simple validation if validators module is not available
        return url.startswith(('http://', 'https://'))
    
    def update_preview(self):
        """Generate and display QR code preview"""
        data = self.data_input.text
        if not data:
            data = "https://example.com"  # Default value for preview
        
        # Get parameters
        size = int(self.size_slider.value)
        border = int(self.border_slider.value)
        
        # Get error correction level
        ec_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction = ec_map.get(self.ec_spinner.text, qrcode.constants.ERROR_CORRECT_H)
        
        # Get colors
        fill_color = self.rgb_to_hex(self.fill_color)
        back_color = self.rgb_to_hex(self.bg_color)
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=size,
                error_correction=error_correction,
                box_size=10,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Convert PIL image to Kivy texture
            img_data = io.BytesIO()
            img.save(img_data, format='PNG')
            img_data.seek(0)
            
            # Create Kivy core image and texture
            im = CoreImage(io.BytesIO(img_data.read()), ext='png')
            texture = im.texture
            
            # Update the image widget
            self.qr_image.texture = texture
            self.qr_image.canvas.ask_update()
            
        except Exception as e:
            logging.error(f"Error generating QR code preview: {str(e)}")
            print(f"Error generating preview: {str(e)}")
    
    def save_qr_code(self, instance):
        """Save QR code to file"""
        data = self.data_input.text
        if not data:
            self.show_error("Please enter URL or text content")
            return
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        num = random.randint(1000, 9999)
        output_name = f"qrimg_{timestamp}_{num}.png"
        
        # Get parameters
        size = int(self.size_slider.value)
        border = int(self.border_slider.value)
        
        # Get error correction level
        ec_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction = ec_map.get(self.ec_spinner.text, qrcode.constants.ERROR_CORRECT_H)
        
        # Get colors
        fill_color = self.rgb_to_hex(self.fill_color)
        back_color = self.rgb_to_hex(self.bg_color)
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=size,
                error_correction=error_correction,
                box_size=10,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image and save
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            img.save(output_name)
            
            logging.info(f"QR code saved as: {output_name}")
            self.show_success(f"QR code saved as: {output_name}")
            
        except Exception as e:
            logging.error(f"Error saving QR code: {str(e)}")
            self.show_error(f"Error: {str(e)}")
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(title='Error',
                     content=Label(text=message),
                     size_hint=(0.8, 0.3))
        popup.open()
    
    def show_success(self, message):
        """Show success popup with option to open the file"""
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        
        button_layout = BoxLayout(size_hint=(1, 0.4), spacing=10, padding=10)
        
        open_button = Button(text="Open File")
        open_button.bind(on_press=lambda x: self.open_file(message.split(": ")[1]))
        
        close_button = Button(text="Close")
        close_button.bind(on_press=lambda x: popup.dismiss())
        
        button_layout.add_widget(open_button)
        button_layout.add_widget(close_button)
        content.add_widget(button_layout)
        
        popup = Popup(title='Success',
                     content=content,
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def open_file(self, filepath):
        """Open the generated file"""
        try:
            abs_path = os.path.abspath(filepath)
            webbrowser.open(f"file://{abs_path}")
        except Exception as e:
            self.show_error(f"Could not open file: {str(e)}")

class QRCodeGeneratorApp(App):
    """QR Code Generator Application"""
    def build(self):
        self.title = 'QR Code Generator'
        return QRWidget()

if __name__ == '__main__':
    QRCodeGeneratorApp().run()