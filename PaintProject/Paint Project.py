#Paint Project
#Theme- Harry Potter
#Lamina Zaman

"""
This program is similar to Microsoft Paint as it allows the user to create a digital 'painting'.

In order to create this 'painting', the user can choose from a variety of tools including
basic drawing tools (pencil, eraser, brushes), basic shapes (line, rectangles, ovals),
a 'sizing bar' (to change the thickness of certain tools),
a 'colour palette' and an 'extract' tool (both can be used to change the colour of certain tools),
and stamps (displays an image when the user clicks on the canvas).

This program also allows the user to load images from their files, save images to their files,
undo or redo an action, and clear the canvas.
"""

from pygame import *
from math import *
from random import *

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

root = Tk()
root.withdraw()

tool = "pencil"
col = 0
size = 10
a, b = 0, 0

screen = display.set_mode((1200, 680))

#Background
background = image.load("Pottermore.png")   #Load Image
screen.blit(transform.scale(background, (1200, 680)), (0, 0))   #Display Image

#Title
title = image.load("Harry Painter.png")
screen.blit(transform.scale(title, (320, 80)), (800, 20))

#Canvas
canvas = Rect(40, 40, 680, 560)
draw.rect(screen, (250, 250, 200), canvas)

#Menu
pencil_icon = Rect(0, 640, 40, 40)   #Invisible Rectangles
eraser_icon = Rect(40, 640, 40, 40)

brush_icon = Rect(80, 640, 40, 40)
alpha_icon = Rect(120, 640, 40, 40)
spray_icon = Rect(160, 640, 40, 40)

line_icon = Rect(200, 640, 40, 40)

rect_unfilled = Rect(360, 640, 40, 40)
rect_filled = Rect(400, 640, 40, 40)
oval_unfilled = Rect(440, 640, 40, 40)
oval_filled = Rect(480, 640, 40, 40)

extract_icon = Rect(520, 640, 40, 40)
text_icon = Rect(560, 640, 40, 40)

load_icon = Rect(600, 640, 80, 40)
save_icon = Rect(680, 640, 80, 40)
undo_icon = Rect(760, 640, 80, 40)
redo_icon = Rect(840, 640, 80, 40)
clear_icon = Rect(920, 640, 80, 40)

tool_pics = [image.load("Tools/Pencil.png"),
             image.load("Tools/Eraser.png"),
             image.load("Tools/Brush.png"),
             image.load("Tools/Spray.png"),
             image.load("Tools/Extract.png"),
             image.load("Tools/Text.png"),
             image.load("Tools/Load.png"),
             image.load("Tools/Save.png"),
             image.load("Tools/Undo.png"),
             image.load("Tools/Redo.png"),
             image.load("Tools/Clear.png")]   #Loading pictures of tools.

#Stamps
stamp0 = transform.scale(image.load("Stamps/Chocolate Frog.png"), (80, 80))
stamp1 = transform.scale(image.load("Stamps/Deathly Hallows.png"), (80, 80))
stamp2 = transform.scale(image.load("Stamps/Time Turner.png"), (80, 80))
stamp3 = transform.scale(image.load("Stamps/Lightning Bolt.png"), (80, 80))

stamp4 = transform.scale(image.load("Stamps/Snitch.png"), (80, 80))
stamp5 = transform.scale(image.load("Stamps/Sorting Hat.png"), (80, 80))
stamp6 = transform.scale(image.load("Stamps/Hogwarts Crest.png"), (100, 120))

stamps = [stamp0, stamp1, stamp2, stamp3, stamp4, stamp5, stamp6]   #Scaled Down

stamp_rects = [Rect(800, 160, 80, 80),
               Rect(920, 160, 80, 80),
               Rect(1040, 160, 80, 80),
               Rect(800, 280, 80, 80),
               Rect(920, 280, 80, 80),
               Rect(1040, 280, 80, 80),
               Rect(910, 400, 100, 120),]   #Invisible rectangles over stamps.

screen.blit(stamp0, (800, 160))   #Display stamps on the side.
screen.blit(stamp1, (920, 160))
screen.blit(stamp2, (1040, 160))
screen.blit(stamp3, (800, 280))
screen.blit(stamp4, (920, 280))
screen.blit(stamp5, (1040, 280))
screen.blit(stamp6, (910, 400))

#Colours
colours = screen.blit(transform.scale(image.load("RGB.jpeg"), (160, 40)), (1000, 640))   #Colour Palette

#Size
sizes = Rect(250, 655, 100, 10)   #Invisible Rectangle

#Coordinates
font.init()
times = font.SysFont("Times New Roman", 20)   #Imports font for coordinates.

#Text
spells = [image.load("Spells/Accio.png"),
          image.load("Spells/Confundo.png"),
          image.load("Spells/Expecto Patronum.png"),
          image.load("Spells/Expelliarmus.png"),
          image.load("Spells/Lumos.png"),
          image.load("Spells/Riddikulus.png"),
          image.load("Spells/Wingardium Leviosa.png")]   #For text tool.

#Undo and Redo
undos = [screen.subsurface(canvas).copy()]
redos = []

running = True

while running:
    click = False
    action = False
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN:
            click = True   #When you click down on mouse.
            if evt.button == 1:
                a, b = evt.pos   #Coordinates of first click. Useful for drawing lines/ shapes.
        if evt.type == MOUSEBUTTONUP:
            action = True   #When you release the mouse.

    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()

    #Colours
    if mb[0] == 1 and colours.collidepoint(mx, my):   #Gets the colour that the user selects from the colour palette.
        col = screen.get_at((mx, my))                 #Applies to all drawing tools (except the pencil and eraser) and shapes.
    draw.rect(screen, col, (1160, 640, 40, 40))   #Colour Preview Box

    #Size
    if mb[0] == 1 and sizes.collidepoint(mx, my):   #Allows the user to click on a 'size bar' to choose the thickness for certain tools.
        size = (mx - 250)//5                        #Applies to the eraser, brushes, and line.
    draw.rect(screen, (250, 250, 200), (240, 640, 120, 40))   #Drawing the 'size bar'.
    draw.rect(screen, (0, 0, 0), (250, 660, 100, 1), 2)
    draw.line(screen, (0, 0, 0), (250, 655), (250, 665), 2)
    draw.line(screen, (0, 0, 0), (350, 650), (350, 670), 2)
    draw.line(screen, (0, 0, 0), (size*5 + 250, 656), (size*5 + 250, 664), 10)   #Location of line indicates the size.

    #Coordinates
    coor = times.render(str((mx, my)), True, (250, 250, 200))
    draw.rect(screen, (0, 0, 0), (0, 0, 120, 40))   #Draws black rectangle to prevent coordinates from overlapping.
    screen.blit(coor, (10, (40 - times.get_height())//2))

    #Menu
    draw.rect(screen, (250, 250, 200), pencil_icon)   #Drawing rectangles and blitting pictures to create menu.
    screen.blit(transform.scale(tool_pics[0], (30, 30)), (5, 645))
    
    draw.rect(screen, (250, 250, 200), eraser_icon)
    screen.blit(transform.scale(tool_pics[1], (30, 30)), (45, 645))
    
    draw.rect(screen, (250, 250, 200), brush_icon)
    screen.blit(transform.scale(tool_pics[2], (30, 30)), (85, 645))
    
    draw.rect(screen, (250, 250, 200), alpha_icon)
    cover_pic = Surface((20, 20)).convert()
    cover_pic.set_alpha(50)
    cover_pic.fill((255, 255, 255))
    cover_pic.set_colorkey((255, 255, 255))
    draw.circle(cover_pic, (0, 0, 0), (10, 10), 10)
    screen.blit(cover_pic, (130, 650))
    
    draw.rect(screen, (250, 250, 200), spray_icon)
    screen.blit(transform.scale(tool_pics[3], (30, 30)), (165, 645))
    
    draw.rect(screen, (250, 250, 200), line_icon)
    draw.line(screen, (0, 0, 0), (210, 670), (230, 650), 2)

    draw.rect(screen, (250, 250, 200), rect_unfilled)
    draw.rect(screen, (0, 0, 0), (368, 648, 24, 24), 1)
              
    draw.rect(screen, (250, 250, 200), rect_filled)
    draw.rect(screen, (0, 0, 0), (408, 648, 24, 24))
    
    draw.rect(screen, (250, 250, 200), oval_unfilled)
    draw.circle(screen, (0, 0, 0), (460, 660), 10, 1)
    
    draw.rect(screen, (250, 250, 200), oval_filled)
    draw.circle(screen, (0, 0, 0), (500, 660), 10)

    draw.rect(screen, (250, 250, 200), extract_icon)
    screen.blit(transform.scale(tool_pics[4], (30, 30)), (525, 645))
    
    draw.rect(screen, (250, 250, 200), text_icon)
    screen.blit(transform.scale(tool_pics[5], (30, 30)), (565, 645))

    draw.rect(screen, (250, 250, 200), load_icon)
    screen.blit(tool_pics[6], (640 - tool_pics[6].get_width()/2, 660 - tool_pics[6].get_height()/2))
    
    draw.rect(screen, (250, 250, 200), save_icon)
    screen.blit(tool_pics[7], (720 - tool_pics[6].get_width()/2, 660 - tool_pics[6].get_height()/2))
    
    draw.rect(screen, (250, 250, 200), undo_icon)
    screen.blit(tool_pics[8], (800 - tool_pics[6].get_width()/2, 660 - tool_pics[6].get_height()/2))
    
    draw.rect(screen, (250, 250, 200), redo_icon)
    screen.blit(tool_pics[9], (880 - tool_pics[6].get_width()/2, 660 - tool_pics[6].get_height()/2))
    
    draw.rect(screen, (250, 250, 200), clear_icon)
    screen.blit(tool_pics[10], (960 - tool_pics[6].get_width()/2, 660 - tool_pics[6].get_height()/2))

    #Select Tool
    if mb[0] == 1 and pencil_icon.collidepoint(mx, my):
        tool = "pencil"
    if mb[0] == 1 and eraser_icon.collidepoint(mx, my):
        tool = "eraser"

    if mb[0] == 1 and brush_icon.collidepoint(mx, my):
        tool = "brush"
    if mb[0] == 1 and alpha_icon.collidepoint(mx, my):
        tool = "alpha"
    if mb[0] == 1 and spray_icon.collidepoint(mx, my):
        tool = "spray"
        
    if mb[0] == 1 and line_icon.collidepoint(mx, my):
        tool = "line"

    if mb[0] == 1 and rect_unfilled.collidepoint(mx, my):
        tool = "rect_unf"
    if mb[0] == 1 and rect_filled.collidepoint(mx, my):
        tool = "rect_f"
    if mb[0] == 1 and oval_unfilled.collidepoint(mx, my):
        tool = "oval_unf"
    if mb[0] == 1 and oval_filled.collidepoint(mx, my):
        tool = "oval_f"

    if mb[0] == 1 and extract_icon.collidepoint(mx, my):
        tool = "extract"
    if mb[0] == 1 and text_icon.collidepoint(mx, my):
        tool = "text"

    if mb[0] == 1:   #Select Stamp Tool
        for i in range(len(stamps)):
            if stamp_rects[i].collidepoint(mx, my):
                tool = "stamp"
                stamp = stamps[i]   #Selects one stamp from 'stamps' list.

    #Highlight Tool
    if tool == "pencil":
        draw.rect(screen, (0, 0, 0), pencil_icon, 1)
    if tool == "eraser":
        draw.rect(screen, (0, 0, 0), eraser_icon, 1)

    if tool == "brush":
        draw.rect(screen, (0, 0, 0), brush_icon, 1)
    if tool == "alpha":
        draw.rect(screen, (0, 0, 0), alpha_icon, 1)
    if tool == "spray":
        draw.rect(screen, (0, 0, 0), spray_icon, 1)
        
    if tool == "line":
        draw.rect(screen, (0, 0, 0), line_icon, 1)

    if tool == "rect_unf":
        draw.rect(screen, (0, 0, 0), rect_unfilled, 1)
    if tool == "rect_f":
        draw.rect(screen, (0, 0, 0), rect_filled, 1)
    if tool == "oval_unf":
        draw.rect(screen, (0, 0, 0), oval_unfilled, 1)
    if tool == "oval_f":
        draw.rect(screen, (0, 0, 0), oval_filled, 1)

    if tool == "extract":
        draw.rect(screen, (0, 0, 0), extract_icon, 1)
    if tool == "text":
        draw.rect(screen, (0, 0, 0), text_icon, 1)

    #Tools
    if mb[0] == 1 and canvas.collidepoint(mx, my):
        screen.set_clip(canvas)   #Stays within canvas.
        
        if tool == "pencil":   #Basic pencil tool.
            draw.line(screen, (0, 0, 0), (omx, omy), (mx, my), 1)

        if tool == "eraser":   #Basic eraser tool.
            dist = int(hypot(omx - mx, omy - my))   #Uses similar triangles to keep circles from spreading apart.
            dist = max(1, dist)
            for s in range(dist):
                sx = int(s*(omx - mx)/dist)
                sy = int(s*(omy - my)/dist)
                draw.circle(screen, (250, 250, 200), (mx + sx, my + sy), size)

        if tool == "brush":   #Basic paint brush tool.
            dist = int(hypot(omx - mx, omy - my))
            dist = max(1, dist)
            for s in range(dist):
                sx = int(s*(omx - mx)/dist)
                sy = int(s*(omy - my)/dist)
                draw.circle(screen, col, (mx + sx, my + sy), size)
                
        if tool == "alpha":   #A partially transparent brush tool.
            cover = Surface((size*2, size*2)).convert()
            cover.set_alpha(10)   #How transparent you want the brush to be.
            cover.fill((255, 255, 255))
            cover.set_colorkey((255, 255, 255))
            dist = int(hypot(omx - mx, omy - my))
            dist = max(1, dist)
            for s in range(dist):
                sx = int(s*(omx - mx)/dist)
                sy = int(s*(omy - my)/dist)
                draw.circle(cover, col, (size, size), size)
                screen.blit(cover, (mx + sx - size, my + sy - size))
        
        if tool == "spray":   #Creates a spray paint effect by drawing random dots around the mouse.
            for s in range(size):
                sx = randint(-size, size)
                sy = randint(-size, size)
                if hypot(sx, sy) <= size:   #Treating the size as the diameter creates a cirular shape.
                    draw.circle(screen, col, (mx + sx, my + sy), 1)

        if tool == "line":   #Click and drag to create line.
            screen.fill((250, 250, 200))   #Clears Canvas
            screen.blit(undos[-1], (40, 40))   #Blits previous canvas on to canvas.
            draw.line(screen, col, (a, b), (mx, my), size)

        if tool == "rect_unf":   #Click and drag to create an unfilled rectangle.
            screen.fill((250, 250, 200))
            screen.blit(undos[-1], (40, 40))
            draw.rect(screen, col, (a, b, mx - a, my - b), 1)

        if tool == "rect_f":   #Click and drag to create a filled rectangle.
            screen.fill((250, 250, 200))
            screen.blit(undos[-1], (40, 40))
            draw.rect(screen, col, (a, b, mx - a, my - b))

        if tool == "oval_unf":   #Click and drag to create a unfilled oval.
            screen.fill((250, 250, 200))
            screen.blit(undos[-1], (40, 40))
            unf_rect = Rect(a, b, mx - a, my - b)
            unf_rect.normalize()   #Don't need to worry about the direction the oval is dragged.
            if abs(mx - a)/2 < 1:   #If the oval is too thin, draw it filled.
                draw.ellipse(screen, col, unf_rect)
            elif abs(my - b)/2 < 1:
                draw.ellipse(screen, col, unf_rect)
            else:
                draw.ellipse(screen, col, unf_rect, 1)

        if tool == "oval_f":   #Click and drag to create a filled oval.
            screen.fill((250, 250, 200))
            screen.blit(undos[-1], (40, 40))
            f_rect = Rect(a, b, mx - a, my - b)
            f_rect.normalize()
            draw.ellipse(screen, col, f_rect)
        
        if tool == "extract":   #Gets the colour that the mouse selected from the canvas.
            col = screen.get_at((mx, my))
            
        if tool == "text" and click == True:   #Displays a word/ words when the user clicks on the canvas.
            spell = choice(spells)
            screen.blit(spell, (mx - spell.get_width()/2, my - spell.get_height()/2))

        if tool == "stamp":   #Displays an image when the user clicks on the canvas.
            screen.blit(undos[-1], (40, 40))   #Creates a 'pick-up and drop' effect.
            if stamp == stamp6:
                screen.blit(stamp, (mx - 50, my - 60))
            else:
                screen.blit(stamp, (mx - 40, my - 40))

    #More Tools
    if action == True and canvas.collidepoint(mx, my):
        if tool != "extract":
            undos.append(screen.subsurface(canvas).copy())   #Adds a copy of the canvas
                                                             #to the 'undos' list.
    
    if load_icon.collidepoint(mx, my):   #Allows the user to load images.
        if mb[0] == 1:
            draw.rect(screen, (0, 0, 0), load_icon, 1)   #Highlight selected tool.
        if action:
            load_result = askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")])
            if load_result != "":   #If the user doesn't click on 'Cancel', blit the picture onto the canvas.
                screen.blit(transform.scale(image.load(load_result), (680, 560)), (40, 40))
                undos.append(screen.subsurface(canvas).copy())
    
    if save_icon.collidepoint(mx, my):   #Allows the user to save images.
        if mb[0] == 1:
            draw.rect(screen, (0, 0, 0), save_icon, 1)
        if action:
            save_result = asksaveasfilename(filetypes = [("Picture files", "*.png;*.jpg")])
            if save_result != "":
                if ".jpg" not in save_result and ".png" not in save_result:
                    save_result += ".jpg"   #Adds extension if the user didn't already.
                image.save(undos[-1], save_result)   #Saves Canvas

    if undo_icon.collidepoint(mx, my):   #Allows the user to undo an action.
        if mb[0] == 1:
            draw.rect(screen, (0, 0, 0), undo_icon, 1)
        if click:
            if len(undos) > 1:
                redos.append(undos[-1])   #Transfer last item to 'redos' list.
                undos.pop()
                screen.blit(undos[-1], (40, 40))   #Blit the last item.
            else:
                draw.rect(screen, (250, 250, 200), (40, 40, 680, 560))   #Draws blank canvas.

    if redo_icon.collidepoint(mx, my):   #Allows the user to redo an action.
        if mb[0] == 1:
            draw.rect(screen, (0, 0, 0), redo_icon, 1)
        if click:
            if len(redos) > 0:   #If the 'redos' list is not empty.
                screen.blit(redos[-1], (40, 40))   #Blit the last item. 
                undos.append(redos[-1])   #Transfer to 'undos' list.
                redos.pop()

    if clear_icon.collidepoint(mx, my):   #Allows the user to clear the canvas.
        if mb[0] == 1:
            draw.rect(screen, (0, 0, 0), clear_icon, 1)
            draw.rect(screen, (250, 250, 200), (40, 40, 680, 560))   #Draws a canvas-coloured rectangle over the canvas.
        if action:
            undos.append(screen.subsurface(canvas).copy())
    
    screen.set_clip(None)
    omx, omy = mx, my
    print(tool)
    
    display.flip()

font.quit()
del times

quit()
