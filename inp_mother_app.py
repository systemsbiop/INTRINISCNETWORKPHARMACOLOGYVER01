# INP Mother App – RDKit-Free Version (uses SMILES input)
import streamlit as st
import requests

st.set_page_config(page_title="INP Mother App – Simplified", layout="wide")
st.title("🌐 INP Mother App – Auto INP Layers (No RDKit)")

st.markdown("Developed by Prof. Dr. Hemanth Kumar Manikyam (Hemu) and his AI Mother (Amma)")

# ---------------------- Helper Functions ----------------------

def fetch_chembl_targets(smiles):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search.json?q={smiles}"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['page_meta']['total_count'] > 0:
        chembl_id = response.json()['molecules'][0]['molecule_chembl_id']
        act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?molecule_chembl_id={chembl_id}&limit=100"
        act_res = requests.get(act_url)
        if act_res.status_code == 200:
            targets = [a.get('target_pref_name', '') for a in act_res.json()['activities']]
            return chembl_id, list(set(t for t in targets if t))
    return None, []

def infer_layers_from_targets(targets):
    layer_map = {
        "oxidase": "Likely redox disruption (Layer 3)",
        "cytokine": "Immune involvement (Layer 4)",
        "kinase": "Therapeutic and signaling pathway (Layer 6)",
        "MAPK": "Feedback loop suspected (Layer 2)",
        "mTOR": "Autophagy/repair system likely impacted (Layer 5)",
        "inflammatory": "Immune and cytokine loop (Layer 4)"
    }
    layers = {f"layer{i+1}": "" for i in range(8)}
    layers["layer1"] = ", ".join(targets[:5])
    for t in targets:
        for keyword, message in layer_map.items():
            if keyword.lower() in t.lower():
                for k in layers:
                    if message not in layers[k]:
                        if message in k:
                            layers[k] += f"• {t} → {message}\n"
    return layers

def extract_receptor_keywords(pdb_bytes):
    lines = pdb_bytes.decode('utf-8').splitlines()
    title = ""
    keywords_found = []
    layer1_info = []
    layer2_info = []
    keyword_map = {
        "oxidase": "Redox collapse (Layer 1, 3)",
        "immune": "Immune loop (Layer 4)",
        "cytokine": "Immune cross-talk (Layer 4)",
        "kinase": "Feedback loop (Layer 2)",
        "receptor": "Trigger node (Layer 1)",
        "transporter": "Collapse gate (Layer 1)",
        "ligand": "Binding logic (Layer 2)",
        "MAPK": "Loop switch (Layer 2)",
        "JAK": "Immune signaling (Layer 4)",
        "GPCR": "Signal distortion (Layer 2)"
    }

    for line in lines:
        if line.startswith("TITLE"):
            title += line[10:].strip() + " "
    for keyword, message in keyword_map.items():
        if keyword.lower() in title.lower():
            keywords_found.append(f"{keyword} → {message}")
            if "Layer 1" in message:
                layer1_info.append(message)
            if "Layer 2" in message:
                layer2_info.append(message)
    return title.strip(), layer1_info, layer2_info, keywords_found

# ---------------------- User Inputs ----------------------

st.header("🔬 Input Section")

smiles = st.text_input("Paste Ligand SMILES String (e.g., CC(=O)Oc1ccccc1C(=O)O)")
receptor = st.file_uploader("Upload Receptor (PDB)", type=["pdb"])

# ---------------------- Process ----------------------

if receptor and smiles:
    receptor_title, l1_hints, l2_hints, all_keywords = extract_receptor_keywords(receptor.read())
    st.markdown(f"### 🧠 Receptor Title: `{receptor_title}`")
    if all_keywords:
        st.success("Receptor Functional Keywords:")
        for hint in all_keywords:
            st.markdown(f"- {hint}")

    chembl_id, targets = fetch_chembl_targets(smiles)
    if chembl_id:
        st.info(f"🧪 Ligand ChEMBL ID: `{chembl_id}`")
        inferred = infer_layers_from_targets(targets)

        inferred["layer1"] += "\n" + "\n".join(l1_hints)
        inferred["layer2"] += "\n" + "\n".join(l2_hints)

        st.header("🔬 Auto-Filled INP Layers (L1–L6)")
        for i in range(6):
            st.markdown(f"### 🔹 Layer {i+1}")
            st.code(inferred[f"layer{i+1}"] or "No data inferred.")
    else:
        st.error("No ChEMBL target match found for this SMILES.")
