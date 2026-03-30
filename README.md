# XML UUID & Total Extractor

> 🌐 Streamlit App: [https://billing-info-extractor.streamlit.app](https://billing-info-extractor.streamlit.app)

---

## Overview

This project provides a simple and efficient web-based tool to extract key information from CFDI XML files. The application processes multiple XML files, retrieves the **UUID** and **Total** fields, and compiles the results into a downloadable CSV file.

Built with **Streamlit**, this tool is designed for quick batch processing of invoices without requiring local scripts or manual parsing.

---

## Features

- Upload multiple `.xml` CFDI files
- Automatic **alphabetical ordering** of files
- Extraction of:
  - `UUID` (TimbreFiscalDigital)
  - `Total` (Comprobante)
- Optional inclusion of **source filename**
- Interactive preview of results
- One-click **CSV download**

---

## Tech Stack

- **Python**
- **Streamlit**
- **xml.etree.ElementTree**
- **csv / io**

---

## Usage

1. Open the app
2. Upload one or more XML files
3. (Optional) Enable filename column
4. Preview extracted data
5. Download the generated CSV

---

## Installation (Local)

```bash
git clone https://github.com/bacaSantiago/billing-info-extractor.git
cd billing-info-extracto

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
