# This is a collection of functions that can be used for input and output

import os
import platform

def clear_screen():
    """
    Clears terminal screen depending on operating system
    """
    
    os_str = platform.system()
    if os_str=='Windows':
        os.system('cls')
    elif os_str=='Linux':
        os.system('clear')
    return True
        
def yn_input(message,default):
    """
    Function will ask the user the message (appended by a [Y/n], 
    with the default value made a capital letter)
    It returns True or False
    """
    
    if (default == "Y")|(default == "y"):
        append_string = "[Y/n] "
    elif (default == "N")|(default == "n"):
        append_string = "[y/N] "
    else:
        raise Exception("Wrong usage for yn_input, default must be \"y\" or \"n\"")

    check_write_input = False
    while check_write_input == False:
        write_input_str = raw_input(message + append_string)
        if write_input_str=="":
            write_input_str=default
            
        if (write_input_str=="n")|(write_input_str=="N"):
            check_write_input = True
            write_input = False
        elif (write_input_str=="y")|(write_input_str=="Y"):
            check_write_input = True
            write_input = True
        else:
            print "Please choose \"y\", \"n\" or \"\" "
    return write_input
    
def print_time_table(reader):
    """
        prints the content of a csv file specified by "reader", but skipping
        every second colom as from two onwards.
    """
    
    for rownum, row in enumerate(reader):
        print_string = ""
        for colnum, col in enumerate(row):
            if colnum in [0,1,3,5,7,9]:
                print_string += col.rjust(10)
                
        print print_string
        
    return True
            
            
            
            