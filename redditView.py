import pygame
import praw
from button import *

WHITE = (255, 255, 255)

redditInstance = praw.Reddit(
    client_id="z5StR94kMHZ8vl-QnB-C7A",
    client_secret="kgveybBNQquwRnNCNCa0lIl-jsfH9g",
    user_agent="testRedditBot"
)

class redditView:
    def __init__(self, screen, position=(20, 0), width=300, height=200):
        self.screen = screen
        self.width = width
        self.height = height
        self.padding = 12
        self.font = pygame.font.Font(None, 20)
        self.posts = getPostsFromTempleSubreddit()
        self.current_index = 0

        win_height = screen.get_height()
        self.rect = pygame.Rect(position[0],
                                win_height - height - 80,
                                width,
                                height)
        btn_w, btn_h = 120, 36
        btn_x = self.rect.x + (width - btn_w) // 2
        btn_y = self.rect.bottom + 10
        self.button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    def set_posts(self, posts):
        self.posts = posts
        self.current_index = 0

    def next_post(self):
        if self.posts:
            self.current_index = (self.current_index + 1) % len(self.posts)

    def wrap_text(self, text):
        words = text.split(' ')
        lines, current = [], ""
        for w in words:
            test = current + (" " if current else "") + w
            if self.font.size(test)[0] <= self.width - 2 * self.padding:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    def draw(self):
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        pygame.draw.rect(s, (255, 255, 255, 40), s.get_rect(), 2, border_radius=8)
        self.screen.blit(s, (self.rect.x, self.rect.y))

        # choose current post text
        if not self.posts:
            text = "Having trouble loading posts from r/Temple"
        else:
            post = self.posts[self.current_index]
            text = f"{post['title']}\nupvotes: {post['upvotes']}"

        # render wrapped lines
        lines = []
        for line in text.split("\n"):
            lines.extend(self.wrap_text(line))
        max_lines = (self.height - 2 * self.padding) // self.font.get_linesize()
        lines = lines[:max_lines]

        y = self.rect.y + self.padding
        for line in lines:
            rendered = self.font.render(line, True, WHITE)
            self.screen.blit(rendered, (self.rect.x + self.padding, y))
            y += self.font.get_linesize()

        # draw reddit button
        self.nextPostButton = Button((20, 700), (300, 75), WHITE, "NEXT POST")

        self.nextPostButton.draw(self.screen,BLACK)



    def is_button_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # if self.button_rect.collidepoint(event.pos):
            if self.nextPostButton.is_clicked:
                return True
        return False
    
def getPostsFromTempleSubreddit(limit=25):
    subreddit = redditInstance.subreddit("temple")
    posts = []

    for submission in subreddit.top(limit=limit):
        posts.append({
            "title": submission.title,
            "upvotes": submission.score
        })

    return posts
