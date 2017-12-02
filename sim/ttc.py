from agent import Agent
import random

def ttc(n, report_prop, seed = None, debug = False):
    random.seed(seed)

    agents = []
    k = int(report_prop * n)
    available_agents = set(range(n))

    for i in xrange(n):
        new_agent = Agent(i)
        true_prefs, rep_prefs = gen_prefs(n, k)
        if debug:
            print new_agent, "prefs:", rep_prefs
        new_agent.init_preferences(available_agents, true_prefs, rep_prefs)
        agents.append(new_agent)

    assigned_items = [-1] * n

    while available_agents:
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
            print "{}:".format(a_id),top_pref

        while top_pref not in visited:
            visited.add(top_pref)
            stack.append(top_pref)
            top_pref = agents[top_pref].get_top_pref()

        # get cycle
        cycle = stack[stack.index(top_pref):] + [top_pref]
        if debug:
            print "\ncycle found:", cycle, "\n"
        # assign matchings
        for i in xrange(len(cycle) - 1):
            assigned_items[cycle[i]] = cycle[i + 1]
        if debug:
            print "\nassigned matchings:", assigned_items, "\n"
        # remove cycle from market
        available_agents -= set(cycle)
        if debug:
            print "\navailable agents:", available_agents, "\n"

    return assigned_items


# generate a random preference order, ranking k out of n items (k <= n)
def gen_prefs(n, k):
    try:
        assert k <= n
    except AssertionError:
        raise ValueError("Prefs should have max length of n")
    return random.shuffle(range(n)), random.sample(range(n), k)

if __name__ == '__main__':
    res = ttc(1000, 1.0, seed = 9, debug=False)
    print res
