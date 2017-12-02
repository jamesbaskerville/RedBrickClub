from ttc import ttc

# do parameter sweeps:
# number of agents = 1000
# proportion of rankings range from 0.1 to 1.0 in 0.1 increments
# anything else?
for prop in xrange(1, 11, 1):
    print ttc(1000, prop/10.0, seed = 312)
