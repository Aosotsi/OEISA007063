"""
funnel_checkV4.py Brief Description:

Provides diagnostic verification of each i in a chosen range and each integer
delta in [-i-2, i+2]. Answers: how many steps (k <= Kmax) are required before 
either |delta| decreases or delta hits 0

Extended to i = 1k (change I_max as you see fit).

V4: Records the sign pattern and writes results to CSV

"""

import csv

I_min = 5          # lower i 
I_max = 1000       # upper i 
Kmax = 30          # max iterations per starting pair
#^ Kmax doesn't need to be higher than 10 tbh (tested)
CSV_OUTPUT = True  # CSV output?
CSV_FILENAME = "funnel_detailed_results.csv"

# Straight out of Section 3.1
def step(i, delta):
    """One-step map T_i(delta)."""
    if delta > 0:
        return (i + 1) - 2 * delta
    elif delta < 0:
        return (i + 2) + 2 * delta
    else:
        return 0

# ***Main*** comparisons
results = []
failures = []
max_k_observed = 0

for i in range(I_min, I_max + 1):
    bound = i + 2
    for delta0 in range(-bound, bound + 1):
        if delta0 == 0:
            continue
        cur = delta0
        pattern = []
        success = False

        for k in range(1, Kmax + 1):
            nxt = step(i + k - 1, cur)
            # record sign for pattern trace
            if nxt > 0:
                pattern.append("+")
            elif nxt < 0:
                pattern.append("-")
            else:
                pattern.append("0")

            # check for success conditions
            if nxt == 0 or abs(nxt) < abs(cur):
                max_k_observed = max(max_k_observed, k)
                results.append({
                    "i": i,
                    "delta0": delta0,
                    "k_success": k,
                    "pattern": "".join(pattern)
                })
                success = True
                break
            cur = nxt

        if not success:
            failures.append({
                "i": i,
                "delta0": delta0,
                "pattern": "".join(pattern),
                "final_delta": cur
            })

print("Checked i in range:", (I_min, I_max))
print("Total pairs examined:", len(results) + len(failures))
print("Max step (k) observed for descent or termination =", max_k_observed)
print("Failures =", len(failures))

# Must print samples
print("\nSample of first 10 successful trajectories:")
for row in results[:10]:
    print(
        f"i={row['i']:>3}, δ₀={row['delta0']:>4}, k={row['k_success']}, "
        f"pattern={row['pattern']}"
    )

if CSV_OUTPUT:
    fieldnames = ["i", "delta0", "k_success", "pattern"]
    with open(CSV_FILENAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"\nDetailed results written to {CSV_FILENAME} (13.7 MB on disk).")

# Failure (important!)
if failures:
    print("\nWARNING: some trajectories did NOT reach descent within Kmax")
    print("Example failures (up to 5):")
    for fail in failures[:5]:
        print(
            f"i={fail['i']}, δ₀={fail['delta0']}, "
            f"pattern={fail['pattern']}, final={fail['final_delta']}"
        )
else:
    print("\nAll trajectories showed descent or termination within Kmax steps.")
