import ttc

# do parameter sweeps:
# number of agents = 1000
# proportion of rankings range from 0.1 to 1.0 in 0.1 increments
# anything else?
ranks = []
rounds = []

ttc.configure_logging('warning')
for prop in xrange(1, 11, 1):
    res = ttc.run(1000, prop/10.0, seed = 234)
    ranks.append((prop/10.0, res[1]))
    rounds.append((prop/10.0, res[2]))

ttc_out = ranks[9][1]

print "Results (pos/neg effects vs. TTC outcome)"
print "-----------------------------------------"
for prop, out in ranks:
    neg, pos = ttc.compare_outcomes(ttc_out, out)
    print "{}%: (+{}, -{}), net difference: {}".format(int(prop * 100),
                                                       pos,
                                                       neg,
                                                       pos - neg)
