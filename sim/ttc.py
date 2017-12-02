from agent import Agent
import random
import logging
import sys

def run(n, report_prop, seed = None, debug = False):
    logging.info("\nBeginning Run of TTC Algorithm")
    random.seed(seed)

    agents = []
    k = int(report_prop * n)
    available_agents = set(range(n))

    logging.info("Assigning initial true and reported preferences...")
    for i in xrange(n):
        new_agent = Agent(i)
        true_prefs, rep_prefs = gen_prefs(n, k, debug)
        if debug:
            print new_agent, "; prefs:", true_prefs, rep_prefs
        new_agent.init_preferences(available_agents, true_prefs, rep_prefs)
        agents.append(new_agent)

    assigned_items = [-1] * n

    logging.info("Running TTC...")
    rounds = 0
    while available_agents:
        rounds += 1
        logging.info("Round {}".format(rounds))
        # update top preferences ("pointing"/directed edges in graph)
        for a_id in available_agents:
            agents[a_id].update_top_pref(available_agents)
            logging.debug("{} ; top_pref: {}".
                          format(agents[a_id], agents[a_id].get_top_pref()))

        # find a cycle
        visited = set()
        stack = []

        a_id = available_agents.pop()
        available_agents.add(a_id)
        visited.add(a_id)
        stack.append(a_id)

        top_pref = agents[a_id].get_top_pref()
        logging.debug("starting DFS from agent {}".format(a_id))
        logging.debug("stack:{}".format(stack))

        while top_pref not in visited:
            visited.add(top_pref)
            stack.append(top_pref)
            top_pref = agents[top_pref].get_top_pref()
            logging.debug("stack:{}".format(stack))

        # get cycle
        cycle = stack[stack.index(top_pref):] + [top_pref]
        logging.debug("cycle found: {}".format(cycle))
        # assign matchings
        for i in xrange(len(cycle) - 1):
            assigned_items[cycle[i]] = cycle[i + 1]
        logging.debug("updated matchings: {}".format(assigned_items))
        # remove cycle from market
        available_agents -= set(cycle)
        logging.debug("remaining agents: {}\n".format(available_agents))
    return assigned_items, get_pref_outcomes(agents, assigned_items), rounds

# a list of the result of the algorithm for each agent
# (e.g. their preference for the item which they were assigned)
def get_pref_outcomes(agents, assigned_items):
    return map(lambda (a, i): agents[a].get_top_pref_index(),
               enumerate(assigned_items))

# generate a random preference order, ranking k out of n items (k <= n)
def gen_prefs(n, k, debug = False):
    try:
        assert k <= n
    except AssertionError:
        raise ValueError("Prefs should have max length of n")
    true_prefs = range(n)
    random.shuffle(true_prefs)
    rep_indices = set(random.sample(range(n), k))
    rep_prefs = map(lambda (_, p): p,
                    filter(lambda (a, _): a in rep_indices,
                           enumerate(true_prefs)))
    logging.debug("{} {} {}".format(true_prefs, rep_indices, rep_prefs))
    return true_prefs, rep_prefs

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

if __name__ == '__main__':
    configure_logging('info')
    res = run(10, 0.75, seed = 124)
    print "items:    {}".format(res[0])
    print "outcomes: {}".format(res[1])
    print "rounds:   {}".format(res[2])
