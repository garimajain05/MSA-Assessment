# MSA modeling assignment

A population-aware core-and-catchment model that clusters cities into metropolitan areas,
in the US and internationally, with explicit non-metro regions.

## Run
1. Put `MSA_Modeling.ipynb` and `msa.csv` in the same folder.
2. Create an environment with Python 3.11–3.14: `python3 -m venv .venv && source .venv/bin/activate`
   (or `uv sync`).
3. Install: `python -m pip install -r requirements.txt`
4. Either open the notebook (`python -m jupyterlab`) and choose Run All, or run it headlessly with
   `python main.py`

## Outputs
- `msa_output.csv`: the deliverable. One row per input row, with columns City, State, Latitude,
  Longitude, Population, Traditional MSA and Your MSA. It covers US and international cities.
- `msa_diagnostics.csv` (optional): adds country, area type (Metro / Non-metro), whether the
  city seeded a metro, and distance to the metro anchor.
- `country_summary.csv` (optional): city, metro and entity counts per country.

## Method, in brief
1. **Seeds:** cities of 50k+ people, or the largest city of a 10 km cluster totalling 50k+.
2. **Urban cores:** seeds linked within 12 km.
3. **Metros:** cores are processed largest first. A core joins a metro if it lies within that
   metro's reach, where reach = 20 km × (P/50k)^0.3, capped at 80 km.
4. **Assignment:** every other city joins the metro with the strongest gravity pull among those
   that reach it. Otherwise it is non-metro.
5. **Rural regions:** non-metro cities are grouped into compact regions (at most 80 km across)
   within a state or province, e.g. "Non-metro NY – Watertown area".

The notebook covers the K-means, DBSCAN and SVM baselines, the calibration grid against the
noisy US labels, case studies, the argument for why this is more useful than the official
MSAs, and limitations.
