# MSA modeling assignment

1. Put `MSA_Modeling.ipynb` and `msa.csv` in the same folder.
2. Create an environment: `python3 -m venv .venv`.
3. Activate it: `source .venv/bin/activate` (macOS/Linux).
4. Install packages: `python -m pip install -r requirements.txt`.
5. Launch: `python -m jupyterlab`.
6. Open the notebook, select the environment's Python kernel, and Run All.
7. Review the EDA, model comparisons, sensitivity tables and limitations.
8. Submit the notebook and `msa_output.csv`.

Everything is implemented in the notebook. DataCleaningAPI handles audits,
canonicalization and ML representations. DataProcessingAPI implements K-means,
DBSCAN and the final population-aware model. SVM is a supervised diagnostic.
The CSV includes US and international cities. Original input rows are preserved.
`msa_diagnostics.csv` adds country, row IDs, metro status and anchor distances;
`country_summary.csv` reports coverage. These are optional review outputs.

Default geographic and population thresholds are policy assumptions, not proven
optimal settings. The notebook explains why commuter/workforce data is needed
to establish an advantage over official MSAs.
