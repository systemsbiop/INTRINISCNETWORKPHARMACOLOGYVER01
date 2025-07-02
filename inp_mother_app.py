import json
from datetime import datetime

def build_inp_layers(smiles, chembl_targets, receptor_keywords, herbal_class=None, docking_score=None):
    report = {}

    # ---------- Layer 1 ----------
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

    # ---------- Layer 2 ----------
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

    # ---------- Layer 3 ----------
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

    # ---------- Layer 4 ----------
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

    # ---------- Layer 5 ----------
    l5_logic = []
    if chembl_targets:
        for t in chembl_targets:
            if 'mTOR' in t or 'AMPK' in t or 'repair' in t.lower():
                l5_logic.append(f"{t} → Autophagy/repair triggered")
    if herbal_class in ['rejuvenator', 'rasaayana', 'cellular tonic']:
        l5_logic.append("Traditional rejuvenator → may trigger mitophagy/autophagy")
    report["Layer 5"] = {
        "description": "Autophagy and Damage Repair Integration",
        "inference": l5_logic or ["No direct targets, but cellular repair not ruled out."],
        "confidence": "HIGH" if l5_logic else "MEDIUM" if herbal_class else "LOW",
        "source": "Target names + traditional knowledge"
    }

    # ---------- Layer 6 ----------
    l6_logic = []
    if chembl_targets:
        l6_logic.append(f"{len(chembl_targets)} known targets matched in ChEMBL")
    if docking_score is not None:
        l6_logic.append(f"Docking score = {docking_score} kcal/mol")
    if herbal_class:
        l6_logic.append(f"Herbal class: {herbal_class}")
    confidence = "HIGH" if docking_score and docking_score < -8 else "MEDIUM" if docking_score else "LOW"
    report["Layer 6"] = {
        "description": "Therapeutic Fit and Network Affinity",
        "inference": l6_logic or ["No docking or ChEMBL overlap found."],
        "confidence": confidence,
        "source": "ChEMBL targets + Docking + Herbal category"
    }

    # ---------- Layer 7 ----------
    l7_logic = [
        "Simulated pathway cascade from Layers 1–6",
        "If Layer 3+4 are HIGH → systemic inflammation predicted",
        "If Layer 5+6 are HIGH → probable network recovery"
    ]
    report["Layer 7"] = {
        "description": "Dynamic Failure/Recovery Propagation",
        "inference": l7_logic,
        "confidence": "SIMULATED",
        "source": "Derived from aggregate of layers"
    }

    # ---------- Layer 8 ----------
    l8_logic = []
    if herbal_class:
        if herbal_class.lower() in ['anti-diabetic', 'anti-obesity']:
            l8_logic.append("Matches metabolic disorder patterns (Layer 3, 5)")
        elif herbal_class.lower() in ['neuroprotective']:
            l8_logic.append("May match Alzheimer's or neurodegeneration profiles")
        else:
            l8_logic.append("Overlay matched from general plant class knowledge")
    else:
        l8_logic.append("No known NP overlay found — needs literature mining.")
    report["Layer 8"] = {
        "description": "Network Pharmacology Overlay (NP & Disease Match)",
        "inference": l8_logic,
        "confidence": "EXPERIMENTAL",
        "source": "NP-disease inference from herbal class mapping"
    }

    return report

# -------- Logging --------
def save_inp_report(report_dict, smiles, output_prefix="inp_session"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"{output_prefix}_{now}.json"
    txt_path = f"{output_prefix}_{now}.txt"

    with open(json_path, "w") as jf:
        json.dump(report_dict, jf, indent=4)

    with open(txt_path, "w") as tf:
        tf.write(f"INP 8-Layer Report for: {smiles}\\n\\n")
        for layer, content in report_dict.items():
            tf.write(f"{layer} - {content['description']}\\n")
            tf.write("Confidence: " + content['confidence'] + "\\n")
            tf.write("Source: " + content['source'] + "\\n")
            tf.write("Findings:\\n")
            for line in content['inference']:
                tf.write(" - " + line + "\\n")
            tf.write("\\n")

    return json_path, txt_path
