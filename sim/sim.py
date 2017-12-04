import ttc

# do parameter sweeps:
# number of agents = 1000
# proportion of rankings range from 0.1 to 1.0 in 0.1 increments
# anything else?
ranks = []
rounds = []

ttc.configure_logging('warning')
for prop in xrange(5, 101, 5):
    #print "Calculating proportion {}...".format(prop/100.0)
    res = ttc.run(1000, prop/100.0, seed = 234, prefs='uniform')
    ranks.append((prop/10.0, res[1]))
    rounds.append(res[2])

ttc_out = ranks[len(ranks) - 1][1]

print "Results (pos/neg effects vs. TTC outcome)"
print "-----------------------------------------"
for i, (prop, out) in enumerate(ranks):
    neg, pos = ttc.compare_outcomes(ttc_out, out)
    print "{}%: (+{}, -{}), net difference: {}, rounds: {}".format(int(prop * 10),
                                                       pos,
                                                       neg,
                                                       pos - neg, rounds[i])
