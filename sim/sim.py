import ttc
from prettytable import PrettyTable
from tabulate import tabulate
import pandas as pd

def run(seed=None, from_file=False):
    # t = init_table()
    data = []

    ctrl_out = ttc.start(1000, 1.0, seed=seed, prefs='correlated', nbuckets=1)
    record_outcome(data, ctrl_out, ctrl_out)

    # # Test uniform preferences
    uni_out = ttc.start(1000, 1.0, seed=seed, prefs='uniform', nbuckets=1)
    record_outcome(data, ctrl_out, uni_out)

    # # Test effect of report proportion
    for prop in xrange(95, 1, -5):
        out = ttc.start(1000, prop/100.0, seed=seed, prefs='correlated', nbuckets=1)
        record_outcome(data, ctrl_out, out)

    # # Test effect of report proportion (uniform)
    for prop in xrange(95, 1, -5):
        out = ttc.start(1000, prop/100.0, seed=seed, prefs='uniform', nbuckets=1)
        record_outcome(data, ctrl_out, out)

    # Test effect of bucketing
    for nbuckets in xrange(5, 101, 5):
        out = ttc.start(1000, 1.0, seed=seed, prefs='correlated', nbuckets=nbuckets)
        record_outcome(data, ctrl_out, out)
    for nbuckets in xrange(125, 1001, 25):
        out = ttc.start(1000, 1.0, seed=seed, prefs='correlated', nbuckets=nbuckets)
        record_outcome(data, ctrl_out, out)

    # Test effect of bucketing (uniform)
    for nbuckets in xrange(5, 101, 5):
        out = ttc.start(1000, 1.0, seed=seed, prefs='uniform', nbuckets=nbuckets)
        record_outcome(data, ctrl_out, out)
    for nbuckets in xrange(125, 1001, 25):
        out = ttc.start(1000, 1.0, seed=seed, prefs='uniform', nbuckets=nbuckets)
        record_outcome(data, ctrl_out, out)

    df = pd.DataFrame()
    if from_file:
        df = load_df()

    df2 = create_df(data)
    df = df.append(df2)

    # print_df(df)
    save_df(df)
    print "Done!"

def compute_outcome(ctrl_out, out):
    liquidity = ttc.compute_liquidity(out[0])
    neg, pos = ttc.compare_outcomes(ctrl_out[1], out[1])
    nrounds = out[2]
    return map(str, out[3:]) + [str(pos), str(neg), str(liquidity), str(nrounds)]

def record_outcome(data, ctrl_out, out):
    res = compute_outcome(ctrl_out, out)
    data.append(res)
    return data

def load_df(csv_file='results.csv'):
    return pd.read_csv(csv_file)

def save_df(df, csv_file='results.csv'):
    df.to_csv(csv_file, index=False)

def create_df(data):
    return pd.DataFrame(data, columns=['Seed', 'n', 'Report Prop', 'Pref Dist Type', '# Buckets', 'Pos Effect', 'Neg Effect', 'Liquidity', '# Rounds'])

def print_df(df):
    print tabulate(df, headers='keys', tablefmt='psql')

if __name__ == '__main__':
    ttc.configure_logging('warning')
    run(seed=53608, from_file=True)
