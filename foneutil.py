"""
Name: foneutil
Version: 0.4.4
Info: Python based script in order to record customer interactions, allowing
      the user to record relevant information from customer interaction. The
      script allows for the user to edit already entered in real time.
Requirements: Pandas, pyfiglet and termcolor modules
Created by: Andras Marton - andras.marton@wpengine.com
"""

import datetime
import readline
import os
import sys

import pandas as pd
import numpy as np
from pyfiglet import figlet_format


def clear():
    """
    Clear the screen at the start of the script
    """
    _ = os.system('clear')


try:
    from termcolor import colored
except ImportError:
    colored = None


def banner(string, color, font="speed", figlet=False):
    """
    Add a color banner on the top of the menu when loading script
    """
    if colored:
        if not figlet:
            print(colored(string, color))
        else:
            print(colored(figlet_format(string, font=font), color))
    else:
        print(string)


def rlinput(prompt, prefill=''):
    """
    Function to allow the user to go back and edit the existing variable
    data when entering call info. This in effect allows the form to act as
        an interactive utility.
    """
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def display_file_content(filename):
    """
    This function reads in the data file and displays the rows along with a
    numberical index value. The pd.set_option() is there to stop the displayed
    rows being truncated.
    """
    clear()
    df_csv = pd.read_csv(filename)
    df_csv = df_csv.replace(np.nan, '', regex=True)
    pd.set_option('display.max_rows', None)
    print(df_csv)


def get_record(var):
    """
    Pull the row related to the index ID that is provided by the user when
    the read records area.
    """
    df_csv = pd.read_csv(filename)
    index_id = int(var)
    display_record = df_csv.iloc[index_id]
    pd.set_option('display.max_colwidth', 2000)
    format_row(display_record)


def format_row(row_number):
    """
    Display row data in a similar setup to the data_entry() function when pulling
    the data from the file.
    """
    print(f'\nDate: {row_number["date"]}')
    print(f'Customer name: {row_number["name"]}')
    print(f'Domain: {row_number["domain"]}')
    print(f'Install: {row_number["install"]}')
    print(f'Pin: {row_number["pin"]}')
    print(f'Conundrum: {row_number["conundrum"]}\n')


def display_record(filename):
    """
    Retrieve data from data.csv. Currently looking at improving the display
        of this data and to create a more interactive menu/search function
    """
    display_file_content(filename)
    while True:
                choice = input("\nEnter index ID to look up record or type [E]xit to return to Main Menu: ")
                if choice.isdigit():
                    try:
                        get_record(choice)
                    except IndexError:
                        print("Could not find requested index.")
                elif choice.lower() in ['e', 'exit']:
                    mainMenuHeader()
                    break
                else:
                    mainMenuHeader()
                    banner("\nIncorrect input provided.", color="yellow")
                    break
    pd.reset_option('display.max_colwidth')


def remove_record(filename):
    """
    This deletes a specific row in the data.csv file that is defined by way
    of user input.
    """
    display_file_content(filename)
    while True:
        try:
            record = input("\nProvide the record index to delete or type [E]xit to return to Main Menu: ")
            if record.lower() in ['e', 'exit']:
                mainMenuHeader()
                break
            else:
                index_id = int(record)
                try:
                    df_csv = pd.read_csv(filename)
                    df_csv  = df_csv.drop(index=[index_id])
                    df_csv.to_csv(filename, index=False)
                    mainMenuHeader()
                    banner("\nNotice:", color="yellow")
                    banner("Record {} has been deleted. Returning to main menu.".format(index_id), color="yellow")
                    break
                except FileNotFoundError:
                    print("Unable to find file. Make sure data.csv exists.")
                except IOError:
                    print("Unable to open file.")
        except IndexError:
            print("Data doesn't exist.")
        except ValueError:
            print("Incorrect value")
            

def data_entry(filename):
    """
    Obtain data from the user to save. The user will be able to go back and
    edit the data already entered and it will be saved once user goes back
    to the main menu.
    """
    var_name = ""
    var_domain = ""
    var_install = ""
    var_pin = ""
    var_conundrum = ""
    date_now = datetime.datetime.now() #  Set time for when script runs
    while True:
        try:
            clear()
            date_formatted = date_now.strftime("%x" + " " + "%X")
            print(date_formatted)
            print("Name: " + var_name)
            print("Domain: " + var_domain)
            print("Install: " + var_install)
            print("Pin: " + var_pin)
            print("Conundrum: " + var_conundrum)
            print("\n[S]ave \t [E]xit\n")
            choice = str(input("Which option do you want to edit? "))
            readline.set_pre_input_hook(None)
            if  choice.lower() in ['n', 'name']:
                var_name = rlinput("Enter name: ", var_name)
            elif choice.lower() in ['d', 'domain', 'url']:
                var_domain = rlinput("Enter domain: ", var_domain)
            elif choice.lower() in ['i', 'install', 'site']:
                var_install = rlinput("Enter install: ", var_install)
            elif choice.lower() in ['p', 'pin']:
                var_pin = rlinput("Enter pin: ", var_pin)
            elif choice.lower() in ['c', 'notes', 'conundrum']:
                var_conundrum = rlinput("Enter conundrum: ", var_conundrum)
            elif choice.lower() in ['s', 'save']:
                menu_options = input("This will save and close this form. Continue? [y/n] ")
                if menu_options.lower() in ['y', 'yes']:
                    notes = {
                            'date': [date_formatted],
                            'name': [var_name],
                            'domain': [var_domain],
                            'install': [var_install],
                            'pin': [var_pin],
                            'conundrum': [var_conundrum]
                    }
                    df = pd.DataFrame(data=notes)
                    try:
                        df.to_csv(filename, mode='a', header=False, index=False)
                        mainMenuHeader()
                        break
                    except IOError as e:
                        print("I/O error: {0}".format(e))
                        sys.exit(1)
                elif menu_options.lower() in ['n', 'no']:
                    continue
            elif choice.lower() in ['e', 'exit', 'q', 'return']:
                menu_options = input("Do you wish to exit the form without saving? [y/n] ")
                if menu_options.lower() in ['y', 'yes']:
                    mainMenuHeader()
                    break
                elif menu_options.lower() in ['n', 'no']:
                    continue
            else:
                print("invalid INPUT!!")
                continue
        except ValueError:
            print("Invalid input.")


def update_record(filename):
    display_file_content(filename)
    record = input("\nPlease provide the index ID to review: ")
    df_csv = pd.read_csv(filename)
    df_csv = df_csv.replace(np.nan, '', regex=True)
    index_id = int(record)
    display_record = df_csv.iloc[index_id]
    pd.set_option('display.max_colwidth', 2000)
    df_csv  = df_csv.drop(index=[index_id])
    df_csv.to_csv(filename, index=False)

    date_formatted = display_record["date"]
    var_name = display_record["name"]
    var_domain = display_record["domain"]
    var_install = display_record["install"]
    var_pin = display_record["pin"]
    var_conundrum = display_record["conundrum"]

    print(f'\nName: {display_record["name"]}')
    print(f'Domain: {display_record["domain"]}')
    print(f'Install: {display_record["install"]}')
    print(f'Pin: {display_record["pin"]}')
    print(f'Conundrum: {display_record["conundrum"]}')

    while True:
        try:
            clear()
            print(f'\nName: {var_name}')
            print(f'Domain: {var_domain}')
            print(f'Install: {var_install}')
            print(f'Pin: {var_pin}')
            print(f'Conundrum: {var_conundrum}')
            #print("\n[S]ave \t [E]xit\n")
            print("\n[S]ave\n")
            choice = str(input("Which option do you want to edit? "))
            readline.set_pre_input_hook(None)
            if  choice.lower() in ['n', 'name']:
                var_name = rlinput("Enter name: ", var_name)
            elif choice.lower() in ['d', 'domain', 'url']:
                var_domain = rlinput("Enter domain: ", var_domain)
            elif choice.lower() in ['i', 'install', 'site']:
                var_install = rlinput("Enter install: ", var_install)
            elif choice.lower() in ['p', 'pin']:
                var_pin = rlinput("Enter pin: ", var_pin)
            elif choice.lower() in ['c', 'notes', 'conundrum']:
                var_conundrum = rlinput("Enter conundrum: ", var_conundrum)
            elif choice.lower() in ['s', 'save']:
                menu_options = input("This will save and close this form. Continue? [y/n] ")
                if menu_options.lower() in ['y', 'yes']:
                    notes = {
                            'date': [date_formatted],
                            'name': [var_name],
                            'domain': [var_domain],
                            'install': [var_install],
                            'pin': [var_pin],
                            'conundrum': [var_conundrum]
                    }
                    df = pd.DataFrame(data=notes)
                    try:
                        df.to_csv(filename, mode='a', header=False, index=False)
                        mainMenuHeader()
                        break
                    except IOError as e:
                        print("I/O error: {0}".format(e))
                        sys.exit(1)
                elif menu_options.lower() in ['n', 'no']:
                    continue
            # Comenting out for the time being as unable to get it working as expected
            # and currently if you were to exit, there will be data loss
            #elif choice.lower() in ['e', 'exit', 'q', 'return']:
            #    menu_options = input("Do you wish to exit the form without saving? [y/n] ")
            #    if menu_options.lower() in ['y', 'yes']:
            #        mainMenuHeader()
            #        break
            #    elif menu_options.lower() in ['n', 'no']:
            #        continue
            else:
                print("invalid INPUT!!")
                continue
        except ValueError:
            print("Invalid input.")
    pd.reset_option('display.max_colwidth')

def create_data_file(filename):
    """
    Create the data file used by the script.
    """
    try:
        with open(filename, "w") as f:
            f.write("date,name,domain,install,pin,conundrum\n")
    except IOError as err:
        print("I/O error: {0}".format(err))


def mainMenuHeader():
    """
    Print the main menu to display options.
    """
    clear()
    banner("foneutil", color="blue", figlet=True)
    banner("Welcome to the foneutil note application", color="red")
    print("\n[R]ead file")
    print("[A]dd record")
    print("[D]elete record")
    print("[U]pdate record")
    print("[E]xit")


def mainMenu():
    """
    Build out the initial menu for the user to interact with
    """
    mainMenuHeader()
    while True:
        try:
            selection = str(input("\nEnter choice: "))
            if selection.lower() in ['r', 'read']:
                display_record('data.csv')
            elif selection.lower() in ['a', 'add']:
                data_entry('data.csv')
            elif selection.lower() in ['d', 'delete']:
                remove_record('data.csv')
            elif selection.lower() in ['u', 'update']:
                update_record('data.csv')
            elif selection.lower() in ['e', 'exit']:
                break
            else:
                mainMenuHeader()
                banner("\nError: invalid input! Please select correct option.", color="red")
                continue
        except ValueError:
            print("Invalid choice. Please select correct option.")
    sys.exit(0)


if __name__ == '__main__':
    """
    Check if 'data.csv' exists
    """
    filename = "data.csv"
    if os.path.exists(filename):
        if os.stat(filename).st_size == 0:
            create_data_file('data.csv')
            mainMenu()
        else:
            mainMenu()
    else:
        create_data_file('data.csv')
        mainMenu()
