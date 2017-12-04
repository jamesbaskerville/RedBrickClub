import ttc

# do parameter sweeps:
# number of agents = 1000
# proportion of rankings range from 0.1 to 1.0 in 0.1 increments
# anything else?
props = []
items = []
ranks = []
rounds = []

ttc.configure_logging('warning')

# Effect of proportion on ranking change, liquidity, # rounds
for prop in xrange(5, 101, 5):
    #print "Calculating proportion {}...".format(prop/100.0)
    res = ttc.start(1000, prop/100.0, seed = 234, prefs='correlated', buckets=5)
    props.append(prop/100.0)
    items.append(res[0])
    ranks.append(res[1])
    rounds.append(res[2])

n = len(items)
ttc_res = (items[n - 1], ranks[n - 1], rounds[n - 1])

print "Results (pos/neg effects vs. TTC outcome)"
print "-----------------------------------------"
for i in xrange(len(ranks)):
    prop, out, num_rounds, item_assign = props[i], ranks[i], rounds[i], items[i]
    neg, pos = ttc.compare_outcomes(ttc_res[1], out)
    liquidity = ttc.compute_liquidity(item_assign)
    print ( "{}%: (+{}, -{});".format(int(prop * 100), pos, neg) +
            "   net difference: {};".format(pos - neg) +
            "   rounds: {};".format(num_rounds) +
            "   liquidity: {}%".format((liquidity * 100)))

