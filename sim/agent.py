'''
    Agent:
        A participant in the item exchange simulation.

        Attributes:
            id:             agent identifier
            rep:            reputation score

            true_prefs:     true preferences of this agent
            rep_prefs:      reported preferences of this agent

'''
class Agent:
    def __init__(self, agent_id):
        self.rep = 1.0
        self.id = agent_id

    def init_preferences(self, available, true_prefs, reported_prefs):
        self.true_prefs = true_prefs
        self.rep_prefs = reported_prefs
        # pref_index is used for "pointing" at reported preferences
        self.pref_index = 0
        self.update_top_pref(available)

    def report(self):
        return self.rep_prefs

    def get_top_pref(self):
        if self.pref_index < len(self.rep_prefs):
            return self.rep_prefs[self.pref_index]
        else:
            return self.id

    def update_top_pref(self, available):
        while ( self.get_top_pref() not in available and
                self.pref_index < len(self.rep_prefs)):
            self.pref_index += 1

    def get_top_pref_index(self):
        return self.pref_index

    def truncate(self, reported = True):
        try:
            if reported:
                assert self.id in self.true_prefs
            else:
                assert self.id in self.rep_prefs
        except AssertionError:
            raise ValueError("Prefs must be complete")

    def __str__(self):
        return "Agent {}, rep: {}".format(self.id, self.rep)
