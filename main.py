from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
import random

set_website_title("Blackjack Player")
set_site_information(
    author="Ryan Bachman",
    description="Plays an accurate game of blackjack",
    sources="Thanks to the Drafter docs and Mr. Peck",
    planning=[""],
    links=["https://github.com/ryanbach44/blackjack-player"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Deck:
    deck: list[str]
    
@dataclass
class State:
    total_points: int
    num_decks: int
    card_decks: list[Deck]
    player_cards: str
    dealer_cards: str

def rand(start: int, stop: int) -> int:
    """
    Generates a random number
    
    Args:
        start: int, the starting number to pick from
        stop: int, the ending number to pick from
        
    Returns:
        a random number from 'start' to 'stop'
    """
    return random.randint(start, stop)

def make_deck() -> Deck:
    """
    Makes a single deck of 52 cards, 2-A for every suit
    
    Args:
        None, it operates alone
        
    Returns:
        A singular deck of cards as a list[str] attributed to the Deck class
    """
    deck = []
    suits = "♠♥♣♦"
    for suit in suits:
        for num in range(1, 14):
            if num >=2 and num <=10:
                deck.append(str(num) + suit)
            if num == 1:
                deck.append("A" + suit)
            if num == 11:
                deck.append("J" + suit)
            if num ==12:
                deck.append("Q" + suit)
            if num == 13:
                deck.append("K" + suit)
    return Deck(deck)

def make_decks(num_of_decks: int) -> list[Deck]:
    """
    Makes multiple decks of cards
    
    Args:
        num_of_decks: int, the number of decks the player wishes to make entered
                            entered at the beginning so the when the cards run out
                            they can be reshuffled to the same num of decks
                    
    Returns:
        A list of decks of the Deck class
    """
    total_decks = []
    for deck in range(0,num_of_decks):
        total_decks.append(make_deck())
    return total_decks

def give_cards(state: State) -> str:
    """
    Gives out one hand of two cards and then deletes those cards
    from the running list of Decks so the cards can't be drawn twice
    
    Args:
        state: State, the state attribute which will give the Decks
                to be drawn from and where to remove the cards
    
    Returns:
        a str that contains two cards, their values and their suits
    """
    deck1 = rand(0,len(state.card_decks)-1)
    
    while len(state.card_decks[deck1].deck)-1 == -1:
        del state.card_decks[deck1]
        
        if len(state.card_decks) < 1:
            state.card_decks = make_decks(state.num_decks)
            
        deck1 = rand(0,len(state.card_decks)-1)
        
    card1 = rand(0,len(state.card_decks[deck1].deck)-1)
    
    cards = state.card_decks[deck1].deck[card1]
    del state.card_decks[deck1].deck[card1]

    return cards

def hand_score(hand: str) -> int:
    """
    Determines the score of a hand based on Blackjack scoring standards,
    2-9 is its value, 10-K is 10, Ace can be 1 or 11
    
    Args:
        hand: str, a hand of two cards, strips the suit character and uses
                    conditions to determine the overall score of the hand
    
    Returns:
        The hand's score as an int
    """
    score = 0
    for card in hand:
        if card.isdigit():
            if int(card) == 1:
                score += 10
                continue
            else:
                score += int(card)
                continue
        if card not in "♠♥♣♦" and card != "A":
            score += 10
    if hand.count("A") == 1 and score < 11:
        score += 11
    elif hand.count("A") == 1 and score >= 11:
        score += 1
    elif hand.count("A") == 2 and score <= 9:
        score += 12
    elif hand.count("A") == 2 and score > 9:
        score += 2
    elif hand.count("A") > 2:
        score += (hand.count("A")-2)
    return score
assert_equal(hand_score("5♠10♣"), 15)
assert_equal(hand_score("10♠A♣"), 21)
assert_equal(hand_score("5♠A♣"), 16)
assert_equal(hand_score("4♠10♣5♠A♣"), 20)
    
@route
def index(state: State) -> Page:
    """
    The first page the player sees at the beginning og a new game
    
    Args:
        state: State, state variables to be defined through the game
        
    Returns:
        A page allowing the player to set the decks and make an inital wager
    """
    state.total_points = 1000
    state.num_decks = 0
    state.card_decks = [[]]
    return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                [Header("Blackjack ♠♥♣♦"),
                "Total Points: " + str(state.total_points) + "\n",
                "Number of Decks: ",
                 TextBox("deck_num"),
                "\nWager: ",
                TextBox("wager"),
                Button("Deal", "deal"),
                "\n",
                Button("How To Play","rules")
                ])
assert_equal(index(State(1000, 0, [], "", "")), Page(State(1000, 0, [[]], "", ""),
                                                        [Header("Blackjack ♠♥♣♦"),
                                                        "Total Points: 1000\n",
                                                        "Number of Decks: ",
                                                         TextBox("deck_num"),
                                                        "\nWager: ",
                                                        TextBox("wager"),
                                                        Button("Deal", "deal"),
                                                        "\n",
                                                        Button("How To Play","rules")
                                                        ])
             )

@route
def new_game_win(state: State) -> Page:
    """
    The page the player sees when they win an individual hand
    
    Args:
        state: State, state variables to show the player and start the next hand
        
    Returns:
        A Page congradulating the player and giving them the option to play agian or stop
    """
    
    return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                [Header("Blackjack ♠♥♣♦"),
                "You win!\n" +
                "Your Cards: " + state.player_cards + "\n" +
                "Dealer Cards: " + state.dealer_cards + "\n" +
                "Total Points: " + str(state.total_points) + "\n",
                "\nWager: ",
                TextBox("wager"),
                Button("Deal", "deal", [Argument("deck_num", str(state.num_decks))]),
                Button("End Game", "finish")
                ])
assert_equal(new_game_win(State(1000, 2, [[]], "2♠5♦", "4♥6♣")), Page(State(1000, 2, [[]], "", ""),
                                                                [Header("Blackjack ♠♥♣♦"),
                                                                "You win!\n" +
                                                                "Your Cards: 2♠5♦\n" +
                                                                "Dealer Cards: 4♥6♣\n" +
                                                                "Total Points: 1000\n",
                                                                "\nWager: ",
                                                                TextBox("wager"),
                                                                Button("Deal", "deal", [Argument("deck_num", 2)]),
                                                                Button("End Game", "finish")
                                                                ])
             )

@route
def new_game_loss(state: State) -> Page:
    """
    The page the player sees when they lose an individual hand
    
    Args:
        state: State, state variables to show the player and start the next hand
        
    Returns:
        A Page telling the player they lost and gives them the option to play agian or stop
    """
    return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                [Header("Blackjack ♠♥♣♦"),
                "You lost :(\n" +
                "Your Cards: " + state.player_cards + "\n" +
                "Dealer Cards: "+ state.dealer_cards + "\n" +
                "Total Points: " + str(state.total_points) + "\n",
                "\nWager: ",
                TextBox("wager"),
                Button("Deal", "deal", [Argument("deck_num", str(state.num_decks))]),
                Button("End Game", "finish")
                ])
assert_equal(new_game_loss(State(1000, 2, [[]], "2♠5♦", "4♥6♣")), Page(State(1000, 2, [[]], "", ""),
                                                                        [Header("Blackjack ♠♥♣♦"),
                                                                        "You lost :(\n" +
                                                                        "Your Cards: 2♠5♦\n" +
                                                                        "Dealer Cards: 4♥6♣\n" +
                                                                        "Total Points: 1000\n",
                                                                        "\nWager: ",
                                                                        TextBox("wager"),
                                                                        Button("Deal", "deal", [Argument("deck_num", 2)]),
                                                                        Button("End Game", "finish")
                                                                        ])
             )
             
@route
def new_game_push(state: State) -> Page:
    """
    The page the player sees when they tie an individual hand
    
    Args:
        state: State, state variables to show the player and start the next hand
        
    Returns:
        A Page telling the player nothing happened and gives them the option to play agian or stop
    """
    return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                [Header("Blackjack ♠♥♣♦"),
                "Push, Try Again\n" +
                "Your Cards: " + state.player_cards + "\n" +
                "Dealer Cards: "+ state.dealer_cards + "\n" +
                "Total Points: " + str(state.total_points) + "\n",
                "\nWager: ",
                TextBox("wager"),
                Button("Deal", "deal", [Argument("deck_num", str(state.num_decks))]),
                Button("End Game", "finish")
                ])
assert_equal(new_game_push(State(1000, 2, [[]], "2♠8♦", "4♥6♣")), Page(State(1000, 2, [[]], "", ""),
                                                                        [Header("Blackjack ♠♥♣♦"),
                                                                        "Push, Try Again" + "\n" +
                                                                        "Your Cards: 2♠8♦\n" +
                                                                        "Dealer Cards: 4♥6♣\n" +
                                                                        "Total Points: 1000\n",
                                                                        "\nWager: ",
                                                                        TextBox("wager"),
                                                                        Button("Deal", "deal", [Argument("deck_num", 2)]),
                                                                        Button("End Game", "finish")
                                                                        ])
             )


@route
def rules(state: State) -> Page:
    "Returns a standard Rules page for how to play blackjack"
    return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                 [Header("How to Play Blackjack ♠♥♣♦"),
                 "Goal: Beat the dealer's hand without going over 21\n\n" +
                 "Gameplay:\n\t1. You will be dealt 2 cards, 2-A\n" +
                 "2. Each card has a different point value\n"+
                 "- 2-10 is worth its value\n\t- J, Q, K are worth 10\n"+
                 "- A can be worth 1 or 11, whichever gets you the most usable points\n"+
                 "3. You will then be shown one of the dealer's cards\n" +
                 "4. Based on what you see you can either hit for another\n"+
                 "   card or stand and see if you beat the dealer\n"+
                 "5. If you're really confident you can double down which doubles\n"+
                 "   your wager and auto deals you one more card before standing\n"+
                 "6. Once you stand, the dealer will deal cards to try and beat you\n"+
                 "   until their score is at or above 17\n"+
                 "7. Both hands will be scored and whoever has closest to 21 without\n"+
                 "   going over wins the hand\n"+
                 "8. You'll either win your wager, lose it, or tie and nothing changes\n"+
                 "9. You may then play another hand or end the game and see your net score\n"+
                 "Good Luck!",
                 Button("Back", "index")])


@route
def deal(state: State, deck_num: str, wager: str) -> Page:
    """
    (can't unit test, uses random)
    Deals out two random cards from a number of decks decided by the player,
    reshuffles the decks if there are no cards left and then deals, returns two
    speacial pages if the wager is too high, one if there is no wager returns
    automatic wins or losses if either the player or dealer is dealt 21, otherwise
    returns a page where the player can hit, stand, or double down
    
    Args:
        state: State, state variables that can be used or changed in the function
        deck_num: str, whatever the player types into the deck_num field, function determines validity
                        and if valid, sets how many decks to be dealt
        wager: str, whatever the player types into the wager field, function determines validity
                    and if valid, sets the running wager for that one hand
                    
    Returns:
        Can return certain error pages depending on user input or immediate wins and losses if
        player or dealer is dealt 21, otherwise shows the player the cards and allows hit or stand
    """
    if deck_num == "" or not deck_num.isdigit():
        return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                    [Header("Blackjack ♠♥♣♦"),
                    "Invalid Decks, Try Again\n" +
                    "Total Points: " + str(state.total_points) + "\n",
                    "\nNumber of Decks: ",
                    TextBox("deck_num"),
                    Button("Deal", "deal", [Argument("wager", str(wager))])
                    ])
    else :
        deck_num = int(deck_num)
    
    if wager == "" or not wager.isdigit() or int(wager) <= 0:
        return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                    [Header("Blackjack ♠♥♣♦"),
                    "Invalid Wager, Try Again\n" +
                    "Total Points: " + str(state.total_points) + "\n",
                    "\nWager: ",
                    TextBox("wager"),
                    Button("Deal", "deal", [Argument("deck_num", str(deck_num))])
                    ])
    else:
        wager = int(wager)
        
    if state.num_decks < 1:
        if deck_num > 25:
            state.num_decks = 25
        elif deck_num < 1:
            state.num_decks = 1
        else:
            state.num_decks = deck_num
        state.card_decks = make_decks(state.num_decks)
        
    if wager > state.total_points:
        return Page(State(state.total_points, state.num_decks, state.card_decks, "", ""),
                    [Header("Blackjack ♠♥♣♦"),
                    "Not Enough Points, Try Again\n" +
                    "Total Points: " + str(state.total_points) + "\n",
                    "\nWager: ",
                    TextBox("wager"),
                    Button("Deal", "deal", [Argument("deck_num", state.num_decks)])
                    ])
    
    state.player_cards = give_cards(state) + give_cards(state)
    state.dealer_cards = give_cards(state) + give_cards(state)
    
    if hand_score(state.player_cards) == 21:
        state.total_points += wager
        return new_game_win(state)
    
    if hand_score(state.dealer_cards) == 21:
        state.total_points -= wager
        return new_game_loss(state)
    
    if state.total_points - wager*2 < 0 :
        return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                    [Header("Blackjack ♠♥♣♦"),
                     "Your Cards: " + state.player_cards + "\n" +
                     "Dealer Cards: X" + state.dealer_cards[-int((len(state.dealer_cards)/2+.5)):] + "\n",
                     Button("Hit", "hit", [Argument("wager", wager)]),
                     Button("Stand", "stand", [Argument("wager", wager)])
                        ])
    
    return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                [Header("Blackjack ♠♥♣♦"),
                 "Your Cards: " + state.player_cards + "\n" +
                 "Dealer Cards: X" + state.dealer_cards[-int((len(state.dealer_cards)/2+.5)):] + "\n",
                 Button("Hit", "hit", [Argument("wager", wager)]),
                 Button("Stand", "stand", [Argument("wager", wager)]),
                 Button("Double Down", "double", [Argument("wager", wager)])
                    ])

@route
def hit(state: State, wager: int) -> Page:
    """
    (Can't unit test, uses random)
    Adds one random card to the player's hand and then calculates the score of the hand
    to determine if the player has busted or is still under 21 and can hit again.
    
    Args:
        state: State, state variables to be used or changed in the function
        wager: int, whatever the running wager is for that hand
        
    Returns:
        The loss page if their hand goes over 21 after a hit, or a page allowing to hit or stand
    """
    state.player_cards += give_cards(state)
    score_player = hand_score(state.player_cards)
    
    if score_player <= 21:
        return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                    [Header("Blackjack ♠♥♣♦"),
                     "Your Cards: " + state.player_cards + "\n" +
                     "Dealer Cards: X" + state.dealer_cards[-int((len(state.dealer_cards)/2+.5)):] + "\n",
                     Button("Hit", "hit", [Argument("wager", wager)]),
                     Button("Stand", "stand", [Argument("wager", wager)])
                        ])
    
    state.total_points -= wager
    return new_game_loss(state)

@route
def stand(state: State, wager: int) -> Page:
    """
    (Unit test only applies to cases where the score of the dealer hand
        is >=17 because if it is less, the dealer starts taking random cards)
        
    Args:
        state: State, state variables to be used or changed in the function
        wager: int, whatever the running wager is for that hand
    
    Returns:
        Either the win, loss, or push pages depending on how the scores for player and dealer come out
    """
    score_player = hand_score(state.player_cards)
    score_dealer = hand_score(state.dealer_cards)
    if score_player > 21:
        state.total_points -= wager
        return new_game_loss(state)
    
    if score_dealer > 21:
        state.total_points += wager
        return new_game_win(state)
    
    if score_dealer >=17 and score_player > score_dealer:
        state.total_points += wager
        return new_game_win(state) 
    
    if score_dealer >=17 and score_player < score_dealer:
        state.total_points -= wager
        return new_game_loss(state)
    
    if score_dealer < 17:
        while score_dealer < 17:
            state.dealer_cards += give_cards(state)
            score_dealer = hand_score(state.dealer_cards)
            
    if score_dealer > 21:
        state.total_points += wager
        return new_game_win(state)
    
    if score_player > score_dealer:
        state.total_points += wager
        return new_game_win(state)
    
    if score_player < score_dealer:
        state.total_points -= wager
        return new_game_loss(state)
    
    return new_game_push(state)

assert_equal(stand(State(1000, 2, [[]], "2♠5♦", "10♥7♣"), 100), Page(State(900, 2, [[]], "", ""),
                                                                        [Header("Blackjack ♠♥♣♦"),
                                                                        "You lost :(\n" +
                                                                        "Your Cards: 2♠5♦\n" +
                                                                        "Dealer Cards: 10♥7♣\n" +
                                                                        "Total Points: 900\n",
                                                                        "\nWager: ",
                                                                        TextBox("wager"),
                                                                        Button("Deal", "deal", [Argument("deck_num", 2)]),
                                                                        Button("End Game", "finish")
                                                                        ])
             )
assert_equal(stand(State(1000, 2, [[]], "10♠9♦", "10♥7♣"), 100), Page(State(1100, 2, [[]], "", ""),
                                                                        [Header("Blackjack ♠♥♣♦"),
                                                                        "You win!\n" +
                                                                        "Your Cards: 10♠9♦\n" +
                                                                        "Dealer Cards: 10♥7♣\n" +
                                                                        "Total Points: 1100\n",
                                                                        "\nWager: ",
                                                                        TextBox("wager"),
                                                                        Button("Deal", "deal", [Argument("deck_num", 2)]),
                                                                        Button("End Game", "finish")
                                                                        ])
             )

@route
def double(state: State, wager: int):
    """
    (Can't unit test, deals out one more random card
    and then forces the player to stand, doubling their wager)
    
    Args:
        state: State, state variables to be used or changed in the function
        wager: int, whatever the running wager is for that hand
        
    Returns:
        An immediate win, loss, or push depending on how their score turns out after one new card 
    """
    state.player_cards += give_cards(state)
    return stand(state, wager*2)

@route
def finish(state: State):
    """
    The page that returns when the player is done playing and wants to cash out their points
    
    Args:
        tate: State, state variables to be used or changed in the function
        wager: int, whatever the running wager is for that hand
        
    Returns:
        A page depending on whether the player had a net gain, loss or nothing in points
    """
    if (state.total_points - 1000) > 0:
        return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                    [Header("Blackjack ♠♥♣♦"),
                     "Good Game!\nYour Score: " + str(state.total_points - 1000) + "\n",
                     Button("Play Again?", "index")
                            ])
    if (state.total_points - 1000) == 0:
        return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                    [Header("Blackjack ♠♥♣♦"),
                     "Thanks For Playing!\nYour Score: " + str(state.total_points - 1000) + "\n",
                     Button("Play Again?", "index")
                            ])

    return Page(State(state.total_points, state.num_decks, state.card_decks, state.player_cards, state.dealer_cards),
                    [Header("Blackjack ♠♥♣♦"),
                     "Better Luck Next Time!\nYour Score: " + str(state.total_points - 1000) + "\n",
                     Button("Play Again?", "index")
                            ])
assert_equal(finish(State(1100, 2, [[]], "", "")), Page(State(1100, 2, [[]], "", ""),
                                                        [Header("Blackjack ♠♥♣♦"),
                                                         "Good Game!\nYour Score: 100\n",
                                                         Button("Play Again?", "index")
                                                                ]))
assert_equal(finish(State(1000, 2, [[]], "", "")), Page(State(1000, 2, [[]], "", ""),
                                                        [Header("Blackjack ♠♥♣♦"),
                                                         "Thanks For Playing!\nYour Score: 0\n",
                                                         Button("Play Again?", "index")
                                                                ]))
assert_equal(finish(State(900, 2, [[]], "", "")), Page(State(900, 2, [[]], "", ""),
                                                        [Header("Blackjack ♠♥♣♦"),
                                                         "Better Luck Next Time!\nYour Score: -100\n",
                                                         Button("Play Again?", "index")
                                                                ]))
    
start_server(State(1000, 0, [[]], "", ""))

