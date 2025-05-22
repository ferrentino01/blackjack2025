import streamlit as st
from deck import Deck
from player import Player

STARTING_BALANCE = 10000
MIN_BET = 1

# Inizializza session state
if "deck" not in st.session_state:
    st.session_state.deck = Deck()
    st.session_state.player = Player("Player")
    st.session_state.dealer = Player("Dealer")
    st.session_state.balance = STARTING_BALANCE
    st.session_state.bet = MIN_BET
    st.session_state.stats = {"giocate": 0, "vittorie": 0, "sconfitte": 0, "pareggi": 0}
    st.session_state.phase = "bet"

def reset_hand():
    st.session_state.deck = Deck()
    st.session_state.player.reset_hand()
    st.session_state.dealer.reset_hand()
    st.session_state.phase = "bet"

st.title("🎮 Blackjack Web App")
st.write(f"💰 Saldo attuale: {st.session_state.balance} monete")

if st.session_state.phase == "bet":
    st.subheader("Inserisci la puntata")
    bet = st.number_input("Quanto vuoi puntare?", min_value=MIN_BET, max_value=st.session_state.balance, value=MIN_BET, step=1)
    if st.button("Inizia la mano"):
        st.session_state.bet = bet
        st.session_state.player.add_card(st.session_state.deck.draw_card())
        st.session_state.dealer.add_card(st.session_state.deck.draw_card())
        st.session_state.player.add_card(st.session_state.deck.draw_card())
        st.session_state.dealer.add_card(st.session_state.deck.draw_card())
        st.session_state.phase = "play"

if st.session_state.phase == "play":
    st.subheader("🃏 Mano in corso")

    st.write(f"**Dealer**: {st.session_state.dealer.show_hand(hide_first=True)}")
    st.write(f"**Player**: {st.session_state.player.show_hand()} ({st.session_state.player.calculate_points()} punti)")

    if st.session_state.player.calculate_points() >= 21:
        st.session_state.phase = "dealer"

    if st.button("Pesca una carta"):
        st.session_state.player.add_card(st.session_state.deck.draw_card())

    if st.button("Stai"):
        st.session_state.phase = "dealer"

if st.session_state.phase == "dealer":
    while st.session_state.dealer.calculate_points() < 17:
        st.session_state.dealer.add_card(st.session_state.deck.draw_card())

    st.subheader("🎯 Risultati finali")
    dealer_pts = st.session_state.dealer.calculate_points()
    player_pts = st.session_state.player.calculate_points()

    st.write(f"**Dealer**: {st.session_state.dealer.show_hand()} ({dealer_pts} punti)")
    st.write(f"**Player**: {st.session_state.player.show_hand()} ({player_pts} punti)")

    st.session_state.stats["giocate"] += 1
    if player_pts > 21:
        st.error("Hai sballato. Hai perso!")
        st.session_state.balance -= st.session_state.bet
        st.session_state.stats["sconfitte"] += 1
    elif dealer_pts > 21 or player_pts > dealer_pts:
        st.success("Hai vinto!")
        st.session_state.balance += st.session_state.bet
        st.session_state.stats["vittorie"] += 1
    elif player_pts == dealer_pts:
        st.info("Pareggio.")
        st.session_state.stats["pareggi"] += 1
    else:
        st.error("Hai perso.")
        st.session_state.balance -= st.session_state.bet
        st.session_state.stats["sconfitte"] += 1

    st.write(f"💰 Nuovo saldo: {st.session_state.balance} monete")
    if st.session_state.balance < MIN_BET:
        st.warning("Non hai abbastanza monete per continuare.")
    else:
        if st.button("Gioca un'altra mano"):
            reset_hand()

    if st.button("Mostra statistiche finali"):
        st.subheader("📊 Statistiche")
        st.write(st.session_state.stats)
