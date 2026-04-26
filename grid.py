import pygame
import units
import math

side = 90
height = math.sqrt(3) * side
circle_ray = 20 

def draw_rectangle_grid(surface):
    for x in range(0, units.WINDOW_X, units.WINDOW_X//7):
        pygame.draw.line(surface, "lightgray", (x, 0), (x, units.WINDOW_Y))
    for y in range(0, units.WINDOW_Y, units.WINDOW_Y//12):
        pygame.draw.line(surface, "lightgray", (0, y), (units.WINDOW_X, y))

def draw_triangle_grid_dual(surface):
    t_height = (side + math.sqrt(side**2 + (height)**2)) / 2
    t_side = t_height * 2 / math.sqrt(3)
    color = "lightgray"
    
    # Draw vertical lines
    for i in range(int(units.WINDOW_X / side)): # +1 to ensure coverage
        x = i * t_height
        pygame.draw.line(surface, color, (x, 0), (x, units.WINDOW_Y))

    num_diagonals = int((units.WINDOW_X + units.WINDOW_Y) / t_height)

    for n in range(-num_diagonals, num_diagonals):
        # Draw diagonal lines top-left to bottom-right (\)
        start_y = n * t_side
        end_x = units.WINDOW_X
        end_y = start_y + (units.WINDOW_X / t_height) * (t_side / 2)
        pygame.draw.line(surface, color, (0, start_y), (end_x, end_y))
        
        # Draw diagonal lines top-right to bottom-left (/)
        start_y2 = n * t_side
        end_y2 = start_y2 - (units.WINDOW_X / t_height) * (t_side / 2)
        pygame.draw.line(surface, color, (0, start_y2), (end_x, end_y2))

def draw_hexagon(surface, color, center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    
    pygame.draw.polygon(surface, color, points, 1)

    for point in points:
        pygame.draw.line(surface, color, center, point, 1)

    pygame.draw.circle(surface, "lightgray", center, circle_ray)
    for point in points:
        pygame.draw.circle(surface, "lightgray", point, circle_ray)

def draw_hex_grid(surface):
    width = side * 2
    color = "lightgray"

    for row in range(units.WINDOW_Y // int(height) + 1):
        for col in range(units.WINDOW_X // int(width * 0.75) + 1):
            x = col * side * 1.5
            y = row * height
            if col % 2 == 1:
                y += height / 2
                
            draw_hexagon(surface, color, (x, y), side)

def draw_grid(surface):
    # draw_triangle_grid_dual(surface)
    draw_hex_grid(surface)