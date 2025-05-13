class Card:
    def __init__(self, suit, value):
        self.suit = suit  # '♠', '♥', '♦', '♣'
        self.value = value  # '2'–'10', 'J', 'Q', 'K', 'A'

    def get_points(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11  # il valore potrà essere adattato a 1 durante il gioco
        else:
            return int(self.value)

    def __str__(self):
        return f"{self.value}{self.suit}"
