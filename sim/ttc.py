from agent import Agent
import numpy as np
import random
import logging
import sys

def run(n, report_prop, seed=None, prefs='correlated'):
    #logging.info("\nBeginning Run of TTC Algorithm")
    np.random.seed(seed)

    agents = []
    k = int(report_prop * n)
    available_agents = set(np.arange(n))

    #logging.info("Generating normal preference order distributions...")
    dists = gen_pref_dists(n)

    #logging.info("Assigning initial true and reported preferences...")
    sample_pref_dists(n, n-2, dists)
    for i in xrange(n):
        new_agent = Agent(i)

        if prefs == 'uniform':
            true_prefs, rep_prefs = gen_prefs(n, k)
        else:
            true_prefs, rep_prefs = sample_pref_dists(n, k, dists)

        #logging.debug("{}; prefs: {}, {}".format(new_agent, true_prefs, rep_prefs))
        new_agent.init_preferences(available_agents, true_prefs, rep_prefs)
        agents.append(new_agent)

    assigned_items = np.empty(n, dtype=int)

    #logging.info("Running TTC...")
    rounds = 0
    while available_agents:
        rounds += 1
        #logging.info("Round {}".format(rounds))
        # update top preferences ("pointing"/directed edges in graph)
        for a_id in available_agents:
            agents[a_id].update_top_pref(available_agents)
            #logging.debug("{} ; top_pref: {}".format(agents[a_id], agents[a_id].get_top_pref()))

        # find a cycle
        visited = set()
        stack = []

        a_id = available_agents.pop()
        available_agents.add(a_id)
        visited.add(a_id)
        stack.append(a_id)

        top_pref = agents[a_id].get_top_pref()
        #logging.debug("starting DFS from agent {}".format(a_id))
        #logging.debug("stack:{}".format(stack))

        while top_pref not in visited:
            visited.add(top_pref)
            stack.append(top_pref)
            top_pref = agents[top_pref].get_top_pref()
            #logging.debug("stack:{}".format(stack))

        # get cycle
        cycle = stack[stack.index(top_pref):] + [top_pref]
        #logging.debug("cycle found: {}".format(cycle))
        # assign matchings
        for i in xrange(len(cycle) - 1):
            assigned_items[cycle[i]] = cycle[i + 1]
        #logging.debug("updated matchings: {}".format(assigned_items))
        # remove cycle from market
        available_agents -= set(cycle)
        #logging.debug("remaining agents: {}\n".format(available_agents))
    return assigned_items, get_pref_outcomes(agents, n), rounds

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
    #logging.debug("Pref dist means and SDs:\n{}\n{}".format(means, sdevs))
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
    ##logging.debug("prefs: {},\n {}".format(true_prefs.flatten().tolist(), rep_prefs.flatten().tolist()))

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
    #logging.debug("{} {}".format(true_prefs, rep_prefs))
    return true_prefs.flatten().astype(int), rep_prefs.flatten().astype(int)

if __name__ == '__main__':
    configure_logging('warning')
    res = run(1000, 0.90, seed = 234, prefs='correlated')
    print "items:\n{}".format(res[0])
    print "outcomes:\n{}".format(res[1])
    print "rounds:\n{}".format(res[2])
