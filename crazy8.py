# Michel, Adant, C1176

import copy
import math
import random


class LinkedList:
    class _Node:
        def __init__(self, v, n):
            self.value = v
            self.next = n

    def __init__(self):
        self._head = None
        self._size = 0

    def __str__(self):
        chaine = "["
        current_node = self._head
        for i in range(self._size):
            chaine += str(current_node.value) + ", "
            current_node = current_node.next
        return chaine.strip(", ") + "]"

    def __len__(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    # Adds a node of value v to the beginning of the list
    def add(self, v):
        self._head = self._Node(v, self._head)
        self._size += 1

    # Adds a node of value v to the end of the list
    def append(self, v):
        current_node = self._head
        if not self.isEmpty():
            while current_node.next:
                current_node = current_node.next
            current_node.next = self._Node(v, current_node.next)
            self._size += 1
        else:
            self.add(v)

    # Removes and returns the first node of the list
    def pop(self):
        if self.isEmpty():
            return None
        head = self._head
        self._head = self._head.next
        self._size -= 1
        return head.value

    # Returns the value of the first node of the list
    def peek(self):
        if self.isEmpty():
            return None
        return self._head.value

    # Removes the first node of the list with value v and return v
    def remove(self, v):
        if not self.isEmpty():
            previous_node = None
            current_node = self._head
            while current_node:
                if current_node.value == v:
                    self._size -= 1
                    if previous_node:
                        previous_node.next = current_node.next
                        return current_node.value
                    else:  # si c'est le premier élément de la liste
                        self._head = current_node.next
                        return current_node.value
                previous_node = current_node
                current_node = current_node.next
        return None  # n'a pas trouvé la valeur


class CircularLinkedList(LinkedList):
    def __init__(self):
        super().__init__()  # contient: ._head et ._size

    def __str__(self):
        return super().__str__()

    def __iter__(self):
        current_node = self._head
        for i in range(self._size):
            yield current_node.value
            current_node = current_node.next

    # Moves head pointer to next node in list
    def next(self):
        if self.isEmpty():
            raise Exception("List is empty")
        self.append(self._head.value)
        self._head = self._head.next
        self._size -= 1  # append fait croitre le size, donc on doit compenser

    # Adds a node of value v to the end of the list
    def append(self, v):
        super().append(v)

    # Reverses the next pointers of all nodes to previous node
    def reverse(self):
        if self._size > 2:  # inverser n'a du sens que pour une liste > 2
            previous_node = None
            current_node = self._head.next
            next_node = current_node.next
            while next_node:
                current_node.next = previous_node
                previous_node = current_node
                current_node = next_node
                next_node = next_node.next
            current_node.next = previous_node
            self._head.next = current_node

    # Removes head node and returns its value
    def pop(self):
        return super().pop()


class Card:
    def __init__(self, r, s):
        self._rank = r
        self._suit = s

    # spades (pique), hearts (coeur), diamonds (carreau), clubs (trèfle)
    suits = {'s': '\U00002660', 'h': '\U00002661', 'd': '\U00002662', 'c': '\U00002663'}

    def __str__(self):
        return self._rank + self.suits[self._suit]

    def __eq__(self, other):
        rank_equal = self._rank == other._rank
        suit_equal = self._suit == other._suit
        #S'il s'agit d'un 1 ou As:
        if self._rank in "1A" and other._rank in "1A":
            rank_equal = True

        #Si on ne précise que certains critères de comparaison:
        if other._rank and other._suit:
            return rank_equal and suit_equal
        elif other._rank:
            return rank_equal
        elif other._suit:
            return suit_equal


class Hand:
    def __init__(self):
        self.cards = {'s': LinkedList(), 'h': LinkedList(), 'd': LinkedList(), 'c': LinkedList()}

    def __str__(self):
        result = ''
        for suit in self.cards.values():
            result += str(suit)
        return result

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        result = 0
        for suit in list(self.cards):
            result += len(self.cards[suit])

        return result

    def add(self, card):
        self.cards[card._suit].add(card)

    def get_most_common_suit(self):
        return max(list(self.cards), key=lambda x: len(self[x]))

    # Returns a card included in the hand according to
    # the criteria contained in *args and None if the card
    # isn't in the hand. The tests show how *args must be used.
    def play(self, *args):
        rank = None
        suit = None
        for arg in args:
            if arg in "shdc": suit = arg
            if arg in "A12345678910JQK": rank = arg
        if rank and suit:
            return self.cards[suit].remove(Card(rank, suit))
        elif rank:
            for s in self.cards:
                c = self.cards[s].remove(Card(rank,None))
                if c: return c
        else:
            return self.cards[suit].pop()



class Deck(LinkedList):
    def __init__(self, custom=False):
        super().__init__()
        if not custom:
            # for all suits
            for i in range(4):
                # for all ranks
                for j in range(13):
                    s = list(Card.suits)[i]
                    r = ''
                    if j == 0:
                        r = 'A'
                    elif j > 0 and j < 10:
                        r = str(j+1)
                    elif j == 10:
                        r = 'J'
                    elif j== 11:
                        r = 'Q'
                    elif j == 12:
                        r = 'K'
                    self.add(Card(r,s))

    def draw(self): #Piger
        return self.pop()

    def shuffle(self, cut_precision = 0.05):
        if self._size > 1:
            # Cutting the two decks in two
            center = len(self) / 2
            k = round(random.gauss(center, cut_precision*len(self)))

            # other_deck must point the kth node in self
            # (starting at 0 of course)
            other_deck = Deck()
            other_deck._head = self._head
            other_deck._size = self._size - k
            self._size = k
            last_card_deck = None

            # Separate both lists
            #Trouver le k ième noeud:
            for i in range(k):
                #Trouver la dernière carte du premier paquet
                if i == k-1:
                    last_card_deck = other_deck._head
                #Déplace la tête du deuxième paquet à la bonne position
                other_deck._head = other_deck._head.next
            last_card_deck.next = None


            # Merging the two decks together
            if random.uniform(0,1) < 0.5:
                #switch self._head and other_deck pointers and size !
                old_self_head = self._head
                self._head = other_deck._head
                other_deck._head = old_self_head

                old_self_size = self._size
                self._size = other_deck._size
                other_deck._size = old_self_size

            if self.isEmpty() or other_deck.isEmpty(): return

            #On entrelace les noeuds ensemble:
            else:
                current_self_node = self._head
                next_self_node = self._head.next

                current_other_node = other_deck._head
                next_other_node = other_deck._head.next

                while current_self_node and current_other_node:
                    current_self_node.next = current_other_node
                    if next_self_node:
                        current_other_node.next = next_self_node

                    current_self_node = next_self_node
                    current_other_node = next_other_node

                    if next_self_node and next_other_node:
                        next_self_node = next_self_node.next
                        next_other_node = next_other_node.next
                    else:
                        break

                self._size = self._size + other_deck._size

class Player():
    def __init__(self, name, strategy='naive'):
        self.name = name
        self.score = 8
        self.hand = Hand()
        self.strategy = strategy

    def __str__(self):
        return self.name

    # This function must modify the player's hand,
    # the discard pile, and the game's declared_suit 
    # attribute. No other variables must be changed.
    # The player's strategy can ONLY be based
    # on his own cards, the discard pile, and
    # the number of cards his opponents hold.
    def play(self, game):
        if(self.strategy == 'naive'):
            top_card = game.discard_pile.peek() #Sommet du talon
            score = game.players.peek().score

            #Fonctions auxiliaires

            #Joue la carte sur le talon ou ne fait rien si pas de carte
            def jouer_carte(card, game):
                if card:
                    deux_ou_qs(card)
                    game.discard_pile.add(card)
                    #Vérifier si la carte provoque une frime:
                    if card == Card(str(score), None):
                        game.declared_suit = self.hand.get_most_common_suit()
                return game

            #Renvoie carte de la même enseigne sans frime ou None:
            def enseigne_sans_frime(enseigne):
                frime = None
                selection = self.hand.play(enseigne)
                if selection and selection == Card(str(score), None):
                    frime = selection  # mettre de côté
                    selection = self.hand.play(enseigne)  # nouvelle recherche
                    self.hand.add(frime)  # remettre la frime dans le paquet
                return selection


            #Ajuste nombre de cartes à piger si Deux ou Reine de pique:
            def deux_ou_qs(card):
                if card._rank == '2':
                    game.draw_count += 2
                elif card == Card('Q','s'):
                    game.draw_count += 5

            def trouver_frime():
                card = self.hand.play(str(score))
                if card: #si on a trouvé une frime
                    game.declared_suit = self.hand.get_most_common_suit()
                else: #on ne peut rien jouer
                    game.draw_count += 1
                return card

            #Différents cas:

            #Cartes à piger, seule façon de s'en sortir, un 2 ou Qs:
            if game.draw_count > 0:
                # Cartes à piger ET une frime (enseigne spécifique à piger):
                specific_suit = game.declared_suit if game.declared_suit else 'None'
                card_to_play = self.hand.play('2', specific_suit) or \
                               self.hand.play('Q','s')
                return jouer_carte(card_to_play, game)


            #Si une frime est en vigueur:
            #On peut soit jouer l'enseigne, ou faire une frime
            if game.declared_suit:
                card_to_play = enseigne_sans_frime(game.declared_suit)
                if card_to_play:
                    game.declared_suit = ''
                else:
                    card_to_play = trouver_frime()
                return jouer_carte(card_to_play, game)


            #Pas de frimes en vigueur, pas de cartes à piger:
            #Essayer d'abord enseigne, puis rang, puis frime:
            card_to_play = enseigne_sans_frime(top_card._suit)
            if not card_to_play:
                card_to_play = self.hand.play(top_card._rank)
            if not card_to_play:
                card_to_play = trouver_frime()
            return jouer_carte(card_to_play, game)

        else:
            # TO DO(?): Custom strategy (Bonus)
            pass


class Game:
    def __init__(self):
        self.players = CircularLinkedList()

        for i in range(1,5):
            self.players.append(Player('Player ' + str(i)))

        self.deck = Deck()
        self.discard_pile = LinkedList()

        self.draw_count = 0
        self.declared_suit = ''

    def __str__(self):
        result = '--------------------------------------------------\n'
        result += 'Deck: ' + str(self.deck) + '\n'
        result += 'Declared Suit: ' + str(self.declared_suit) + ', '
        result += 'Draw Count: ' + str(self.draw_count) + ', '
        result += 'Top Card: ' + str(self.discard_pile.peek()) + '\n'

        for player in self.players:
            result += str(player) + ': '
            result += 'Score: ' + str(player.score) + ', '
            result += str(player.hand) + '\n'
        return result


    # Puts all cards from discard pile except the 
    # top card back into the deck in reverse order
    # and shuffles it 7 times
    def reset_deck(self):
        if self.discard_pile._size > 0:
            new_discard_top = self.discard_pile.pop() #nouveau top du talon
            discard_pile_size = self.discard_pile._size
            for i in range(discard_pile_size):
                self.deck.append(self.discard_pile.pop())
            #remettre le top du talon
            self.discard_pile.add(new_discard_top)
        for i in range(7):
            self.deck.shuffle()

    # Safe way of drawing a card from the deck
    # that resets it if it is empty after card is drawn
    def draw_from_deck(self, num, player):
        for i in range(num):
            card = self.deck.draw()
            self.draw_count -= 1
            if card:
                player.hand.add(card)
            if self.deck.isEmpty():
                self.reset_deck()

    def start(self, debug=False):
        # Ordre dans lequel les joueurs gagnent la partie
        result = LinkedList()

        self.reset_deck()

        # Each player draws 8 cards
        for player in self.players:
            for i in range(8):
                player.hand.add(self.deck.draw())

        #Ajoute le top du talon
        self.discard_pile.add(self.deck.draw())

        transcript = open('result.txt', 'w', encoding='utf-8')
        if debug:
            transcript = open('result_debug.txt', 'w', encoding='utf-8')

        while(not self.players.isEmpty()):
            if debug:
                transcript.write(str(self))

            # player plays turn
            player = self.players.peek()

            old_top_card = self.discard_pile.peek()

            self = player.play(self) #Joueur joue

            new_top_card = self.discard_pile.peek()

            # Player didn't play a card => must draw from pile
            if new_top_card == old_top_card:
                if self.draw_count > 0:
                    plural = 's' if self.draw_count > 1 else ''
                    transcript.write(str(player) + ' draws '
                                     + str(self.draw_count) + ' card'+plural+'\n')
                    self.draw_from_deck(self.draw_count, player)

            # Player played a card
            else:
                transcript.write(str(player) + ' plays ' + str(new_top_card)+'\n')

                #On inverse l'ordre des joueurs
                if new_top_card._rank == 'A':
                    self.players.reverse()

                #On saute un joueur
                if new_top_card._rank == 'J':
                    self.players.next()

            # Handling player change
            # Player has finished the game
            if len(player.hand) == 0 and player.score == 1:
                #Enlever de la liste circulaire:
                result.append(self.players.pop())
                transcript.write(player.name + ' finishes in position '
                                 + str(len(result)) + "\n")
                #S'il ne reste qu'un joueur, il finit dernier
                if len(self.players) == 1:
                    transcript.write(str(self.players.peek()) + ' finishes last')
                    result.append(self.players.pop())

            else:
                # Player is out of cards to play
                if len(player.hand) == 0:
                    transcript.write(player.name+' is out of cards to play! ')
                    player.score = player.score - 1
                    #Pige le nombre de cartes de son score:
                    plural = 's' if player.score > 1 else ''
                    transcript.write(player.name + ' draws '
                                     + str(player.score) + ' card'+plural+'\n')
                    self.draw_count += player.score
                    self.draw_from_deck(player.score, player)

                # Player has a single card left to play
                elif len(player.hand) == 1:
                    transcript.write('*Knock, knock* - '
                            + str(player) + ' has a single card left!\n')
                self.players.next()
        return result


if __name__ == '__main__':
    random.seed(420)
    game = Game()
    print(game.start(debug=True))

    # TESTS
    # LinkedList
    l = LinkedList()
    l.append('b')
    l.append('c')
    l.add('a')

    assert (str(l) == '[a, b, c]')
    assert (l.pop() == 'a')
    assert (len(l) == 2)
    assert (str(l.remove('c')) == 'c')
    assert (l.remove('d') == None)
    assert (str(l) == '[b]')
    assert (l.peek() == 'b')
    assert (l.pop() == 'b')
    assert (len(l) == 0)
    assert (l.isEmpty())

    # CircularLinkedList
    l = CircularLinkedList()
    l.append('a')
    l.append('b')
    l.append('c')

    assert (str(l) == '[a, b, c]')
    l.next()
    assert (str(l) == '[b, c, a]')
    l.next()
    assert (str(l) == '[c, a, b]')
    l.next()
    assert (str(l) == '[a, b, c]')
    l.reverse()
    assert (str(l) == '[a, c, b]')
    assert (l.pop() == 'a')
    assert (str(l) == '[c, b]')

    # Card
    c1 = Card('A', 's')
    c2 = Card('A', 's')
    # Il est pertinent de traiter le rang 1
    # comme étant l'ace
    c3 = Card('1', 's')
    assert (c1 == c2)
    assert (c1 == c3)
    assert (c3 == c2)

    # Hand
    h = Hand()
    h.add(Card('A', 's'))
    h.add(Card('8', 's'))
    h.add(Card('8', 'h'))
    h.add(Card('Q', 'd'))
    h.add(Card('3', 'd'))
    h.add(Card('3', 'c'))

    assert (str(h) == '[8♠, A♠][8♡][3♢, Q♢][3♣]')
    assert (str(h['d']) == '[3♢, Q♢]')
    assert (h.play('3', 'd') == Card('3', 'd'))
    assert (str(h) == '[8♠, A♠][8♡][Q♢][3♣]')
    assert (str(h.play('8')) == '8♠')
    assert (str(h.play('c')) == '3♣')
    assert (str(h) == '[A♠][8♡][Q♢][]')
    assert (h.play('d', 'Q') == Card('Q', 'd'))
    assert (h.play('1') == Card('A', 's'))
    assert (h.play('J') == None)

    # Deck
    d = Deck(custom=True)
    d.append(Card('A', 's'))
    d.append(Card('2', 's'))
    d.append(Card('3', 's'))
    d.append(Card('A', 'h'))
    d.append(Card('2', 'h'))
    d.append(Card('3', 'h'))

    random.seed(15)

    temp = copy.deepcopy(d)
    assert (str(temp) == '[A♠, 2♠, 3♠, A♡, 2♡, 3♡]')
    temp.shuffle()
    assert (str(temp) == '[A♠, A♡, 2♠, 2♡, 3♠, 3♡]')
    temp = copy.deepcopy(d)
    temp.shuffle()
    assert (str(temp) == '[A♡, A♠, 2♡, 2♠, 3♡, 3♠]')
    assert (d.draw() == Card('A', 's'))

