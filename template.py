# !/usr/bin/env python3
# -*- coding: utf-8 -*-


# Print cotegories instructions
def instruction_browsepages():
    instructions = """
    Instructions commands:
    Find      -- Find the popular articles in the specific category
    Browse    -- Browse the specific category


    Categories' commands:
    NBA       -- NBA
    MH        -- Monster Hunter World
    Gossiping -- Gossipings
    Sex       -- Sex
    Movie     -- Movies
    LoL       -- League of Legend
    Baseball  -- baseball
    Beauty    -- Beauty
    (You can also enter other categories you know the name)

    exit      -- Leave program

    Please input Instruction, Category and how many Pages to read:
    """
    print(instructions)


# Print error message
def error_msg():
    print("""
            ************************************
            *** Oops, something goes wrong!! ***
            ***                              ***
            ***      Please try again!!      ***
            ************************************
    """)
    help_msg()


def help_msg():
    # Help message
    print("""
### help      -- Look for instructions
    """)


def bye_msg():
    print("""
            ************************************
            ***            Bye!!             ***
            ************************************
    """)
