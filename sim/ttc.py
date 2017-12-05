from agent import Agent
import numpy as np
import random
import logging
import sys

def start(n, report_prop, seed=None, prefs='correlated', nbuckets=1):
    logging.info("\nSTART")
    np.random.seed(seed)

    agents = []
    k = int(report_prop * n)
    bucket_sz = int(n / nbuckets)
    available_agents = set(np.arange(n))

    logging.info("Generating normal preference order distributions...")
    dists = gen_pref_dists(n)

    logging.info("Assigning initial true and reported preferences...")
    sample_pref_dists(n, k, dists)
    for i in xrange(n):
        new_agent = Agent(i)

        if prefs == 'uniform':
            true_prefs, rep_prefs = gen_prefs(n, k)
        else:
            true_prefs, rep_prefs = sample_pref_dists(n, k, dists)

        new_agent.init_preferences(available_agents, true_prefs, rep_prefs)
        agents.append(new_agent)

    item_assignment = np.empty(n, dtype=int)
    rounds = 0

    logging.info("Running TTC...")
    for bucket in xrange(nbuckets):
        logging.info("  Bucket {}".format(bucket))
        start = bucket * bucket_sz
        end = min((bucket + 1) * bucket_sz, n)
        num = end - start
        available_agents = set(np.arange(start, end))
        logging.debug("    {} {} {} {}".format(bucket, start, end, num, available_agents))
        bucket_assign, bucket_rounds = run(available_agents, agents, n)
        #print bucket_assign
        np.put(item_assignment, np.arange(start, end), bucket_assign[start:end])
        #print item_assignment
        rounds += bucket_rounds

    logging.info("END\n")
    return item_assignment, get_pref_outcomes(agents, n), rounds, seed, n, '%.2f' % report_prop, prefs, nbuckets

def run(available_agents, agents, n):
    item_assignment = np.empty(n, dtype=int)
    rounds = 0
    while available_agents:
        rounds += 1
        logging.info("    Round {}".format(rounds))
        # update top preferences ("pointing"/directed edges in graph)
        for a_id in available_agents:
            agents[a_id].update_top_pref(available_agents)

        # find all cycles
        visited = set()
        unvisited_agents = available_agents - visited
        while unvisited_agents:
            stack = []
            a_id = unvisited_agents.pop()
            visited.add(a_id)
            stack.append(a_id)

            top_pref = agents[a_id].get_top_pref()

            while top_pref not in visited:
                visited.add(top_pref)
                stack.append(top_pref)
                top_pref = agents[top_pref].get_top_pref()

            # there's a cycle
            if top_pref in stack:
                cycle = stack[stack.index(top_pref):] + [top_pref]
                # assign matchings
                for i in xrange(len(cycle) - 1):
                    item_assignment[cycle[i]] = cycle[i + 1]
                # remove cycle from market
                available_agents -= set(cycle)

            unvisited_agents = available_agents - visited

    return item_assignment, rounds

# a list of the result of the algorithm for each agent
# (e.g. their preference for the item which they were assigned)
def get_pref_outcomes(agents, n):
    vfunc = np.vectorize(lambda a: agents[a].get_top_pref_index())
    return vfunc(np.arange(n))

# generate a preference order distribution for each item
# each distribution is a normal with a random SD and mean = item number
# we assume lower-numbered items are, on average, more valuable WLOG
def gen_pref_dists(n):
    means = np.arange(n, dtype = float)
    sdevs = np.random.random(n) * n / 2.0
    return means, sdevs

# sample over item preference order distributions to generate a pref order
# rank in order in the floats generated--both true and reported prefs
def sample_pref_dists(n, k, (means, sdevs)):
    try:
        assert k <= n and len(means) == n and len(sdevs) == n
    except AssertionError:
        raise ValueError("Wrong number of reports or preference distributions")

    true_prefs = np.stack((np.arange(n), np.random.normal(means, sdevs, n)), axis=-1)

    # numpy makes it hard to sort by column...
    true_prefs.view('i8,f8').sort(order=['f1'], axis=0)
    # strip rankings, leaving just the strict preference order
    true_prefs = np.delete(true_prefs, 1, 1)

    # report preference on k items, keeping order from the true preferences
    rep_prefs = true_prefs[np.sort(np.random.choice(np.arange(n), size=k, replace=False))]

    return true_prefs.flatten().astype(int), rep_prefs.flatten().astype(int)

def configure_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    root_logger = logging.getLogger('')
    strm_out = logging.StreamHandler(sys.__stdout__)
    strm_out.setFormatter(logging.Formatter('%(message)s'))
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(strm_out)

# compare two pref outcomes, calculating the number of agents who do worse
def compare_outcomes(ttc, other):
    return (len(filter(lambda (t, o): t < o, zip(ttc, other))),
            len(filter(lambda (t, o): t > o, zip(ttc, other))))

# liquidity is defined as the proportion of agents who receive a different item
def compute_liquidity(item_assignment):
    n = len(item_assignment)
    no_change = 0.0
    it = np.nditer(item_assignment, flags=['f_index'])
    while not it.finished:
        if it.index == it[0]:
            no_change += 1.0
        it.iternext()
    return (1.0 - no_change / n)

### DEPRECATED ###

# generate a uniform random preference order, ranking k out of n items (k <= n)
def gen_prefs(n, k):
    try:
        assert k <= n
    except AssertionError:
        raise ValueError("Prefs should have max length of n")
    true_prefs = np.arange(n)
    np.random.shuffle(true_prefs)
    rep_prefs = true_prefs[np.sort(np.random.choice(np.arange(n), size=k, replace=False))]
    return true_prefs.flatten().astype(int), rep_prefs.flatten().astype(int)

if __name__ == '__main__':
    configure_logging('info')
    res = start(1000, 1.0, seed=234, prefs='correlated', nbuckets=1)
    print "items: {}".format(res[0])
    print "outcomes: {}".format(res[1])
    print "rounds: {}".format(res[2])
    print "liquidity: {}%".format(compute_liquidity(res[0]) * 100)
