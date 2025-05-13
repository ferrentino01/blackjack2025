import streamlit as st
import random

# --- Funzioni di gioco ---
def crea_mazzo():
    semi = ['♠', '♥', '♦', '♣']
    valori = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [v + s for s in semi for v in valori]

def punti(carte):
    totale = 0
    assi = 0
    for c in carte:
        v = c[:-1]
        if v in ['J', 'Q', 'K']:
            totale += 10
        elif v == 'A':
            totale += 11
            assi += 1
        else:
            totale += int(v)
    while totale > 21 and assi:
        totale -= 10
        assi -= 1
    return totale

# --- Stato iniziale ---
if 'mazzo' not in st.session_state:
    st.session_state.mazzo = random.sample(crea_mazzo(), 52)
    st.session_state.giocatore = [st.session_state.mazzo.pop()]
    st.session_state.banco = [st.session_state.mazzo.pop()]
    st.session_state.fine = False

# --- Interfaccia ---
st.title("🃏 Blackjack Semplice")
st.write(f"**Le tue carte**: {', '.join(st.session_state.giocatore)} (Totale: {punti(st.session_state.giocatore)})")
st.write(f"**Carta visibile del banco**: {st.session_state.banco[0]}")

# --- Gioca ---
if not st.session_state.fine:
    if st.button("Pesca una carta"):
        st.session_state.giocatore.append(st.session_state.mazzo.pop())
        if punti(st.session_state.giocatore) > 21:
            st.session_state.fine = True
            st.error("Hai sballato! 💥")
    if st.button("Stai"):
        while punti(st.session_state.banco) < 17:
            st.session_state.banco.append(st.session_state.mazzo.pop())
        st.session_state.fine = True

# --- Risultato finale ---
if st.session_state.fine:
    punteggio_gioc = punti(st.session_state.giocatore)
    punteggio_banco = punti(st.session_state.banco)

    st.write(f"**Carte del banco**: {', '.join(st.session_state.banco)} (Totale: {punteggio_banco})")
    if punteggio_gioc > 21:
        st.write("Hai perso 😭")
    elif punteggio_banco > 21 or punteggio_gioc > punteggio_banco:
        st.write("Hai vinto! 🥳")
    elif punteggio_gioc < punteggio_banco:
        st.write("Hai perso 😭")
    else:
        st.write("Pareggio 😐")

    if st.button("Nuova partita"):
        st.session_state.clear()

