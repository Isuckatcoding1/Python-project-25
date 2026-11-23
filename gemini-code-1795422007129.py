import pandas as pd
import streamlit as st

st.set_page_config(page_title="DNA PWM Motif Scanner", page_icon="🧬")

st.title("🧬 DNA PWM Motif Scanner")
st.write(
    "Scan a DNA sequence using a 3-bp Position Weight Matrix (PWM) to find"
    " motifs meeting or exceeding a score threshold."
)

# Default values matching your original script
DEFAULT_DNA = "ACGTACGATCGATCGATCG"
DEFAULT_THRESHOLD = 2.0
MOTIF_LEN = 3
VALID_BASES = {"A", "C", "G", "T"}

dna = (
    st.text_input("DNA Sequence (A, C, G, T)", value=DEFAULT_DNA)
    .upper()
    .strip()
)
threshold = st.number_input(
    "Score Threshold", value=DEFAULT_THRESHOLD, step=0.1, format="%.2f"
)

st.subheader("Position Weight Matrix (PWM)")
pwm_df = st.data_editor(
    pd.DataFrame(
        {
            0: [1.5, -0.5, -0.8, -2.0],
            1: [-2.0, 1.8, -1.2, 0.5],
            2: [0.8, -1.0, 1.9, 1.6],
        },
        index=["A", "C", "G", "T"],
    ),
    use_container_width=True,
)

if st.button("Scan Sequence", type="primary"):
  if not dna or not set(dna).issubset(VALID_BASES):
    st.error("Please enter a valid DNA sequence using only A, C, G, and T.")
  elif len(dna) < MOTIF_LEN:
    st.warning(f"Sequence length must be at least {MOTIF_LEN} base pairs.")
  else:
    pwm = {
        base: [float(pwm_df.loc[base, pos]) for pos in range(MOTIF_LEN)]
        for base in VALID_BASES
    }

    matches = []
    for i in range(len(dna) - MOTIF_LEN + 1):
      window = dna[i : i + MOTIF_LEN]
      score = 0.0
      for pos, base in enumerate(window):
        score += pwm[base][pos]

      if score >= threshold:
        matches.append({
            "Position": i,
            "Motif": window,
            "Score": round(score, 2),
        })

    if matches:
      st.success(f"Found {len(matches)} match(es) with score ≥ {threshold:.2f}:")
      st.dataframe(pd.DataFrame(matches), hide_index=True, use_container_width=True)
    else:
      st.info(f"No matches found with score ≥ {threshold:.2f}.")