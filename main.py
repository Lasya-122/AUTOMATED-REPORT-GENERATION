import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

def read_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="latin1")
        print("CSV loaded. Columns:", df.columns.tolist())
        return df
    except:
        print("Error reading file")
        return None

def analyze_data(df):
    summary = df[["SALES", "QUANTITYORDERED"]].describe()
    grouped = df.groupby("TERRITORY")[["SALES", "QUANTITYORDERED"]].sum()
    return summary, grouped

def create_plot(df):
    grouped = df.groupby("TERRITORY")["SALES"].sum()
    plt.figure(figsize=(8, 5))
    plt.bar(grouped.index, grouped.values)
    plt.title("Sales by Territory")
    plt.xlabel("Territory")
    plt.ylabel("Sales")
    plt.savefig("sales_plot.png")
    plt.close()

def create_pdf(summary, grouped):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sales Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Summary:", ln=True)
    pdf.multi_cell(0, 10, str(summary))
    pdf.ln(10)
    pdf.cell(200, 10, txt="Sales by Territory:", ln=True)
    pdf.multi_cell(0, 10, str(grouped))
    pdf.ln(10)
    pdf.cell(200, 10, txt="Plot:", ln=True)
    pdf.image("sales_plot.png", x=10, w=180)
    pdf.output("report.pdf")
    print("PDF saved as report.pdf")

df = read_data("sales_data_sample.csv")
if df is not None:
    summary, grouped = analyze_data(df)
    create_plot(df)
    create_pdf(summary, grouped)