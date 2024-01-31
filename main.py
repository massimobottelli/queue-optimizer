import time

DELAY_SECONDS = 3
SKIERS_PER_BOARDING = 4

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
    current_queue = get_positive_number(f"How many skiers are currently in the {station_name} station queue? ")
    board_per_minute = get_positive_number(f"How many skiers board per minute at {station_name} station? ")
    return current_queue, board_per_minute

def board_skiers(current_queue, board_per_minute, num_to_board):
    boarded = min(num_to_board, current_queue)
    remaining_queue = max(0, current_queue - boarded)
    return remaining_queue, boarded

def add_new_skiers(current_queue, board_per_minute):
    updated_current_queue = int(current_queue + (board_per_minute * DELAY_SECONDS / 60))
    return updated_current_queue

if __name__ == '__main__':
    bottom_current_queue, bottom_board_per_minute = get_current_queue_and_rate("bottom")
    intermediate_current_queue, intermediate_board_per_minute = get_current_queue_and_rate("intermediate")

    for _ in range(10):

        # Add new skiers to the queues
        bottom_current_queue = add_new_skiers(bottom_current_queue, bottom_board_per_minute)
        intermediate_current_queue = add_new_skiers(intermediate_current_queue, intermediate_board_per_minute)

        # Board SKIERS_PER_BOARDING skiers at the bottom station
        bottom_current_queue, boarded_bottom = board_skiers(bottom_current_queue, bottom_board_per_minute, SKIERS_PER_BOARDING)


        # Display current queue states and the number of skiers that boarded
        print("\nBottom Station:")
        print(" - Queue:", bottom_current_queue)
        print(" - Boarded:", boarded_bottom)
        print("Intermediate Station")
        print(" - Queue:", intermediate_current_queue)
        print(" - Boarded:")

        time.sleep(DELAY_SECONDS)

    print("\nSimulation complete.")
