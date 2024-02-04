import pygame

DELAY_SECONDS = 10
SKIERS_PER_BOARDING = 4

NOW_BOARDING_BOTTOM = 1
NOW_BOARDING_INTERMEDIATE = 2
NOW_BOARDING_NONE = 0

# Colors
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
BAR_COLOR = (200, 200, 200)
BOTTOM_COLOR = (64, 128, 255)
INTERMEDIATE_COLOR = (255, 64, 64)

# Sizes
window_size = (500, 500)
circle_radius = 20
border_thickness = 2
circle_speed = 4


def draw_square(square_x, square_y, border_color):
    pygame.draw.rect(window, border_color, (square_x, square_y, station_size, station_size), 2)
    pygame.draw.rect(window, BACKGROUND_COLOR, (square_x + border_thickness, square_y + border_thickness,
                                                station_size - 2 * border_thickness,
                                                station_size - 2 * border_thickness))


def draw_circle(boarding):
    color_mapping = {
        NOW_BOARDING_BOTTOM: BOTTOM_COLOR,
        NOW_BOARDING_INTERMEDIATE: INTERMEDIATE_COLOR,
        NOW_BOARDING_NONE: BACKGROUND_COLOR
    }
    color = color_mapping.get(boarding)
    pygame.draw.circle(window, BORDER_COLOR, (circle_x, circle_y), circle_radius)
    pygame.draw.circle(window, color, (circle_x, circle_y), circle_radius - border_thickness)

    # Show the number of boarded skiers inside the circle
    number = 0 if boarding == NOW_BOARDING_NONE else SKIERS_PER_BOARDING
    text = font.render(str(number), True, BORDER_COLOR)
    text_rect = text.get_rect(center=(circle_x, circle_y))
    window.blit(text, text_rect)


def draw_line(start, end):
    pygame.draw.line(window, BORDER_COLOR, start, end, 2)


def draw_bar(bar_x, bar_y, queue, adding, color):
    bar_width = queue * 5
    pygame.draw.rect(window, color, (bar_x, bar_y, bar_width, station_size))

    # Render the queue at the center of the nar
    text = font.render(str(queue), True, BORDER_COLOR)
    text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y + station_size // 2))
    window.blit(text, text_rect)

    # Render adding skiers besides the bar
    text = font.render("+" + str(adding), True, BORDER_COLOR)
    text_rect = text.get_rect(center=(bar_x + bar_width + 20, bar_y + station_size // 2))
    window.blit(text, text_rect)


def get_positive_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number < 0:
                print("Please insert a positive number.")
            else:
                return number
        except ValueError:
            print("Please insert a valid number.")


def get_current_queue_and_rate(station_name):
    # Get current queue and boarding rate for a given station
    current_queue = get_positive_number(f"How many skiers are currently in the {station_name} station queue? ")
    board_per_minute = get_positive_number(f"How many skiers board per minute at {station_name} station? ")
    return current_queue, board_per_minute


def add_new_skiers(current_queue, board_per_minute):
    # Add new skiers to the queue based on the boarding rate
    return int(current_queue + (board_per_minute * DELAY_SECONDS / 60))


def board_skiers(current_queue, num_to_board):
    # Board skiers from the queue
    boarded = min(num_to_board, current_queue)
    remaining_queue = max(0, current_queue - boarded)
    return remaining_queue, boarded


if __name__ == '__main__':
    # Get initial values for bottom and intermediate stations
    bottom_current_queue, bottom_board_per_minute = get_current_queue_and_rate("bottom")
    intermediate_current_queue, intermediate_board_per_minute = get_current_queue_and_rate("intermediate")

    # Get the boarding periodicity
    periodicity = int(get_positive_number("Every how many chairs should I leave one empty? "))

    counter = 0
    partial_counter = 0
    intermediate_boarded = 0
    bottom_boarded = 0

    intermediate_adding = int(intermediate_board_per_minute * DELAY_SECONDS / 60)
    bottom_adding = int(bottom_board_per_minute * DELAY_SECONDS / 60)

    # Set up the window
    window_width, window_height = window_size
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Moving Circle Animation")

    # Set up the line
    line_start = (0, window_height)
    line_end = (window_width, 0)

    # Set up the stations
    station_size = 2 * circle_radius

    station_bottom_x = 0
    station_bottom_y = window_height - station_size

    station_intermediate_x = (window_width - station_size) // 2
    station_intermediate_y = (window_height - station_size) // 2

    # Set up the circle
    circle_x = circle_radius
    circle_y = window_height - circle_radius

    # Initialize Pygame
    pygame.init()

    # Set up the clock
    clock = pygame.time.Clock()

    # Set up the font
    font = pygame.font.Font(None, 24)

    while True:

        # Increment counters
        counter += 1
        partial_counter += 1

        # Update the queues with new skiers
        bottom_current_queue = add_new_skiers(bottom_current_queue, bottom_board_per_minute)
        intermediate_current_queue = add_new_skiers(intermediate_current_queue, intermediate_board_per_minute)

        # Board skiers based on the periodicity
        if partial_counter < periodicity:

            # Board at bottom station
            bottom_current_queue, bottom_boarded = board_skiers(bottom_current_queue, SKIERS_PER_BOARDING)
            now_boarding = NOW_BOARDING_BOTTOM
            intermediate_boarded = 0
        else:
            # Board at intermediate station
            intermediate_current_queue, intermediate_boarded = board_skiers(intermediate_current_queue,
                                                                            SKIERS_PER_BOARDING)
            now_boarding = NOW_BOARDING_INTERMEDIATE
            bottom_boarded = 0
            partial_counter = 0

        # Animation loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            # Clear the screen
            window.fill(BACKGROUND_COLOR)

            # Draw the line
            draw_line(line_start, line_end)

            # Draw the bottom station
            draw_square(station_bottom_x, station_bottom_y, BOTTOM_COLOR)
            draw_bar(station_bottom_x + station_size + 10, station_bottom_y, bottom_current_queue, bottom_adding,
                     BOTTOM_COLOR)

            # Draw the intermediate station
            draw_square(station_intermediate_x, station_intermediate_y, INTERMEDIATE_COLOR)

            # If boarding at intermediate station
            if now_boarding == NOW_BOARDING_INTERMEDIATE and circle_x < window_width // 2:

                # Display empty chair and do not reduce the queue
                draw_circle(NOW_BOARDING_NONE)
                draw_bar(station_intermediate_x + station_size + 10, station_intermediate_y,
                         intermediate_current_queue + SKIERS_PER_BOARDING,
                         intermediate_adding, INTERMEDIATE_COLOR)

            else:
                # Draw the chair based on the boarding station
                draw_circle(now_boarding)
                draw_bar(station_intermediate_x + station_size + 10, station_intermediate_y, intermediate_current_queue,
                         intermediate_adding, INTERMEDIATE_COLOR)

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(30)

            # Move the circle
            circle_x += circle_speed
            circle_y -= circle_speed

            # Check if the circle is out of bounds
            if circle_x > window_width + circle_radius:
                running = False

        # End of run
        running = False
        circle_x = circle_radius
        circle_y = window_height - circle_radius
