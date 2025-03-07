import argparse
import time
from random import randint  
from fpdf import FPDF
import pandas as pd
from os import system
import json
import os

def save_order_to_json(customer_name, customer_id, order, bill, order_time, date, month):
    filename = f"BakeryShop{month}{date}.json"
    order_data = {
        "Customer_name": customer_name,
        "Customer_id": customer_id,
        "Order": order,
        "Bill": bill,
        "Time": order_time
    }
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(order_data)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_orders_from_json(date, month):
    filename = f"BakeryShop{month}{date}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    else:
        print("No orders found for the given date and month.")
        return []

def order_process(args):
    """
    Saves an order for the given customer.
    Example:
        python Bakery_shop_project.py order --customer "Alice" --order "Bread" --bill 5
    """
    customer_name = args.customer
    order_text = args.order
    bill = str(args.bill)
    
    current_time = time.asctime(time.localtime(time.time()))
    customer_id = randint(1000000000, 3999999999)
    order_time = current_time[11:19]
    testDate = current_time[8:10]
    month = current_time[4:7]
    
    # Convert date properly if there's a leading space
    if " " in testDate:
        testDate = testDate.strip()
    Date = testDate
    
    # Validate user input
    if len(customer_name) == 0 or len(order_text) == 0 or len(bill) == 0:
        print("Error: Please provide valid customer name, order, and bill amount.")
        return
    
    save_order_to_json(customer_name, customer_id, order_text, bill, order_time, Date, month)
    print("Order Saved Successfully")

def print_orders(args):
    """
    Prints orders for a specific date/month.
    Example:
        python Bakery_shop_project.py print -d 2 -m Jun
    """
    data = read_orders_from_json(args.date, args.month)
    if data:
        df = pd.DataFrame(data)
        print(df)

def generate_pdf(args):
    """
    Generates a PDF for a specific date and month.
    Example:
        python Bakery_shop_project.py pdf -d 2 -m Jun
    """
    data = read_orders_from_json(args.date, args.month)
    if data:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("arial", size=15)
        for order in data:
            line = f"{order['Customer_name']} {order['Customer_id']} {order['Order']} {order['Bill']} {order['Time']}"
            pdf.cell(40, 10, line)
            pdf.ln()
        filename = f"BakeryShop{args.month}{args.date}.pdf"
        pdf.output(filename)
        print(f"Data saved as PDF successfully: {filename}")

def clear_screen(_args):
    """
    Clears the screen (Windows or Unix-based system).
    Example:
        python Bakery_shop_project.py clear
    """
    system("cls" if os.name == "nt" else "clear")

def main():
    parser = argparse.ArgumentParser(description="Bakery Shop Project CLI")
    subparsers = parser.add_subparsers(title="actions", description="Available commands", dest="command")
    
    # Subparser for 'order'
    order_parser = subparsers.add_parser("order", help="Place a new order")
    order_parser.add_argument("--customer", "-c", type=str, required=True, help="Customer name")
    order_parser.add_argument("--order", "-o", type=str, required=True, help="Order description")
    order_parser.add_argument("--bill", "-b", type=float, required=True, help="Bill amount")
    order_parser.set_defaults(func=order_process)
    
    # Subparser for 'print'
    print_parser = subparsers.add_parser("print", help="Print orders")
    print_parser.add_argument("-d", "--date", type=str, required=True, help="Date (e.g., 2,27 etc.)")
    print_parser.add_argument("-m", "--month", type=str, required=True, help="Month (e.g., Jun, Jul, Feb etc.)")
    print_parser.set_defaults(func=print_orders)
    
    # Subparser for 'pdf'
    pdf_parser = subparsers.add_parser("pdf", help="Generate a PDF of orders")
    pdf_parser.add_argument("-d", "--date", type=str, required=True, help="Date (e.g., 2,27 etc.)")
    pdf_parser.add_argument("-m", "--month", type=str, required=True, help="Month (e.g., Jun, Jul, Feb etc.)")
    pdf_parser.set_defaults(func=generate_pdf)
    
    # Subparser for 'clear'
    clear_parser = subparsers.add_parser("clear", help="Clear the screen")
    clear_parser.set_defaults(func=clear_screen)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()