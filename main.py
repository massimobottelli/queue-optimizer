from prettytable import PrettyTable
import time

DELAY_SECONDS = 10
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
    # Get current queue and boarding rate for a given station
    current_queue = get_positive_number(f"How many skiers are currently in the {station_name} station queue? ")
    board_per_minute = get_positive_number(f"How many skiers board per minute at {station_name} station? ")
    return current_queue, board_per_minute


def add_new_skiers(current_queue, board_per_minute):
    # Add new skiers to the queue based on the boarding rate
    return int(current_queue + (board_per_minute * DELAY_SECONDS / 60))


def board_skiers(current_queue, num_to_board):
    # Board a specified number of skiers from the queue
    boarded = min(num_to_board, current_queue)
    remaining_queue = max(0, current_queue - boarded)
    return remaining_queue, boarded


def text_bar_chart(data, labels, boarding):
    max_value = max(data)
    scale_factor = 40 / max_value  # Factor for the desired width

    for boarded, label, value in zip(boarding, labels, data):
        bar = '#' * int(value * scale_factor)
        print(f"{label}: {value} {bar} {boarded}")


if __name__ == '__main__':
    # Get initial values for bottom and intermediate stations
    bottom_current_queue, bottom_board_per_minute = get_current_queue_and_rate("bottom")
    intermediate_current_queue, intermediate_board_per_minute = get_current_queue_and_rate("intermediate")

    # Get the boarding periodicity from the user
    periodicity = int(get_positive_number("Every how many chairs should I leave one empty? "))

    counter = 0
    partial_counter = 0

    labels = ['Interm', 'Bottom']

    # Create the table
    table = PrettyTable()
    table.field_names = ["Station", "Queue", "Boarded"]

    while True:
        # Increment counters
        counter += 1
        partial_counter += 1

        # Update the queues with new skiers
        bottom_current_queue = add_new_skiers(bottom_current_queue, bottom_board_per_minute)
        intermediate_current_queue = add_new_skiers(intermediate_current_queue, intermediate_board_per_minute)

        # Board skiers based on the periodicity
        if partial_counter < periodicity:
            bottom_current_queue, bottom_boarded = board_skiers(bottom_current_queue, SKIERS_PER_BOARDING)
            intermediate_boarded = 0
        else:
            bottom_boarded = 0
            intermediate_current_queue, intermediate_boarded = board_skiers(intermediate_current_queue,
                                                                            SKIERS_PER_BOARDING)
            partial_counter = 0

        # Prepare data for graph
        data = [bottom_current_queue, intermediate_current_queue]
        boarding = [-bottom_boarded, -intermediate_boarded]

        # Create and display the text-based bar chart
        print()
        text_bar_chart(data, labels, boarding)

        time.sleep(2)
