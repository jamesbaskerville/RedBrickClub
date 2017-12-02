from agent import Agent
import random

def run(n, report_prop, seed = None, debug = False):
    print "\nBeginning Run of TTC Algorithm"
    random.seed(seed)

    agents = []
    k = int(report_prop * n)
    available_agents = set(range(n))

    print "Assigning initial true and reported preferences..."
    for i in xrange(n):
        new_agent = Agent(i)
        true_prefs, rep_prefs = gen_prefs(n, k, debug)
        if debug:
            print new_agent, "; prefs:", true_prefs, rep_prefs
        new_agent.init_preferences(available_agents, true_prefs, rep_prefs)
        agents.append(new_agent)

    assigned_items = [-1] * n

    print "Running TTC..."
    rounds = 0
    while available_agents:
        rounds += 1
        print "Round {}".format(rounds)
        # update top preferences ("pointing"/directed edges in graph)
        for a_id in available_agents:
            agents[a_id].update_top_pref(available_agents)
            if debug:
                print agents[a_id], "prefs:", agents[a_id].get_top_pref()

        # find a cycle
        visited = set()
        stack = []

        a_id = available_agents.pop()
        available_agents.add(a_id)
        visited.add(a_id)
        stack.append(a_id)

        top_pref = agents[a_id].get_top_pref()
        if debug:
            print "starting DFS from agent {}".format(a_id)
            print "stack:", stack

        while top_pref not in visited:
            visited.add(top_pref)
            stack.append(top_pref)
            top_pref = agents[top_pref].get_top_pref()
            if debug:
                print "stack:", stack

        # get cycle
        cycle = stack[stack.index(top_pref):] + [top_pref]
        if debug:
            print "cycle found:", cycle
        # assign matchings
        for i in xrange(len(cycle) - 1):
            assigned_items[cycle[i]] = cycle[i + 1]
        if debug:
            print "updated matchings:", assigned_items
        # remove cycle from market
        available_agents -= set(cycle)
        if debug:
            print "remaining agents:", available_agents, "\n"
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
    if debug:
        print true_prefs, rep_indices, rep_prefs
    return true_prefs, rep_prefs

if __name__ == '__main__':
    res = run(10, 0.75, seed = 124, debug=True)
    print res
