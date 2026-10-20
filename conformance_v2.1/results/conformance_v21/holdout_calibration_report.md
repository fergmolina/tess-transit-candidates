# Holdout calibration, conformance-v2.1 (holdout sectors only; DECISIONS 76, 82)

Outcome of record includes the timing-split check. Cases: null (real transits removed), ontime (reference box), displaced (+(gate+60) min).
Real-transit holes exceed 0.1 d for 183374279 and 253931796 and trigger the 0.5-d pre-gap trim there (not present in S106).

## Per target-sector
```
      tic  sector      case  runs  insufficient  scored  N_eff                         RECOVERED                      INCONSISTENT                          EXCLUDED                         AMBIGUOUS
 70441745      68 displaced    40             0      40      8  0/40 [0.00-0.09] Neff[0.00-0.37] 31/40 [0.62-0.89] Neff[0.35-0.97]  0/40 [0.00-0.09] Neff[0.00-0.37]  9/40 [0.11-0.38] Neff[0.03-0.65]
 70441745      68      null    40             0      40      8  0/40 [0.00-0.09] Neff[0.00-0.37]  0/40 [0.00-0.09] Neff[0.00-0.37]  0/40 [0.00-0.09] Neff[0.00-0.37] 40/40 [0.91-1.00] Neff[0.63-1.00]
 70441745      68    ontime    40             0      40      8 37/40 [0.80-0.98] Neff[0.47-1.00]  0/40 [0.00-0.09] Neff[0.00-0.37]  0/40 [0.00-0.09] Neff[0.00-0.37]  3/40 [0.02-0.20] Neff[0.00-0.53]
115692561      69 displaced    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
115692561      69      null    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
115692561      69    ontime    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
120444365      69 displaced    40             4      36      3  0/36 [0.00-0.10] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71] 36/36 [0.90-1.00] Neff[0.29-1.00]
120444365      69      null    40             4      36      3  0/36 [0.00-0.10] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71] 36/36 [0.90-1.00] Neff[0.29-1.00]
120444365      69    ontime    40             4      36      3  4/36 [0.03-0.26] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71]  0/36 [0.00-0.10] Neff[0.00-0.71] 32/36 [0.74-0.97] Neff[0.29-1.00]
120444365     103 displaced    40             4      36      2  0/36 [0.00-0.10] Neff[0.00-0.84] 12/36 [0.19-0.51] Neff[0.01-0.99]  0/36 [0.00-0.10] Neff[0.00-0.84] 24/36 [0.49-0.81] Neff[0.01-0.99]
120444365     103      null    40             4      36      2  0/36 [0.00-0.10] Neff[0.00-0.84]  0/36 [0.00-0.10] Neff[0.00-0.84]  1/36 [0.00-0.15] Neff[0.00-0.84] 35/36 [0.85-1.00] Neff[0.16-1.00]
120444365     103    ontime    40             4      36      2 28/36 [0.61-0.90] Neff[0.16-1.00]  0/36 [0.00-0.10] Neff[0.00-0.84]  0/36 [0.00-0.10] Neff[0.00-0.84]  8/36 [0.10-0.39] Neff[0.00-0.84]
122522485     105 displaced    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
122522485     105      null    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
122522485     105    ontime    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
183374279      69 displaced    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71] 40/40 [0.91-1.00] Neff[0.29-1.00]
183374279      69      null    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71]  3/40 [0.02-0.20] Neff[0.00-0.71] 37/40 [0.80-0.98] Neff[0.29-1.00]
183374279      69    ontime    40             0      40      3  8/40 [0.09-0.36] Neff[0.01-0.91]  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71] 32/40 [0.64-0.91] Neff[0.09-0.99]
183374279     103 displaced    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71] 31/40 [0.62-0.89] Neff[0.09-0.99]  0/40 [0.00-0.09] Neff[0.00-0.71]  9/40 [0.11-0.38] Neff[0.01-0.91]
183374279     103      null    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71]  4/40 [0.03-0.24] Neff[0.00-0.71] 36/40 [0.76-0.97] Neff[0.29-1.00]
183374279     103    ontime    40             0      40      3 37/40 [0.80-0.98] Neff[0.29-1.00]  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71]  3/40 [0.02-0.20] Neff[0.00-0.71]
206620592      68 displaced    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
206620592      68      null    40             0      40      1  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 40/40 [0.91-1.00] Neff[0.03-1.00]
206620592      68    ontime    40             0      40      1 15/40 [0.23-0.54] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97]  0/40 [0.00-0.09] Neff[0.00-0.97] 25/40 [0.46-0.77] Neff[0.03-1.00]
253931796      68 displaced    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71] 37/40 [0.80-0.98] Neff[0.29-1.00]  0/40 [0.00-0.09] Neff[0.00-0.71]  3/40 [0.02-0.20] Neff[0.00-0.71]
253931796      68      null    40             0      40      3  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71] 37/40 [0.80-0.98] Neff[0.29-1.00]  3/40 [0.02-0.20] Neff[0.00-0.71]
253931796      68    ontime    40             0      40      3 38/40 [0.83-0.99] Neff[0.29-1.00]  0/40 [0.00-0.09] Neff[0.00-0.71]  0/40 [0.00-0.09] Neff[0.00-0.71]  2/40 [0.01-0.17] Neff[0.00-0.71]
```

## Per target (holdout sectors pooled)
```
70441745 (N_eff total 8; INSUFFICIENT 0/120): null->RECOVERED 0/40 [0.00-0.09]; null->EXCLUDED 0/40 [0.00-0.09]; ontime->RECOVERED 37/40 [0.80-0.98]; ontime->INCONSISTENT 0/40 [0.00-0.09]; displaced->RECOVERED 0/40 [0.00-0.09]; displaced->INCONSISTENT 31/40 [0.62-0.89]
115692561 (N_eff total 1; INSUFFICIENT 0/120): null->RECOVERED 0/40 [0.00-0.09]; null->EXCLUDED 0/40 [0.00-0.09]; ontime->RECOVERED 0/40 [0.00-0.09]; ontime->INCONSISTENT 0/40 [0.00-0.09]; displaced->RECOVERED 0/40 [0.00-0.09]; displaced->INCONSISTENT 0/40 [0.00-0.09]
120444365 (N_eff total 5; INSUFFICIENT 24/240): null->RECOVERED 0/72 [0.00-0.05]; null->EXCLUDED 1/72 [0.00-0.07]; ontime->RECOVERED 32/72 [0.33-0.57]; ontime->INCONSISTENT 0/72 [0.00-0.05]; displaced->RECOVERED 0/72 [0.00-0.05]; displaced->INCONSISTENT 12/72 [0.09-0.27]
122522485 (N_eff total 1; INSUFFICIENT 0/120): null->RECOVERED 0/40 [0.00-0.09]; null->EXCLUDED 0/40 [0.00-0.09]; ontime->RECOVERED 0/40 [0.00-0.09]; ontime->INCONSISTENT 0/40 [0.00-0.09]; displaced->RECOVERED 0/40 [0.00-0.09]; displaced->INCONSISTENT 0/40 [0.00-0.09]
183374279 (N_eff total 6; INSUFFICIENT 0/240): null->RECOVERED 0/80 [0.00-0.05]; null->EXCLUDED 7/80 [0.04-0.17]; ontime->RECOVERED 45/80 [0.45-0.67]; ontime->INCONSISTENT 0/80 [0.00-0.05]; displaced->RECOVERED 0/80 [0.00-0.05]; displaced->INCONSISTENT 31/80 [0.28-0.50]
206620592 (N_eff total 1; INSUFFICIENT 0/120): null->RECOVERED 0/40 [0.00-0.09]; null->EXCLUDED 0/40 [0.00-0.09]; ontime->RECOVERED 15/40 [0.23-0.54]; ontime->INCONSISTENT 0/40 [0.00-0.09]; displaced->RECOVERED 0/40 [0.00-0.09]; displaced->INCONSISTENT 0/40 [0.00-0.09]
253931796 (N_eff total 3; INSUFFICIENT 0/120): null->RECOVERED 0/40 [0.00-0.09]; null->EXCLUDED 37/40 [0.80-0.98]; ontime->RECOVERED 38/40 [0.83-0.99]; ontime->INCONSISTENT 0/40 [0.00-0.09]; displaced->RECOVERED 0/40 [0.00-0.09]; displaced->INCONSISTENT 37/40 [0.80-0.98]
```

Family-wise false RECOVERED across the 7 tests: point 0.000; with every per-test rate at its N_eff upper bound 1.000.
