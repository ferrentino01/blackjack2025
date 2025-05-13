from deck import Deck
from player import Player

STARTING_BALANCE = 10000
MIN_BET = 1

def play_game(balance, stats):
    deck = Deck()
    dealer = Player("Dealer")
    player = Player("Player")

    # Inserisci la puntata
    while True:
        try:
            bet = int(input(f"Hai {balance} monete. Quanto vuoi puntare? (minimo {MIN_BET}): "))
            if MIN_BET <= bet <= balance:
                break
            else:
                print(f"Puntata non valida. Deve essere almeno {MIN_BET} e non più del tuo saldo.")
        except ValueError:
            print("Inserisci un numero intero valido.")

    # Distribuzione iniziale
    for _ in range(2):
        player.add_card(deck.draw_card())
        dealer.add_card(deck.draw_card())

    print(f"\nDealer: {dealer.show_hand(hide_first=True)}")
    print(f"{player.name}: {player.show_hand()} ({player.calculate_points()} punti)")

    # Turno del giocatore
    while player.calculate_points() < 21:
        action = input("Vuoi pescare una carta? (s/n): ")
        if action.lower() == 's':
            player.add_card(deck.draw_card())
            print(f"{player.name}: {player.show_hand()} ({player.calculate_points()} punti)")
        else:
            break

    # Turno del dealer
    while dealer.calculate_points() < 17:
        dealer.add_card(deck.draw_card())

    # Mostra mani finali
    print(f"\n--- RISULTATI FINALI ---")
    print(f"Dealer: {dealer.show_hand()} ({dealer.calculate_points()} punti)")
    print(f"{player.name}: {player.show_hand()} ({player.calculate_points()} punti)")

    # Calcolo risultato
    player_pts = player.calculate_points()
    dealer_pts = dealer.calculate_points()
    stats["giocate"] += 1

    if player_pts > 21:
        print("Hai sballato. Hai perso!")
        balance -= bet
        stats["sconfitte"] += 1
    elif dealer_pts > 21 or player_pts > dealer_pts:
        print("Hai vinto!")
        balance += bet
        stats["vittorie"] += 1
    elif player_pts == dealer_pts:
        print("Pareggio. Nessuna variazione.")
        stats["pareggi"] += 1
    else:
        print("Hai perso.")
        balance -= bet
        stats["sconfitte"] += 1

    print(f"Saldo attuale: {balance} monete")
    return balance

def mostra_statistiche(stats):
    print("\n📊 Statistiche finali:")
    print(f"Partite giocate: {stats['giocate']}")
    print(f"Vittorie: {stats['vittorie']}")
    print(f"Sconfitte: {stats['sconfitte']}")
    print(f"Pareggi: {stats['pareggi']}")

def main():
    balance = STARTING_BALANCE
    stats = {"giocate": 0, "vittorie": 0, "sconfitte": 0, "pareggi": 0}
    print("🎮 Benvenuto al Blackjack!")
    print(f"Parti con {STARTING_BALANCE} monete.")

    while balance >= MIN_BET:
        balance = play_game(balance, stats)
        if balance < MIN_BET:
            print("Non hai abbastanza monete per continuare. Fine del gioco!")
            break
        again = input("\nVuoi giocare un'altra mano? (s/n): ")
        if again.lower() != 's':
            break

    print(f"\nHai terminato con un saldo di {balance} monete. Grazie per aver giocato!")
    mostra_statistiche(stats)

if __name__ == "__main__":
    main()

