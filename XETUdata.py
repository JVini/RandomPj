#!/usr/bin/env python
"""
    File name: XETUdata.py
    Author: Jorge Quintero
    Date created: 10/30/2017
    Date last modified: 10/31/2017
    Python version: 3.6
"""
# TODO: In the data productions function, it cannot handle dates of two months.
# TODO: In generate resume, handle if the productData file is empty.
# TODO: Check if the user put a day between the writen ones on productData file.
from time import sleep
from calendar import month_name


def menu():
    """Displays to the user the variety of commands he can use."""
    print("\nWelcome, please choose the action you want to perform:\n\n\
          \t1.- Add data of the productions.\n\
          \t2.- Generate a resume of the productions.\n\
          \t3.- Remove the data of the file.\n\
          \t4.- Check specific data of a certain day.\n\
          \t9.- Exit.\n")


def checker(msg):
    """Ask the user for an input and checks it.

    Keyword arguments:
        msg (str): Is the instruction you give the user.

    Returns:
        int: A correct number of user input.
    """
    while True:
        try:
            u_in = int(input(msg))
        except ValueError:
            print("Sorry, invalid input, please try again.")
        else:
            break
    return u_in


def data_productions():
    """User manually writes data to a file.

    Description:
        We ask the user for the period which the data corresponds to, next we request
        the info of every line and turn, in each day of the week.

    Returns:
        It returns the two days of the user input.
    """
    while True:
        print("\nPlease, enter the following data:")
        info = input("Day of start, day of end, month and year, all in numbers and separated by commas: ")
        # Splits the string and eliminates the possible spaces between the commas.
        pro_info = [data.strip() for data in info.split(",")]
        # This checks if the user inputs correct information.
        if len(pro_info) != 4:
            print("\nSorry, you must enter correct information.\n")
            return
        if (int(pro_info[1]) - int(pro_info[0]) == 6) and 0 < int(pro_info[2]) < 12 and len(pro_info[3]) == 4:
            break
        print("Please, reenter a valid input.")
        sleep(2)
    # The return variable.
    beauty = [pro_info[0], [pro_info[1]]]
    # Converts the number of the number to it's name.
    month = str(month_name[int(pro_info[2])])
    first_line = "Production line report from %s to %s %s %s\n" \
                 % (pro_info[0], pro_info[1], month, pro_info[3])
    # Here we open the file and the first line we created above.
    with open('productData.txt', 'a') as file:
        file.write(first_line)
    # This loops thought all days, all lines and all turns and adds the data each time.
    for day in range(1, 8):
        print("\nEnter the data of day " + str(day))
        for line in range(1, 6):
            for turn in range(1, 4):
                print("\nWrite the following data of the line %s and turn %s"
                      % (str(line), str(turn)))
                # The abs() method is just in case the user writes negatives.
                products = abs(checker("Number of products: "))
                stopped = abs(checker("Number of times it stopped: "))
                togo_data = "Line %s,Turn %s,%s-%s-%s,%s,%s\n"\
                            % (str(line), str(turn), pro_info[0], pro_info[2],
                               pro_info[3], str(products), str(stopped))
                with open('productData.txt', 'a') as file:
                    file.write(togo_data)
        # This line changes the number of the day.
        pro_info[0] = int(pro_info[0]) + 1
    return beauty


def generate_resume():
    """Writes a resume of the productData.txt in dataResume.txt file.

    Description:
        Calls two other functions in order to extract the important information
        of productData.txt, then we write all the information extracted into a
        nice formatted view for the user.

    Returns:
        It doesn't return anything, it writes on a file.
    """
    # We take the info of the first line of the file product data.
    with open('productData.txt', 'r') as file:
        checking = file.readline()
        week_days = [checking[28:30], checking[34:36]]
    # Assigns to each line it's corresponding dictionary.
    l1, l2, l3, l4, l5 = (dict_gen(1), dict_gen(2), dict_gen(3), dict_gen(4), dict_gen(5))
    production_lines = [l1, l2, l3, l4, l5]
    # This will count the days.
    counter = 0
    with open('dataResume.txt', 'a') as resume:
        testing = 'Week from %s to %s\n\n' % (week_days[0], week_days[1])
        resume.write(testing)
        for line in production_lines:
            counter += 1
            for turn in range(1, 4):
                # The next two lines coverts all the strings in the lists to ints.
                products = [int(i) for i in line[turn][0]]
                stopped_times = [int(i) for i in line[turn][1]]
                resume.write('Production line number: ' + str(counter) + '\n')
                resume.write('Turn: ' + str(turn) + '\n')
                resume.write('Total produced products of the week: %s\n' % (str(sum(products))))
                resume.write('Times the line stopped: %s\n' % (str(sum(stopped_times))))
                resume.write('Day in which the machine stopped most: %s\n\n' % (most_stops(line, turn)))


def most_stops(line, turn):
    """Analyze the data to determine in which day the production line stopped more.

    Keyword arguments:
        line (dict): The dictionary which contains all the products and times the production
                        line stopped.
        turn (int): The turn wanted to analyze.

    Returns:
        The date of the most stops in the desired turn.
    """
    vartop = [int(i) for i in line[turn][1]]
    vartop = max(vartop)
    with open('productData.txt', 'r') as data:
        data.readline()
        for i in data:
            i = i.strip('\n')
            i = i.split(',')
            if int(i[4]) == vartop and i[1] == 'Turn ' + str(turn):
                return i[2]


def dict_gen(line):
    """Generates a dictionary.

    Keyword arguments:
        line (int): Is the line the function will take as reference for search.

    Returns:
        A dictionary that contains 3 keys, each of them represents the a turn of
        the production line, with two list, one containing all the products of the
        turn, and the other all the times it stopped.
    """
    # Creates a dictionary for each line and that represents the 3 turns of each line.
    x = dict([(i, [[], []]) for i in range(1, 4)])
    for turn in range(1, 4):
        with open('productData.txt', 'r') as data:
            # Reading the first line which data isn't needed.
            data.readline()
            for file_line in data:
                working = file_line.strip('\n')
                file_line = working.split(',')
                if file_line[0] == ("Line " + str(line)) and file_line[1] == ("Turn " + str(turn)):
                    x[turn][0].append(file_line[3])
                    x[turn][1].append(file_line[4])
    return x


def par_consult(line, turn, day):
    """Search the products and stops of a certain line and turn in a day.

    :param line: Is the line the user wants to check.
    :param turn: Is the turn the user wants to check.
    :param day: Is the specific day of the data.
    :return: The products and stops depending on the parameters of above.
    """
    with open('productData.txt', 'r') as file:
        file.readline()
        for data in file:
            data = data.strip('\n')
            data = data.split(',')
            desired_date = data[2].split('-')
            if data[0] == "Line " + str(line) and data[1] == "Turn " + str(turn) and desired_date[0] == str(day):
                return [data[3], data[4]]


# Checks if the predetermined files exists and can be used, if not, creates them.
for name in ['productData', 'dataResume']:
    try:
        test = open(name + '.txt', 'a')
        test.close()
    except IOError:
        print('Something went wrong. Contact the administrator.')
        exit()
# Loop of the program
while True:
    menu()
    sleep(2)
    action = checker('Enter the action to perform based on the menu: ')
    if action == 1:
        nice = data_productions()
        if nice:
            print("\nAll data has been stored in 'productData.txt'")
    elif action == 2:
        generate_resume()
        print("The resume has been generated and stored in 'dataResume.txt'")
    elif action == 3:
        print('Everything in the file will be deleted in 2 seconds.')
        sleep(2)
        open('productData.txt', 'w').close()
        open('dataResume.txt', 'w').close()
        print("Deleted.")
    elif action == 4:
        while True:
            day = checker("\nSpecify the day of the info (Example: 29): ")
            # The next lines just prevents errors at the search of the info.
            line = checker("Enter the production line: ")
            if 1 <= line <= 5:
                turn = checker("Enter the turn you want to check: ")
                if 1 <= turn <= 3:
                    break
            print("Please, reenter the info.")
        info = par_consult(line, turn, day)
        print(("\nIn the day %s of the month, the line %s in the turn %s had:\n" +
              "\tProducts: %s\n\tStops: %s") % (day, line, turn, info[0], info[1]))
        sleep(2)
    elif action == 9:
        break
    else:
        print("You need to choose a number of the menu.\n")
    sleep(1)


print('%sThank you for using the program, you will now exit.\nBye bye.' % ("\n" * 100))
exit()
