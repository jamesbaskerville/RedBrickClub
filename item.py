from user import User
'''
    Item:
        An item in the exchange market.

        Attributes:
            token:          (URL-safe) unique identifier
            user:           user that owns this item
            description:    text description of this item
'''
class Item:
    # Params:
    #   user_token: (string) token of owning user
    #   description: (string) text description
    def __init__(self, user_token, description):
        self.token = secrets.token_urlsafe()
        self.user = User.find_by_user_token(user_token)
        self.description = description

    def add_or_replace_description(self, description):
        self.description = description

    def add_picture(self, picture):
        # TODO ???
        raise NotImplemented
