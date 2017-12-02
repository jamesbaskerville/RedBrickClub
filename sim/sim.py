import ttc

# do parameter sweeps:
# number of agents = 1000
# proportion of rankings range from 0.1 to 1.0 in 0.1 increments
# anything else?
ranks = []
rounds = []
for prop in xrange(1, 11, 1):
    res = ttc.run(1000, prop/10.0, seed = 234)
    ranks.append((prop/10.0, sum(res[1])))
    rounds.append((prop/10.0, res[2]))

print "\nResults:"
for i in xrange(len(ranks)):
    print "{}% reported preferences: {} ranks; {} rounds".format(ranks[i][0]*100,
                                                                  ranks[i][1],
                                                                  rounds[i][1])

