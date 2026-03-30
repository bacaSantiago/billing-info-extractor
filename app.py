import io
import csv
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="XML UUID & Total Extractor", page_icon="📄", layout="centered")


def extract_uuid_and_total_from_xml_bytes(xml_bytes: bytes):
    """
    Extract UUID and Total from a CFDI XML file given as bytes.
    Returns a tuple: (uuid, total)
    """
    namespaces = {
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
    }

    root = ET.fromstring(xml_bytes)

    total = root.attrib.get("Total", "")

    timbre = root.find(".//tfd:TimbreFiscalDigital", namespaces)
    uuid = timbre.attrib.get("UUID", "") if timbre is not None else ""

    return uuid, total


def build_csv_string(rows):
    """
    Build CSV content as a string.
    """
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["UUID", "Total"])
    writer.writerows(rows)
    return output.getvalue()


def sort_uploaded_files_alphabetically(files):
    """
    Sort uploaded files alphabetically by filename.
    """
    return sorted(files, key=lambda f: f.name.lower())


st.title("XML UUID & Total Extractor")
st.write(
    "Upload one or more CFDI XML files, and the app will extract **UUID** and **Total** "
    "in alphabetical order and generate a CSV."
)
st.write("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload XML files",
    type=["xml"],
    accept_multiple_files=True
)

include_filename = st.checkbox("Include source filename column", value=False)

if uploaded_files:
    sorted_files = sort_uploaded_files_alphabetically(uploaded_files)

    rows = []
    errors = []

    for uploaded_file in sorted_files:
        try:
            xml_bytes = uploaded_file.read()
            uuid, total = extract_uuid_and_total_from_xml_bytes(xml_bytes)

            if include_filename:
                rows.append([uploaded_file.name, uuid, total])
            else:
                rows.append([uuid, total])

        except Exception as e:
            errors.append((uploaded_file.name, str(e)))

    st.subheader("Preview")

    if include_filename:
        st.dataframe(
            [{"Filename": r[0], "UUID": r[1], "Total": r[2]} for r in rows],
            use_container_width=True
        )
    else:
        st.dataframe(
            [{"UUID": r[0], "Total": r[1]} for r in rows],
            use_container_width=True
        )

    csv_output = io.StringIO()
    writer = csv.writer(csv_output, lineterminator="\n")

    if include_filename:
        writer.writerow(["Filename", "UUID", "Total"])
    else:
        writer.writerow(["UUID", "Total"])

    writer.writerows(rows)
    csv_content = csv_output.getvalue().encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_content,
        file_name="xml_uuid_total_output.csv",
        mime="text/csv"
    )

    if errors:
        st.warning(f"{len(errors)} file(s) could not be processed.")
        with st.expander("Show errors"):
            for filename, err in errors:
                st.write(f"**{filename}**: {err}")

else:
    st.info("Upload XML files to begin.")