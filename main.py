"""Run MSA_Modeling.ipynb headlessly; writes msa_output.csv and the executed notebook."""
import nbformat
from nbclient import NotebookClient

NOTEBOOK = "MSA_Modeling.ipynb"


def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)
    NotebookClient(nb, timeout=1800, kernel_name="python3").execute()
    nbformat.write(nb, NOTEBOOK)
    print("Done: msa_output.csv, msa_diagnostics.csv, country_summary.csv")


if __name__ == "__main__":
    main()
