import pygame
import pygame_gui

class infoWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        super().__init__((pos),
                         manager,
                         window_display_title='How to Play Poker',
                         object_id='#info_window',
                         draggable=True)
        self.scroll_box = pygame_gui.elements.UITextBox("""Welcome to the World of INSERT_GAME_TITLE!
Get ready to dive into a high risk, high reward game of INSERT_GAME_TITLE – where fortunes are made, bluffs are called, and every card is a potential game-changer.

Chapter 1: Setting the Stage
Imagine a grand table surrounded by competitive players like yourself. Each player is dealt two private cards, known as the "Hole Cards."

Chapter 2: The Blinds
Before the first card even thinks about hitting the table, two players must make a small blind and a big blind bet. It's like tossing a couple of coins into the poker cauldron, stirring up the excitement for the round.

Chapter 3: Flop, Turn, River
Now, the dealer reveals three community cards - the "Flop." Witness the magic unfold! A fourth card, the "Turn," appears, followed by the final community card, the "River." These cards are unexpected and unpredictable - you never know what's coming next!

Chapter 4: The Art of Betting
As the cards unveil their secrets, it's time to put your chips where your bravado is. You can bet, check, raise, or fold. Bluffing is encouraged - just don't get caught with a bad hand!

Chapter 5: Showdown
The moment of truth! Show your Hole Cards and let the best hand win. Is it a royal flush or just a pair of socks? Only one way to find out.

Chapter 6: Winning the Pot
If your hand trumps the rest, you snatch the pot of gold (or chips, in this case) right from under their noses. If your hand loses, say goodbye to the money you've put in the pot. But don't worry, there's still ways to win it back!

Chapter 7: Rinse and Repeat
The thrill doesn't stop! Shuffle the deck, deal the cards, and let the poker frenzy continue. The more you play, the more you'll master the art of reading opponents, crafting killer strategies, and taking big risks!

Congratulations, you've now learned the basics of Poker - where luck meets skill, and every game is unpredictable. May the cards be ever in your favor!""",
                                                            relative_rect=pygame.Rect((0.000001 * pos.width, 0.02 * pos.height), (0.875 * pos.width, 0.825 * pos.height)),
                                                            manager=manager,
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                            "centerx": "centerx"
                                                            })
        # pygame_gui.elements.UIScrollingContainer(pygame.Rect((100, 200), (300, 200)),
        #                                                                                      manager=manager,
        #                                                                                      container=self
        # )
    #     self.info_label = pygame_gui.elements.UILabel(pygame.Rect((1, 1), (1, 1)),
    #                                                   "",
    #                                                   manager=manager,
    #                                                   container=self.scroll_box
    #     )
    # def load_text(self, file_path):
    #     try:
    #         with open(file_path, 'r') as file:
    #             text = file.read()
    #             self.info_label.set_text(text)
    #             self.scroll_box.set_dimensions((400, 400))
    #     except FileNotFoundError:
    #         print(f"File not found: {file_path}")