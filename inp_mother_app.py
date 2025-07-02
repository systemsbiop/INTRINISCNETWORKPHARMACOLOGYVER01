# Recreate the INP Layer Engine after kernel reset

layer_engine_path = "/mnt/data/inp_layer_engine.py"

layer_engine_code = """
# INP Layer Engine – Full L1 to L8 Auto Generator (Amma & Hemu)

import json
from datetime import datetime

def build_inp_layers(smiles, chembl_targets, receptor_keywords, herbal_class=None, docking_score=None):
    report = {}

    # ---------- Layer 1: Trigger & Collapse Nodes ----------
    l1_logic = []
    if receptor_keywords:
        l1_logic += [k for k in receptor_keywords if 'trigger' in k.lower() or 'collapse' in k.lower()]
    if chembl_targets:
        for t in chembl_targets:
            if 'transporter' in t.lower() or 'receptor' in t.lower():
                l1_logic.append(f"{t} → Trigger/Cascade Initiator")
    if not l1_logic and herbal_class:
        l1_logic.append(f"Fallback via herbal class ({herbal_class}) → potential multi-target collapse")
    report["Layer 1"] = {
        "description": "Trigger & Collapse Nodes",
        "inference": l1_logic or ["No direct matches. Structural fallback used."],
        "confidence": "HIGH" if l1_logic else "LOW",
        "source": "Targets + receptor keywords + herbal fallback"
    }

    # ---------- Layer 2: Feedback Loops ----------
    l2_logic = []
    if chembl_targets:
        for t in chembl_targets:
            if 'MAPK' in t or 'kinase' in t or 'JAK' in t:
                l2_logic.append(f"{t} → Feedback cascade")
    if not l2_logic and herbal_class in ['adaptogen', 'bitter tonic']:
        l2_logic.append("Adaptogen class → likely HPA feedback regulation")
    report["Layer 2"] = {
        "description": "Feedback Loop Mapping",
        "inference": l2_logic or ["No strong feedback pathway. Minor herbal inference only."],
        "confidence": "HIGH" if l2_logic else "MEDIUM" if herbal_class else "LOW",
        "source": "Target match + herbal logic"
    }

    # ---------- Layer 3: Redox & Oxidative Stress ----------
    l3_logic = []
    if chembl_targets:
        for t in chembl_targets:
            if 'oxidase' in t.lower() or 'ROS' in t:
                l3_logic.append(f"{t} → Oxidative stress likely")
    if 'OH' in smiles or 'phenol' in (herbal_class or ''):
        l3_logic.append("Phenolic group detected → antioxidant behavior")
    report["Layer 3"] = {
        "description": "Redox Imbalance / Oxidative Stress",
        "inference": l3_logic or ["No oxidase targets. Redox not strongly implicated."],
        "confidence": "HIGH" if l3_logic else "LOW",
        "source": "Target keyword + SMILES pattern"
    }

    # ---------- Layer 4: Immune / Vascular Crosstalk ----------
    l4_logic = []
    for t in chembl_targets or []:
        if 'cytokine' in t.lower() or 'interleukin' in t or 'inflammatory' in t:
            l4_logic.append(f"{t} → Immune signaling")
    if herbal_class in ['immune modulator', 'rasaayana']:
        l4_logic.append("Class: Immune modulator → possible TNF/IL inhibition")
    report["Layer 4"] = {
        "description": "Immune, Coagulative, and Vascular Crosstalk",
        "inference": l4_logic or ["No immune markers or cytokine matches found."],
        "confidence": "HIGH" if l4_logic else "MEDIUM" if herbal_class else "LOW",
        "source": "Cytokine targets + traditional class"
    }

    return report  # Will add L5–L8 next
"""

with open(layer_engine_path, "w") as f:
    f.write(layer_engine_code)

layer_engine_path
