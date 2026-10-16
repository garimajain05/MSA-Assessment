"""Sanity checks for msa_output.csv. Run after the notebook: python verify.py"""
import pandas as pd

inp = pd.read_csv("msa.csv", index_col=0)
out = pd.read_csv("msa_output.csv")
diag = pd.read_csv("msa_diagnostics.csv")

def check(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)

# 1. Deliverable format
cols = ["City", "State", "Latitude", "Longitude", "Population", "Traditional MSA", "Your MSA"]
check("exactly the 7 required columns", list(out.columns) == cols)
check("one output row per input row, same order", len(out) == len(inp) and (out.City.values == inp.city.values).all())
check("every row has a label", out["Your MSA"].notna().all())

# 2. Model rules hold
members = diag[diag["Area Type"].eq("Metro") & ~diag.seed]
check("no assigned town is more than 80 km from its metro's anchor", members.anchor_distance_km.le(80 + 1e-6).all())
check("non-metro rows are labelled 'Non-metro ...'",
      diag.loc[diag["Area Type"].eq("Non-metro"), "Your MSA"].str.startswith("Non-metro").all())

# 3. Spot checks against common sense (city, state/region, expected substring)
expected = [
    ("mahopac", "new york", "New York City"),        # NYC exurb
    ("yokohama", "kanagawa", "Tokyo"),               # part of greater Tokyo
    ("gurgaon", "haryana", "Delhi"),
    ("fort worth", "texas", "Dallas–Fort Worth"),
    ("plattsburgh", "new york", "Non-metro"),         # rural upstate NY
    ("watertown", "new york", "Non-metro"),
    ("jacksonville", "oregon", "Medford"),           # official label wrongly says Jacksonville FL
]
for city, state, want in expected:
    got = out.loc[out.City.eq(city) & out.State.eq(state), "Your MSA"]
    check(f"{city}, {state} -> contains '{want}'  (got: {got.iloc[0] if len(got) else 'MISSING'})",
          len(got) > 0 and want in got.iloc[0])

# 4. Big official metros are kept mostly whole (share of cities in our single biggest match)
us = out[diag.country_key.eq("united states").values]
for msa in ["New York-Northern New Jersey-Long Island NY-NJ-PA MSA", "Chicago-Naperville-Joliet IL-IN-WI MSA",
            "Dallas-Fort Worth-Arlington TX MSA", "Houston-Sugar Land-Baytown TX MSA"]:
    s = us.loc[us["Traditional MSA"].eq(msa), "Your MSA"].value_counts(normalize=True)
    check(f"{msa[:30]:<30} {s.iloc[0]:.0%} in '{s.index[0]}'", s.iloc[0] >= 0.75)

# 5. Overall shape
metro_share = diag.loc[diag["Area Type"].eq("Metro") & diag.country_key.eq("united states"), "population"].sum() \
    / diag.loc[diag.country_key.eq("united states"), "population"].sum()
print(f"\nUS population in metros: {metro_share:.0%} (official ~86%)")
print("Metros:", diag.loc[diag["Area Type"].eq("Metro"), "Your MSA"].nunique(),
      "| Non-metro regions:", diag.loc[diag["Area Type"].eq("Non-metro"), "Your MSA"].nunique())

# 6. Eyeball a random sample: does each label make sense for that town?
print("\nRandom sample to eyeball:")
print(out.sample(15, random_state=None)[["City", "State", "Population", "Your MSA"]].to_string(index=False))
