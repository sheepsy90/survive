# -*- coding:utf-8 -*-
import pygame
from pygame.rect import Rect
from client.colours import WHITE, GREY, GREEN
from client.config import WINDOWWIDTH

ITEM_CELL_SIZE = 25

def draw_item_grid(renderer, border, basex, basey, shape):
    for i in range(shape[0]):
        for j in range(shape[1]):
            other_rect = Rect(i * ITEM_CELL_SIZE + basex+border, j * ITEM_CELL_SIZE + basey+border, 25, 25)
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(renderer, WHITE, other_rect)
                else:
                    pygame.draw.rect(renderer, GREY, other_rect)
            else:
                if j % 2 == 0:
                    pygame.draw.rect(renderer, GREY, other_rect)
                else:
                    pygame.draw.rect(renderer, WHITE, other_rect)
    other_rect = Rect(basex+1, basey+1, shape[0] * ITEM_CELL_SIZE + border,
                      shape[1] * ITEM_CELL_SIZE + border)
    pygame.draw.rect(renderer, (115, 179, 32), other_rect, border)

def textHollow(font, message, fontcolor):
    notcolor = [c ^ 0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img

def draw_text_on_screen_at(screen, text, xc, yc, font_size, c1=GREEN, c2=WHITE, alpha=255):
    name_tag_font = pygame.font.Font('resources/fonts/VENUSRIS.ttf', font_size)
    g = textOutline(name_tag_font, text, c1, c2)
    name_tag_rect = g.get_rect()
    name_tag_rect.center = (xc, yc)
    if name_tag_rect.width > WINDOWWIDTH:
        g = pygame.transform.scale(g, (WINDOWWIDTH, int(name_tag_rect.height * WINDOWWIDTH/float(name_tag_rect.width))))
    name_tag_rect = g.get_rect()
    name_tag_rect.center = (xc, yc)
    g.set_alpha(alpha)
    screen.blit(g, name_tag_rect)


def drawText(surface, text, color, rect, font, aa=True, bkg=None):

    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text



def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    amt = max(1, amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf



def dim(surface, darken_factor=64, color_filter=(0,0,0)):
        darken = pygame.Surface(surface.get_size())
        darken.fill(color_filter)
        darken.set_alpha(darken_factor)
        # safe old clipping rectangle...
        old_clip = pygame.display.get_surface().get_clip()

        # ..blit over entire screen...
        surface.blit(darken, (0, 0))
        #pygame.display.flip()
        # ... and restore clipping
        #pygame.display.get_surface().set_clip(old_clip)
