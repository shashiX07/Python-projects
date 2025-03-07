import time
from random import randint
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.spinner import Spinner
from kivy.metrics import dp

# Attempt to import FPDF, but provide a fallback if not available
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    print("Warning: fpdf module not found. PDF export will be disabled.")
    print("To enable PDF export, install fpdf: pip install fpdf")
    HAS_FPDF = False

# Set window size and color
Window.size = (900, 700)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

BAKERY_ITEMS = {
    "Bread": 2.50,
    "Croissant": 1.75,
    "Donut": 1.25,
    "Cake Slice": 3.50,
    "Muffin": 1.50,
    "Cupcake": 2.00,
    "Cookie": 1.00,
    "Brownie": 2.25,
    "Coffee": 2.50,
    "Tea": 1.75
}

def get_current_date_time():
    current_time = time.asctime(time.localtime(time.time()))
    date = current_time[8:10].strip()
    month = current_time[4:7]
    year = current_time[20:24]
    order_time = current_time[11:19]
    return date, month, year, order_time

def save_order_to_json(customer_name, customer_id, order_items, bill, order_time, date, month):
    filename = f"BakeryShop{month}{date}.json"
    order_data = {
        "Customer_name": customer_name,
        "Customer_id": customer_id,
        "Order_items": order_items,
        "Total_bill": bill,
        "Time": order_time,
        "Date": f"{date} {month}"
    }
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(order_data)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_orders_from_json(date, month):
    filename = f"BakeryShop{month}{date}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                return []
    else:
        return []

class OrderItem(BoxLayout):
    def __init__(self, item_name, price, **kwargs):
        super(OrderItem, self).__init__(orientation='horizontal', size_hint_y=None, height=dp(40), **kwargs)
        self.item_name = item_name
        self.price = price
        
        # Item name label
        self.name_label = Label(text=item_name, size_hint_x=0.5)
        self.add_widget(self.name_label)
        
        # Price label
        self.price_label = Label(text=f"${price:.2f}", size_hint_x=0.2)
        self.add_widget(self.price_label)
        
        # Quantity spinner (now starting with '0' by default and including '0' in values)
        self.quantity_spinner = Spinner(
            text='0',  # Default quantity to 0
            values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            size_hint_x=0.15
        )
        self.quantity_spinner.bind(text=self.update_total)
        self.add_widget(self.quantity_spinner)
        
        # Total price label
        self.total_label = Label(text=f"${0.00:.2f}", size_hint_x=0.15)
        self.add_widget(self.total_label)
    
    def update_total(self, instance, value):
        quantity = float(value)
        self.total_label.text = f"${quantity * self.price:.2f}"
    
    def get_total(self):
        return float(self.quantity_spinner.text) * self.price
    
    def get_item_info(self):
        return {
            "item": self.item_name,
            "quantity": int(self.quantity_spinner.text),
            "price": self.price,
            "total": self.get_total()
        }

class BakeryShopApp(App):
    def build(self):
        self.title = 'Bakery Shop Management'
        self.order_items = []
        
        # Main layout with tabs
        self.tabbed_panel = TabbedPanel(do_default_tab=False)
        
        # Order Tab
        order_tab = TabbedPanelItem(text='New Order')
        order_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header with logo
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        logo_layout = BoxLayout(size_hint_x=0.3)
        with logo_layout.canvas.before:
            Color(0.2, 0.3, 0.4)
            Rectangle(pos=logo_layout.pos, size=logo_layout.size)
        header.add_widget(logo_layout)
        
        title_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        title_layout.add_widget(Label(text='Sweet Delights Bakery', font_size=dp(24)))
        title_layout.add_widget(Label(text='Order Management System', font_size=dp(16)))
        header.add_widget(title_layout)
        
        order_layout.add_widget(header)
        
        # Customer Details
        customer_details = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.2)
        customer_details.add_widget(Label(text='Customer Name:', halign='right'))
        self.customer_name_input = TextInput(hint_text='Enter customer name', multiline=False)
        customer_details.add_widget(self.customer_name_input)
        
        customer_details.add_widget(Label(text='Phone Number:', halign='right'))
        self.phone_input = TextInput(hint_text='Enter phone number', multiline=False)
        customer_details.add_widget(self.phone_input)
        
        order_layout.add_widget(customer_details)
        
        # Menu Items Section
        order_layout.add_widget(Label(text='Menu Items', font_size=dp(18), size_hint_y=0.05))
        
        # Create scrollable menu
        menu_scroll = ScrollView(size_hint_y=0.4)
        self.menu_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.menu_layout.bind(minimum_height=self.menu_layout.setter('height'))
        
        # Add menu items
        for item, price in BAKERY_ITEMS.items():
            order_item = OrderItem(item, price)
            self.menu_layout.add_widget(order_item)
            self.order_items.append(order_item)
        
        menu_scroll.add_widget(self.menu_layout)
        order_layout.add_widget(menu_scroll)
        
        # Order Summary
        summary_box = BoxLayout(orientation='vertical', size_hint_y=0.2, padding=[0, dp(10)])
        summary_box.add_widget(Label(text='Order Summary', font_size=dp(18)))
        
        totals_grid = GridLayout(cols=2, spacing=dp(10))
        totals_grid.add_widget(Label(text='Total Items:'))
        self.total_items_label = Label(text='0')
        totals_grid.add_widget(self.total_items_label)
        
        totals_grid.add_widget(Label(text='Total Amount:'))
        self.total_amount_label = Label(text='$0.00')
        totals_grid.add_widget(self.total_amount_label)
        
        summary_box.add_widget(totals_grid)
        order_layout.add_widget(summary_box)
        
        # Action Buttons
        buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.1)
        calculate_button = Button(text='Calculate Total', background_color=(0.2, 0.6, 0.2, 1))
        calculate_button.bind(on_press=self.calculate_total)
        buttons_layout.add_widget(calculate_button)
        
        clear_button = Button(text='Clear Form', background_color=(0.8, 0.2, 0.2, 1))
        clear_button.bind(on_press=self.clear_form)
        buttons_layout.add_widget(clear_button)
        
        save_button = Button(text='Save Order', background_color=(0.2, 0.3, 0.8, 1))
        save_button.bind(on_press=self.save_order)
        buttons_layout.add_widget(save_button)
        
        order_layout.add_widget(buttons_layout)
        order_tab.add_widget(order_layout)
        
        # View Orders Tab
        view_tab = TabbedPanelItem(text='View Orders')
        view_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Date Selection
        date_selection = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.15)
        date_selection.add_widget(Label(text='Date:', halign='right'))
        self.date_input = TextInput(hint_text='e.g., 8', multiline=False)
        date_selection.add_widget(self.date_input)
        
        date_selection.add_widget(Label(text='Month:', halign='right'))
        self.month_input = Spinner(
            text='Select Month',
            values=('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        )
        date_selection.add_widget(self.month_input)
        
        view_layout.add_widget(date_selection)
        
        # Action Buttons for View Tab
        view_buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.1)
        fetch_button = Button(text='Fetch Orders', background_color=(0.2, 0.6, 0.2, 1))
        fetch_button.bind(on_press=self.fetch_orders)
        view_buttons.add_widget(fetch_button)
        
        if HAS_FPDF:
            pdf_button = Button(text='Save as PDF', background_color=(0.2, 0.3, 0.8, 1))
            pdf_button.bind(on_press=self.save_data_as_pdf)
            view_buttons.add_widget(pdf_button)
        
        view_layout.add_widget(view_buttons)
        
        # Orders Display
        view_layout.add_widget(Label(text='Order History', font_size=dp(18), size_hint_y=0.05))
        
        self.order_scroll = ScrollView(size_hint_y=0.7)
        self.orders_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.orders_layout.bind(minimum_height=self.orders_layout.setter('height'))
        self.order_scroll.add_widget(self.orders_layout)
        
        view_layout.add_widget(self.order_scroll)
        view_tab.add_widget(view_layout)
        
        # Add tabs to the panel
        self.tabbed_panel.add_widget(order_tab)
        self.tabbed_panel.add_widget(view_tab)
        
        return self.tabbed_panel

    def calculate_total(self, instance):
        total_items = 0
        total_amount = 0
        
        for order_item in self.order_items:
            quantity = int(order_item.quantity_spinner.text)
            if quantity > 0:
                total_items += quantity
                total_amount += order_item.get_total()
        
        self.total_items_label.text = str(total_items)
        self.total_amount_label.text = f"${total_amount:.2f}"
        
        return total_items, total_amount
    
    def clear_form(self, instance):
        self.customer_name_input.text = ""
        self.phone_input.text = ""
        for order_item in self.order_items:
            order_item.quantity_spinner.text = "1"
        self.total_items_label.text = "0"
        self.total_amount_label.text = "$0.00"
    
    def save_order(self, instance):
        customer_name = self.customer_name_input.text
        phone_number = self.phone_input.text
        
        if not customer_name or not phone_number:
            self.show_popup('Error', 'Please enter customer name and phone number')
            return
        
        total_items, total_amount = self.calculate_total(None)
        
        if total_items == 0:
            self.show_popup('Error', 'Please add at least one item to the order')
            return
        
        # Create detailed order information
        order_details = []
        for order_item in self.order_items:
            quantity = int(order_item.quantity_spinner.text)
            if quantity > 0:
                order_details.append(order_item.get_item_info())
        
        # Generate unique customer ID
        customer_id = f"CUST-{randint(1000, 9999)}"
        
        # Get current date and time
        date, month, year, order_time = get_current_date_time()
        
        # Save order to JSON
        save_order_to_json(
            customer_name, 
            customer_id, 
            order_details, 
            total_amount, 
            order_time, 
            date, 
            month
        )
        
        # Show success popup with receipt
        receipt_text = f"Customer: {customer_name}\n"
        receipt_text += f"Order ID: {customer_id}\n"
        receipt_text += f"Date: {date} {month} {year}\n"
        receipt_text += f"Time: {order_time}\n\n"
        receipt_text += "Items Ordered:\n"
        for item in order_details:
            receipt_text += f"• {item['item']} x{item['quantity']} - ${item['total']:.2f}\n"
        receipt_text += f"\nTotal: ${total_amount:.2f}"
        
        self.show_receipt(receipt_text)
        
        # Clear the form
        self.clear_form(None)
    
    def show_receipt(self, receipt_text):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        title_label = Label(text="Order Receipt", font_size=dp(18), size_hint_y=0.1)
        popup_layout.add_widget(title_label)
        
        receipt_scroll = ScrollView(size_hint_y=0.7)
        receipt_label = Label(text=receipt_text, text_size=(dp(400), None), halign='left', valign='top')
        receipt_scroll.add_widget(receipt_label)
        popup_layout.add_widget(receipt_scroll)
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.2)
        print_button = Button(text='Print Receipt')
        close_button = Button(text='Close')
        buttons_layout.add_widget(print_button)
        buttons_layout.add_widget(close_button)
        popup_layout.add_widget(buttons_layout)
        
        popup = Popup(title='Order Saved Successfully', content=popup_layout, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        print_button.bind(on_press=lambda x: self.print_receipt(receipt_text, popup))
        popup.open()
    
    def print_receipt(self, receipt_text, popup):
        # In a real application, this would connect to a printer
        # For now, just show a message
        info_popup = Popup(title='Print Receipt', 
                          content=Label(text='Printing functionality would be implemented here.\nReceipt would be sent to printer.'),
                          size_hint=(0.6, 0.3))
        info_popup.open()
    
    def fetch_orders(self, instance):
        date = self.date_input.text
        month = self.month_input.text
        
        if not date or month == 'Select Month':
            self.show_popup('Error', 'Please select a date and month')
            return
        
        data = read_orders_from_json(date, month)
        self.display_orders(data)
    
    def display_orders(self, orders):
        self.orders_layout.clear_widgets()
        
        if not orders:
            no_orders = Label(text='No orders found for the selected date', size_hint_y=None, height=dp(40))
            self.orders_layout.add_widget(no_orders)
            return
        
        for order in orders:
            # Create order display
            order_box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5), 
                                size_hint_y=None, height=dp(200))
            with order_box.canvas.before:
                Color(0.95, 0.95, 0.95)
                Rectangle(pos=order_box.pos, size=order_box.size)
            
            # Order header
            header = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            header.add_widget(Label(text=f"Customer: {order['Customer_name']}", size_hint_x=0.5))
            header.add_widget(Label(text=f"ID: {order['Customer_id']}", size_hint_x=0.3))
            header.add_widget(Label(text=f"Time: {order['Time']}", size_hint_x=0.2))
            order_box.add_widget(header)
            
            # Order items
            items_scroll = ScrollView(size_hint_y=0.6)
            items_layout = BoxLayout(orientation='vertical', size_hint_y=None)
            items_layout.bind(minimum_height=items_layout.setter('height'))
            
            if 'Order_items' in order and isinstance(order['Order_items'], list):
                for item in order['Order_items']:
                    item_text = f"{item['item']} x{item['quantity']} - ${item['total']:.2f}"
                    item_label = Label(text=item_text, size_hint_y=None, height=dp(30))
                    items_layout.add_widget(item_label)
            else:
                # For backward compatibility with older order formats
                items_layout.add_widget(Label(text=str(order.get('Order', 'Unknown')), size_hint_y=None, height=dp(30)))
            
            items_scroll.add_widget(items_layout)
            order_box.add_widget(items_scroll)
            
            # Order footer
            footer = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            footer.add_widget(Label(text=f"Total: ${order.get('Total_bill', order.get('Bill', '0.00'))}", size_hint_x=0.7))
            view_details = Button(text='View Details', size_hint_x=0.3)
            view_details.bind(on_press=lambda x, o=order: self.show_order_details(o))
            footer.add_widget(view_details)
            order_box.add_widget(footer)
            
            self.orders_layout.add_widget(order_box)
    
    def show_order_details(self, order):
        # Create a detailed view of the order
        order_text = f"Customer: {order['Customer_name']}\n"
        order_text += f"Order ID: {order['Customer_id']}\n"
        order_text += f"Date: {order.get('Date', 'Unknown')}\n"
        order_text += f"Time: {order['Time']}\n\n"
        
        # Show items if available in new format
        if 'Order_items' in order and isinstance(order['Order_items'], list):
            order_text += "Items Ordered:\n"
            for item in order['Order_items']:
                order_text += f"• {item['item']} x{item['quantity']} - ${item['total']:.2f}\n"
        else:
            # For backward compatibility
            order_text += f"Order: {order.get('Order', 'Unknown')}\n"
        
        order_text += f"\nTotal: ${order.get('Total_bill', order.get('Bill', '0.00'))}"
        
        self.show_popup('Order Details', order_text)
    
    def save_data_as_pdf(self, instance):
        if not HAS_FPDF:
            self.show_popup('Error', 'PDF export is not available. Please install the fpdf module.')
            return
        
        date = self.date_input.text
        month = self.month_input.text
        
        if not date or month == 'Select Month':
            self.show_popup('Error', 'Please select a date and month')
            return
        
        data = read_orders_from_json(date, month)
        
        if not data:
            self.show_popup('Error', 'No orders found for the selected date')
            return
        
        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"Sweet Delights Bakery - Orders for {date} {month}", 0, 1, 'C')
            
            # Date and time
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}", 0, 1, 'R')
            
            pdf.ln(5)
            
            # Table header
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Customer", 1, 0, 'C')
            pdf.cell(40, 10, "Order ID", 1, 0, 'C')
            pdf.cell(40, 10, "Time", 1, 0, 'C')
            pdf.cell(60, 10, "Total Amount", 1, 1, 'C')
            
            # Table data
            pdf.set_font("Arial", '', 10)
            for order in data:
                pdf.cell(50, 10, str(order['Customer_name']), 1, 0, 'L')
                pdf.cell(40, 10, str(order['Customer_id']), 1, 0, 'C')
                pdf.cell(40, 10, str(order['Time']), 1, 0, 'C')
                pdf.cell(60, 10, f"${order.get('Total_bill', order.get('Bill', '0.00'))}", 1, 1, 'R')
            
            # Summary
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"Total Orders: {len(data)}", 0, 1)
            
            # Calculate total revenue
            total_revenue = sum(float(order.get('Total_bill', order.get('Bill', 0))) for order in data)
            pdf.cell(0, 10, f"Total Revenue: ${total_revenue:.2f}", 0, 1)
            
            # Save the PDF
            filename = f"BakeryShop{month}{date}.pdf"
            pdf.output(filename)
            self.show_popup('Success', f'Data saved as PDF: {filename}')
            
        except Exception as e:
            self.show_popup('Error', f'Failed to generate PDF: {str(e)}')
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Scrollable message for long text
        scroll = ScrollView()
        message_label = Label(text=message, text_size=(dp(400), None), size_hint_y=None)
        message_label.bind(texture_size=message_label.setter('size'))
        scroll.add_widget(message_label)
        
        popup_layout.add_widget(scroll)
        
        close_button = Button(text='Close', size_hint=(1, 0.2))
        popup_layout.add_widget(close_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    BakeryShopApp().run()