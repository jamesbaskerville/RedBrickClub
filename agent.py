import secrets

'''
    Agent:
    A participant in the item exchange market.

    Attributes:
    token:          unique, anonymous identifier
    email:          email address
    house:          house affiliation
    mailbox:        house mailbox number
    rep:            reputation score

    unseen:         set of items in a round the user has yet to rank
    nitems:         the total number of items in a round
    pref_order:     the items that the user has ranked, in order
'''
class Agent:
    def __init__(self, email, house, mailbox):
        # TODO some sort of check against existing identities to prevent
        # sybil or whitewashing attacks
        self.token = secrets.token_urlsafe()
        self.email = email
        self.house = house
        self.mailbox = int(mailbox)
        self.rep = 0

    def init_preferences(self, items):
        self.unseen = set(items)
        self.nitems = len(items)
        self.pref_order = []

    # the rank of an item should be 0-indexed
    def rank_item(self, item, rank):
        if rank < 0 or rank > len(self.pref_order):
            # TODO complain
            pass

        self.pref_order.insert(rank, item)

        if item in self.unseen:
            self.unseen.remove(item)

    def get_pref_order(self):
        return self.pref_order

