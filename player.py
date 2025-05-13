class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def calculate_points(self):
        points = sum(card.get_points() for card in self.hand)
        # gestisci asso come 1 se necessario
        aces = sum(1 for card in self.hand if card.value == 'A')
        while points > 21 and aces:
            points -= 10
            aces -= 1
        return points

    def show_hand(self, hide_first=False):
        if hide_first:
            return "[??] " + " ".join(str(c) for c in self.hand[1:])
        return " ".join(str(c) for c in self.hand)
