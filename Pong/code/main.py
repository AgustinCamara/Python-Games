from settings import *
from paddle import Player, Opponent
from ball import Ball
from groups import AllSprites
import json

class Game:
    def __init__(self):
        # Setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.running = True

        # Sprites
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.player = Player((self.paddle_sprites, self.all_sprites), POS['player'])
        self.ball = Ball((self.all_sprites, self.ball_sprites), self.paddle_sprites, self.update_score)
        self.opponent = Opponent((self.paddle_sprites, self.all_sprites), POS['opponent'], self.ball)

        # Score
        try:
            with open(join('..', 'data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player':0, 'opponent':0}
        self.font = pygame.font.Font(None, 160)

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def display_score(self):
        # Player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.screen.blit(player_surf, player_rect)

        # Opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.screen.blit(opponent_surf, opponent_rect)

        # Line separator
        pygame.draw.line(self.screen, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 10)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(join('..', 'data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)

            # Update
            self.all_sprites.update(dt)

            # Draw
            self.screen.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.draw()
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()