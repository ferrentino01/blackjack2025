import streamlit as st
import random

# --- CLASSI ---
class Card:
    def __init__(self, suit, value):
        self.suit = suit  # '♠', '♥', '♦', '♣'
        self.value = value  # '2'–'10', 'J', 'Q', 'K', 'A'

    def get_points(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)

    def __str__(self):
        return f"{self.value}{self.suit}"


class Deck:
    def __init__(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand = []

    def get_points(self):
        total = 0
        aces = 0
        for card in self.hand:
            pts = card.get_points()
            total += pts
            if card.value == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total


# --- FUNZIONI DI STATO ---
def reset_game():
    st.session_state.deck = Deck()
    st.session_state.player = Player("Player")
    st.session_state.dealer = Player("Dealer")
    st.session_state.game_over = False
    st.session_state.message = ""
    for _ in range(2):
        st.session_state.player.add_card(st.session_state.deck.draw())


# --- INIZIALIZZAZIONE ---
if "player" not in st.session_state:
    reset_game()

# --- UI ---
st.title("🃏 Blackjack")

player = st.session_state.player
deck = st.session_state.deck

st.subheader("Le tue carte:")
st.write(" - ".join(str(c) for c in player.hand))
st.write(f"Totale punti: **{player.get_points()}**")

# --- BOTTONE PESCA ---
if not st.session_state.game_over:
    if st.button("Pesca una carta"):
        new_card = deck.draw()
        player.add_card(new_card)
        st.success(f"Hai pescato: {new_card}")
        if player.get_points() > 21:
            st.session_state.game_over = True
            st.session_state.message = "💥 Hai sballato! Hai perso."

# --- RISULTATO ---
if st.session_state.game_over:
    st.error(st.session_state.message)

# --- RESET ---
if st.button("🔄 Nuova partita"):
    reset_game()
