# Queue optimizer

def get_positive_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number < 0:
                print("Per favore, inserisci un numero positivo.")
                continue
            return number
        except ValueError:
            print("Per favore, inserisci un valore numerico.")


def get_queue():
    queue_uphill = get_positive_number("Inserisci il numero di sciatori al minuto a monte: ")
    queue_downhill = get_positive_number("Inserisci il numero di sciatori al minuto a valle: ")
    return queue_uphill, queue_downhill


# Main loop
if __name__ == '__main__':
    skiers_uphill, skiers_downhill = get_queue()
    print("I valori inseriti sono:", skiers_uphill, "e", skiers_downhill)

