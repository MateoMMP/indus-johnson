
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Johnson 2‑Machine Scheduler", layout="centered")

st.title("Johnson's Algorithm – Paint & Quality Control Line")

st.markdown(
    """
    Esta aplicación aplica el algoritmo de Johnson para secuenciar **lotes de vehículos** que pasan
    por dos estaciones consecutivas:

    * **M1 – Cabina de Pintura**  
    * **M2 – Control de Calidad final**

    El objetivo es **minimizar el makespan** (tiempo total) y los tiempos muertos de las máquinas.
    """
)

# --- Datos de ejemplo (se pueden editar) ---------------------------------
default_jobs = {
    "Lote": ["A‑Sedán", "B‑SUV", "C‑Híbrido", "D‑Eléctrico", "E‑Compacto", "F‑Furgón"],
    "Pintura [M1] (min)": [45, 60, 50, 65, 40, 55],
    "Calidad [M2] (min)": [30, 25, 35, 20, 30, 25]
}
df = pd.DataFrame(default_jobs)

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    key="jobs_table"
)

st.markdown("### Sequencing result")

# --- Johnson's algorithm --------------------------------------------------
def johnson_two_machines(df_jobs):
    jobs = df_jobs.to_dict(orient="records")
    left_seq, right_seq = [], []
    while jobs:
        # identify job with smallest processing time
        min_job = min(jobs, key=lambda x: min(x["Pintura [M1] (min)"], x["Calidad [M2] (min)"]))
        jobs.remove(min_job)
        if min_job["Pintura [M1] (min)"] <= min_job["Calidad [M2] (min)"]:
            left_seq.append(min_job)
        else:
            right_seq.insert(0, min_job)
    return left_seq + right_seq

sequenced_jobs = johnson_two_machines(edited_df)

seq_df = pd.DataFrame(sequenced_jobs)
st.dataframe(seq_df, use_container_width=True)

# --- Construcción del diagrama de Gantt -----------------------------------
st.markdown("### Gantt chart")

fig, ax = plt.subplots(figsize=(10, 3))
m1_end, m2_end = 0, 0

for idx, job in enumerate(sequenced_jobs):
    m1_start = m1_end
    m1_end = m1_start + job["Pintura [M1] (min)"]

    m2_start = max(m1_end, m2_end)
    m2_end = m2_start + job["Calidad [M2] (min)"]

    # barras
    ax.barh(1, job["Pintura [M1] (min)"], left=m1_start, height=0.3, color="#1f77b4")
    ax.barh(0, job["Calidad [M2] (min)"], left=m2_start, height=0.3, color="#ff7f0e")

    # etiquetas
    ax.text(m1_start + job["Pintura [M1] (min)"]/2, 1, job["Lote"], ha="center", va="center", color="white", fontsize=8)
    ax.text(m2_start + job["Calidad [M2] (min)"]/2, 0, job["Lote"], ha="center", va="center", color="white", fontsize=8)

ax.set_yticks([0,1])
ax.set_yticklabels(["M2  Calidad", "M1  Pintura"])
ax.set_xlabel("Minutos")
ax.set_title("Secuencia optimizada – Makespan: {} min".format(m2_end))
ax.invert_yaxis()
ax.grid(True, axis="x", linestyle="--", alpha=0.4)
st.pyplot(fig)

st.success("Makespan total: {} minutos".format(m2_end))
st.caption("Basado en el algoritmo original de S. M. Johnson (1954)")
