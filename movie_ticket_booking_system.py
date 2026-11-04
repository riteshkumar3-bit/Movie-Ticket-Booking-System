"""
Movie Ticket Booking System
Project No.: 49
Language: Python 3

Seats: A1 to C5 (15 seats)
Ticket price: Rs. 200 per seat
Bookings are saved in bookings.txt in the same folder as this program.
"""

from pathlib import Path

TICKET_PRICE = 200
ROWS = ["A", "B", "C"]
SEAT_NUMBERS = ["1", "2", "3", "4", "5"]
BOOKING_FILE = Path(__file__).with_name("bookings.txt")


def create_empty_seat_map():
    """Create a seat map in which every seat is available."""
    return {
        row: {number: None for number in SEAT_NUMBERS}
        for row in ROWS
    }


def is_valid_seat(seat_code):
    """Return True only for seat codes A1 through C5."""
    if not isinstance(seat_code, str):
        return False

    seat_code = seat_code.strip().upper()
    return (
        len(seat_code) == 2
        and seat_code[0] in ROWS
        and seat_code[1] in SEAT_NUMBERS
    )


def load_bookings():
    """Load saved bookings from the text file."""
    seats = create_empty_seat_map()

    if not BOOKING_FILE.exists():
        return seats

    try:
        with BOOKING_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                if not line or "|" not in line:
                    continue

                seat_code, name = line.split("|", 1)
                seat_code = seat_code.strip().upper()
                name = name.strip()

                if is_valid_seat(seat_code) and name:
                    row = seat_code[0]
                    number = seat_code[1]
                    seats[row][number] = name

    except OSError:
        print("Warning: Could not read bookings.txt. Starting with empty seats.")

    return seats


def save_bookings(seats):
    """Save all current bookings to the text file."""
    try:
        with BOOKING_FILE.open("w", encoding="utf-8") as file:
            for row in ROWS:
                for number in SEAT_NUMBERS:
                    name = seats[row][number]
                    if name is not None:
                        file.write(f"{row}{number}|{name}\n")
    except OSError:
        print("Error: Bookings could not be saved.")


def count_available_seats(seats):
    """Count seats that are not booked."""
    count = 0
    for row in ROWS:
        for number in SEAT_NUMBERS:
            if seats[row][number] is None:
                count += 1
    return count


def display_seat_map(seats):
    """Display the cinema seat map."""
    print("\n========== SEAT MAP ==========")
    print("     " + "  ".join(SEAT_NUMBERS))

    for row in ROWS:
        seat_status = []
        for number in SEAT_NUMBERS:
            seat_status.append("O" if seats[row][number] is None else "X")
        print(f"Row {row}:  " + "  ".join(seat_status))

    print("\nO = Available   X = Booked")
    print(f"Seats left: {count_available_seats(seats)}")
    print("==============================\n")


def parse_seat_codes(raw_input):
    """Accept one or more seat codes, separated by commas or the word 'and'."""
    cleaned = raw_input.upper().replace(",", " ")
    parts = cleaned.replace(" AND ", " ").split()
    return parts


def book_seat(seats):
    """Book one or more available seats for the same passenger."""
    raw_seats = input("Enter seat code(s), e.g. A1 or A2 and A3: ").strip()
    seat_codes = parse_seat_codes(raw_seats)

    if not seat_codes:
        print("Please enter at least one seat code.")
        return

    # Validate every seat code before changing any booking.
    for seat_code in seat_codes:
        if not is_valid_seat(seat_code):
            print("Invalid seat. Rows are A to C and seat numbers are 1 to 5.")
            return

    # Avoid booking the same seat twice in one request.
    if len(set(seat_codes)) != len(seat_codes):
        print("A seat code was entered more than once. Please try again.")
        return

    for seat_code in seat_codes:
        row, number = seat_code[0], seat_code[1]
        if seats[row][number] is not None:
            print(f"Seat {seat_code} is already booked.")
            return

    name = input("Enter passenger name: ").strip()
    if not name:
        print("Name cannot be empty. Booking cancelled.")
        return

    for seat_code in seat_codes:
        row, number = seat_code[0], seat_code[1]
        seats[row][number] = name

    save_bookings(seats)
    amount = len(seat_codes) * TICKET_PRICE

    if len(seat_codes) == 1:
        print(f"Seat {seat_codes[0]} booked for {name}. Amount: {amount}")
    else:
        print(f"Seats {', '.join(seat_codes)} booked for {name}. Amount: {amount}")

    if count_available_seats(seats) == 0:
        print("Seats left: 0")
        print("Show is now housefull.")


def cancel_booking(seats):
    """Cancel an existing booking using its seat code."""
    seat_code = input("Enter seat code to cancel (A1 to C5): ").strip().upper()

    if not is_valid_seat(seat_code):
        print("Invalid seat. Rows are A to C and seat numbers are 1 to 5.")
        return

    row, number = seat_code[0], seat_code[1]

    if seats[row][number] is None:
        print(f"Seat {seat_code} is not booked.")
        return

    passenger_name = seats[row][number]
    seats[row][number] = None
    save_bookings(seats)
    print(f"Booking for {seat_code} ({passenger_name}) has been cancelled.")


def show_menu():
    """Display the main menu."""
    print("\n====== MOVIE TICKET BOOKING SYSTEM ======")
    print("1. Book Ticket")
    print("2. Cancel Ticket")
    print("3. Seat Map")
    print("4. Exit")
    print("=========================================")


def main():
    """Run the booking system."""
    seats = load_bookings()
    print("Welcome to the Movie Ticket Booking System!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            book_seat(seats)
        elif choice == "2":
            cancel_booking(seats)
        elif choice == "3":
            display_seat_map(seats)
        elif choice == "4":
            print("Thank you for using the Movie Ticket Booking System.")
            break
        else:
            print("Invalid menu option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
