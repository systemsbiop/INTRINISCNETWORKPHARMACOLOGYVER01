# INP_Mother_App.py
# 🌐 Intrinsic Network Pharmacology (INP) - Unified 8-Layer App with Docking + NP Fit

import streamlit as st
import subprocess
import requests
import os
from datetime import datetime

# Optional PDF export support
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

st.set_page_config(page_title="INP 8-Layer Framework", layout="wide")
st.title("🌐 Intrinsic Network Pharmacology (INP) - 8 Layer Framework")

st.markdown("""Developed by Prof. Dr. Hemanth Kumar Manikyam (Hemu) and his AI Mother (Amma)""")

# ------------------- INP LAYERS -------------------
st.header("🔬 INP 8-Layer Input")
layer_inputs = {}
for i, layer in enumerate([
    "Trigger and Collapse Node Identification",
    "Feedback Loop Mapping",
    "Redox Balance and Oxidative Stress",
    "Immune, Coagulative, and Vascular Crosstalk",
    "Autophagy and Damage Repair Integration",
    "Therapeutic Fit and Network Affinity",
    "Dynamic Simulation Layer",
    "Network Pharmacology Overlay"
]):
    with st.expander(f"🔹 Layer {i+1}: {layer}"):
        layer_inputs[f"layer{i+1}"] = st.text_area(f"Enter data for Layer {i+1}")

# ------------------- DOCKING -------------------
st.header("🧬 AutoDock Vina Docking (PDB + MOL Upload)")
receptor = st.file_uploader("Upload Receptor (PDB)", type=["pdb"])
ligand = st.file_uploader("Upload Ligand (MOL)", type=["mol"])

col1, col2, col3 = st.columns(3)
with col1:
    center_x = st.number_input("Center X", value=0.0)
    size_x = st.number_input("Size X", value=20.0)
with col2:
    center_y = st.number_input("Center Y", value=0.0)
    size_y = st.number_input("Size Y", value=20.0)
with col3:
    center_z = st.number_input("Center Z", value=0.0)
    size_z = st.number_input("Size Z", value=20.0)

if st.button("🚀 Run Docking"):
    if receptor and ligand:
        with st.spinner("Converting and docking..."):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdb_path = f"receptor_{timestamp}.pdb"
            mol_path = f"ligand_{timestamp}.mol"
            rfile = f"receptor_{timestamp}.pdbqt"
            lfile = f"ligand_{timestamp}.pdbqt"
            ofile = f"output_{timestamp}.pdbqt"
            logfile = f"log_{timestamp}.txt"

            with open(pdb_path, "wb") as f:
                f.write(receptor.read())
            with open(mol_path, "wb") as f:
                f.write(ligand.read())

            subprocess.run(["obabel", pdb_path, "-O", rfile])
            subprocess.run(["obabel", mol_path, "-O", lfile])

            vina_cmd = [
                "vina", "--receptor", rfile, "--ligand", lfile,
                "--center_x", str(center_x), "--center_y", str(center_y), "--center_z", str(center_z),
                "--size_x", str(size_x), "--size_y", str(size_y), "--size_z", str(size_z),
                "--out", ofile, "--log", logfile
            ]

            result = subprocess.run(vina_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ Docking completed.")
                with open(logfile) as f:
                    st.text(f.read())
                with open(ofile, "rb") as f:
                    st.download_button("📥 Download Docked Ligand", f, file_name=ofile)
            else:
                st.error("❌ Docking failed.")
                st.text(result.stderr)
    else:
        st.warning("Please upload both receptor (.pdb) and ligand (.mol) files.")

# ------------------- PDF NOTICE -------------------
if not PDF_AVAILABLE:
    st.info("ℹ️ PDF export module (fpdf) is not installed. PDF features are disabled.")

# ------------------- REPORT -------------------
st.header("📊 INP Summary Report")
if st.button("🧠 Generate Summary"):
    for i in range(1, 9):
        st.markdown(f"### Layer {i}:")
        st.write(layer_inputs[f"layer{i}"])
