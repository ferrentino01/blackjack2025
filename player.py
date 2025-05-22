class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def calculate_points(self):
        points = 0
        aces = 0
        for card in self.hand:
            val = card.value
            if val in ['J', 'Q', 'K']:
                points += 10
            elif val == 'A':
                points += 11
                aces += 1
            else:
                points += int(val)
        while points > 21 and aces:
            points -= 10
            aces -= 1
        return points

    def show_hand(self, hide_first=False):
        if hide_first and len(self.hand) > 0:
            return "[??] " + " ".join(str(card) for card in self.hand[1:])
        else:
            return " ".join(str(card) for card in self.hand)

    def reset_hand(self):
        self.hand = []
