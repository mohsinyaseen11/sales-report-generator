#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[9]:





# In[ ]:





# In[ ]:





# In[11]:


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
def generate_report(file_path):

    data = pd.read_csv(file_path)
    data["Date"]=pd.to_datetime(data["Date"],errors="coerce")
    data = data.dropna(subset=["Date"])
    data["Product"]=data["Product"].replace(r'^\s*$',None,regex=True)
    data["Category"]=data["Category"].replace(r'^\s*$',None,regex=True)
    data["Quantity"]=pd.to_numeric(data["Quantity"],errors="coerce")
    data["Price"]=pd.to_numeric(data["Price"],errors="coerce")
    data=data.dropna(subset=["Product","Category","Quantity","Price"])
    data=data.dropna(subset=["Quantity"])
    data=data[data["Quantity"]>0]
    data=data.dropna(subset=["Price"])
    data=data[data["Price"]>0]
    data["City"]=data["City"].fillna("Unknown City")
    data=data.drop_duplicates()
    data["Product"] = data["Product"].str.strip().str.lower()
    data["City"] = data["City"].str.strip().str.title()
    data["Category"] = data["Category"].str.strip().str.title()
    data["Sales"] = data["Quantity"].astype(float) * data["Price"].astype(float)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    cleaned_file = f"cleaned_data_{timestamp}.csv"
    data.to_csv(cleaned_file, index=False)
    total_sales=data["Sales"].sum()
    print("Total Sales :",total_sales)
    total_transactions=len(data)
    print("Total Transactions :",total_transactions)
    average_order_value=total_sales/total_transactions
    print("Average Order Value :",average_order_value)
    total_quantity=data["Quantity"].sum()
    print("Total Quantity Sold :",total_quantity)
    Top_5_best_selling_products=data.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5)
    #print("Top 5 best-selling products\n",Top_5_best_selling_products)
    Bottom_5_least_selling_products=data.groupby("Product")["Quantity"].sum().sort_values(ascending=True).head(5)
    #print("Bottom 5 least-selling products\n",Bottom_5_least_selling_products)
    Product_wise_total_sales=data.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    #print("Product-wise total sales\n",Product_wise_total_sales)
    Category_wise_total_sales=data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    #print("Category-wise total sales\n",Category_wise_total_sales)
    Best_performing_category=data.groupby("Category")["Sales"].sum().idxmax()
    #print("Best performing category\n",Best_performing_category)
    daily_sales=data.groupby("Date")["Sales"].sum().sort_index()
    #print("Daily sales trend\n",daily_sales)
    monthly_sales=data.groupby(data["Date"].dt.to_period("M"))["Sales"].sum().sort_index()
    #print("Monthly sales summary\n",monthly_sales)
    City_wise_total_sales=data.groupby("City")["Sales"].sum().sort_values(ascending=False)
    #print("City-wise total sales\n",City_wise_total_sales)
    Top_performing_city=data.groupby("City")["Sales"].sum().idxmax()
    #print("Top performing city\n",Top_performing_city)

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet


    pdf_file = f"sales_report_{timestamp}.pdf"

    pdf = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Sales Report Summary", styles["Title"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Total Sales", styles["Heading2"]))
    content.append(Paragraph(f" {total_sales}", styles["Normal"]))
    content.append(Paragraph("Total Orders", styles["Heading2"]))
    content.append(Paragraph(f" {total_transactions}", styles["Normal"]))
    content.append(Paragraph("Average Order Value", styles["Heading2"]))
    content.append(Paragraph(f"{average_order_value}", styles["Normal"]))
    content.append(Paragraph("Top 5 Products", styles["Heading2"]))
    for product, qty in Top_5_best_selling_products.items():
        content.append(
            Paragraph(f"{product}: {qty}", styles["Normal"])
        )

    content.append(Paragraph("Worst 5 Products", styles["Heading2"]))

    for product, qty in Bottom_5_least_selling_products.items():
        content.append(
            Paragraph(f"{product}: {qty}", styles["Normal"])
        )
    content.append(Paragraph("Best Category", styles["Heading2"]))
    content.append(Paragraph(f" {Best_performing_category}", styles["Normal"]))
    content.append(Paragraph("City Performance", styles["Heading2"]))

    for city, sales in City_wise_total_sales.head(5).items():
        content.append(
            Paragraph(f"{city}: {sales}", styles["Normal"])
        )

    Top_5_best_selling_products.plot(kind="bar")
    plt.title("Top 5 Products")
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")
    plt.savefig("top_products.png", bbox_inches="tight")
    plt.close()
    daily_sales.plot(kind="line")
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.savefig("daily_sales.png", bbox_inches="tight")
    plt.close()
    content.append(Paragraph("Top Products Chart", styles["Heading2"]))
    content.append(Image("top_products.png", width=400, height=250))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Daily Sales Trend", styles["Heading2"]))
    content.append(Image("daily_sales.png", width=400, height=250))
    category_distribution=data.groupby("Category")["Sales"].sum()
    category_distribution.plot(kind="pie")
    plt.title("Category Distribution")
    plt.savefig("category_distribution.png", bbox_inches="tight")
    plt.close()
    content.append(Paragraph("Category Distribution", styles["Heading2"]))
    content.append(Image("category_distribution.png", width=400, height=300))
    pdf.build(content)



import tkinter as tk
from tkinter import filedialog, messagebox

def select_file():

    file_path = filedialog.askopenfilename(
        title="Select Sales CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        generate_report(file_path)

        messagebox.showinfo(
            "Success",
            "Report Generated Successfully!"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


root = tk.Tk()

root.title("Sales Report Generator")
root.geometry("400x200")

title = tk.Label(
    root,
    text="Sales Report Generator",
    font=("Arial", 14)
)
title.pack(pady=20)

btn = tk.Button(
    root,
    text="Select CSV File",
    command=select_file
)
btn.pack(pady=20)

root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:


SALES_REPORT_GENERATOR

