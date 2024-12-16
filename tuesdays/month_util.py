# Month names, and number of days each
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS =   [0,   31,        28,         31,      30,      31,    30,     31,     31,       30,          31,        30,         31       ]

# Do stuff like "1st", "2nd", "3rd", "4th", etc
def get_ord(day):
    if day in {1, 21, 31}:
        return f"{day}st"
    elif day in {2, 22}:
        return f"{day}nd"
    elif day in {3, 23}:
        return f"{day}rd"
    else:
        return f"{day}th"
