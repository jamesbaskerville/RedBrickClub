import secrets

'''
    Agent:
        A participant in the item exchange simulation.

        Attributes:
            id:             agent identifier
            rep:            reputation score
            item:           item belonging to the user (if it exists)

            nitems:         the total number of items in a round
            true_prefs:     true preferences of this agent
            rep_prefs:      reported preferences of this agent

'''
class Agent:
    def __init__(self):
        # TODO some sort of check against existing identities to prevent
        # sybil or whitewashing attacks
        self.rep = 1.0
        self.item = None

    def init_preferences(self, prefs):
        self.true_prefs = prefs
        self.rep_prefs = prefs

    def report(self):
        return self.rep_prefs

    def truncate(self, reported = True):
        try:
            if reported:
                assert item in self.true_prefs
            else:
                assert item in self.rep_prefs
        except AssertionError:
            raise ValueError("Prefs must be complete")