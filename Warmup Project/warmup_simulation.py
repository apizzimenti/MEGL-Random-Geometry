import argparse
import csv
from warmup_helpers import simulate_percolation
import numpy as np

def run_simulation(output_file, lower_p, upper_p, lower_N, upper_N, trials):
    headers = ["N", "p", "prop_first", "prop_second"]

    p_values = np.arange(lower_p, upper_p + 0.05, 0.1) 
    N_values = range(lower_N, upper_N + 1)

    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for p in p_values:
            current_p = round(p, 2)
            for N in N_values:
                for trial in range(0, trials):
                    prop_first, prop_second = simulate_percolation(N, current_p)
                    writer.writerow([N, current_p, prop_first, prop_second])

                f.flush()
                



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Percolation simulation on a periodic square lattice")
    
    parser.add_argument("output_file", help = "File name for the output CSV")
    parser.add_argument("--lp", type=float, default=0.1, help = "Lower p (default 0.1)")
    parser.add_argument("--up", type=float, default=1.0, help = "Upper p (default 1.0)")
    parser.add_argument("--ln", type=int, default=2, help = "Lower N (default 2)")
    parser.add_argument("--un", type=int, default=100, help = "Upper N (default 100)")
    parser.add_argument("--trials", type=int, default=30, help = "Trials per N/p (default 30)")
    
    args = parser.parse_args()

    run_simulation(
        args.output_file, 
        args.lp, 
        args.up, 
        args.ln, 
        args.un, 
        args.trials
    )


