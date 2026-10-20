"""Lock the per-object configuration for the conformance evaluator (2026-10-20; regenerated for v2.1 the same day), BEFORE any test-sector photometry is examined.
Reference depth/duration: the value printed in the registration's "Reference values for the outcome clauses" line; where a registration
predates that line (TIC 120444365 v2, TIC 70441745 v2), the same rule the generator applies to every later freeze
(prereg_v2.py: ref_depth = report.json sap_depth; ref_T14 = shape_mcmc T14_h if present, else the BLS duration_h), recorded as a dated
amendment. Product: QLP SAP_FLUX (every reference depth is raw SAP; the QLP sectors of every ephemeris were timed on SAP flux, some
ephemerides also use SPOC 2-min PDCSAP sectors). Release of record: the first QLP release, v01 (later releases reported separately).
Withdrawn tests get no config.
Output: configs/conformance/<TIC>_S<sector>.json"""
import os, re, json, hashlib
R = "/Users/fernando/Desktop/NASA"; OUT = f"{R}/configs/conformance"; os.makedirs(OUT, exist_ok=True)
TESTS = {183374279: (106, "v2"), 120444365: (106, "v2"), 70441745: (106, "v2"), 206620592: (106, "v2"), 122522485: (106, "v2"), 253931796: (106, "v2"), 115692561: (106, "v2")}
for tic, (sec, ver) in TESTS.items():
    d = f"{R}/results/vet_allsky/{tic}"; txt = open(f"{d}/PREREGISTRATION_{ver}.md").read(); pred = f"{d}/predicted_transits_2026_2027_{ver}.csv"
    m = re.search(r"Reference values for the outcome clauses: depth (\d+) ppm \([^)]*\), T14 ([\d.]+) h", txt)
    if m:
        cut = min([i for i in (txt.find("ADDENDUM"), txt.find("**Addendum"), txt.find("**Amendment")) if i >= 0] or [len(txt)])
        dep, dur = float(m.group(1)), float(m.group(2))
        src = f"PREREGISTRATION_{ver}.md reference-values line (frozen text)" if m.start() < cut else f"PREREGISTRATION_{ver}.md reference-values line in a post-freeze dated addendum"
    else:
        rep = json.load(open(f"{d}/report.json")); dep = round(rep["sap_depth"]["depth_ppm"]); dur = rep.get("shape_mcmc", {}).get("T14_h", rep["bls_refine"]["duration_h"])
        has_t14 = "T14_h" in rep.get("shape_mcmc", {})
        src = ("dated amendment 2026-10-20: report.json sap_depth; " + ("shape-fit T14_h" if has_t14 else "BLS duration_h (the shape fit exists but has no T14_h field)") + "; registration predates the reference-values line")
    eph = json.load(open(f"{d}/final_ephemeris_{ver}.json")); sha = hashlib.sha256(open(pred, "rb").read()).hexdigest(); assert sha == eph["sha256_csv"], tic
    cfg = dict(tic=tic, sector=sec, test_of_record=f"{ver} ({os.path.basename(pred)})", product="QLP", flux_col="SAP_FLUX", pred_csv=pred, pred_sha256=sha,
               ref_depth_ppm=round(float(dep), 1), ref_dur_h=round(float(dur), 3), reference_source=src,
               timing_rule="max(3 mean sigma_min, 30 min) adopted (CLARIFICATION_TIMING_RULE_2026-10-20.md); min(3 sigma, 30 min) reading also reported",
               evaluator="scripts/prereg_conformance.py (conformance-v2.1) plus the frozen scripts/prereg_test.py (literal output also reported)",
               evaluator_sha256=hashlib.sha256(open(f"{R}/scripts/prereg_conformance.py", "rb").read()).hexdigest(),
               frozen_evaluator_commands=[f"python -I scripts/prereg_test.py --lc <QLP S{sec} HLSP FITS> --flux-col {col} --pred {os.path.relpath(pred, R)} --depth-ppm {round(float(dep), 1)} --dur-h {round(float(dur), 3)} --sector {sec}" for col in ("SAP_FLUX", "DET_FLUX")],
               frozen_evaluator_note="SAP_FLUX = same source FITS and flux column as the conformance procedure (the frozen evaluator applies its own preprocessing and no clock correction); DET_FLUX = the protocol's column (PREREG_PROTOCOL.tex). Both literal outputs are reported.",
               release_of_record="v01", strict_epochs=([245, 246] if tic == 183374279 else None),
               edge_rule="drop 1.5 d after data start / resume (gap > 0.5 d) and 0.5 d before any gap > 0.1 d or data end (author-selected pooled rule; DECISIONS 76, 82, 86)",
               object_specific_clauses=("addendum 2026-10-19 item 1 stays in force: a gap or flagged cadences at epoch 245 or 246 makes the outcome INSUFFICIENT; the more conservative outcome is reported" if tic == 183374279 else None),
               data_status="sector already observed; public data products existed at freeze; authors attest target-sector photometry not examined (ERRATUM_S106)",
               locked_utc=__import__("datetime").datetime.now(__import__("datetime").UTC).strftime("%Y-%m-%d %H:%M:%S UTC"))
    p = f"{OUT}/{tic}_S{sec}.json"; json.dump(cfg, open(p, "w"), indent=1); print(tic, sec, dep, dur, src[:40])
