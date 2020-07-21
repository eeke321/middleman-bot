
from enum import Enum
from typing import List
from telegram import PhotoSize

class LiftState(Enum):
    NONE = 0
    SHORE = 1
    OPENING = 2
    SITE = 3
    LOST = 4

class Lift:
    def __init__(self, id, photo, state, site, opening, note):
        self.id = id
        self.photo = photo
        self.state = state
        self.site = site
        self.opening = opening
        self.note = note

import openpyxl

def load_lifts(lift_list : List):
    wb = openpyxl.load_workbook('lifts.xlsx')
    
    lifts_sheet = wb['lifts']


    i = 1

    while True:
        i += 1
        

        id = lifts_sheet.cell(row = i, column = 1).value

        if (id == None):
            break

        photo = 'https://telegram.org/img/t_logo.png'
        state = lifts_sheet.cell(row = i, column = 2).value
        site = lifts_sheet.cell(row = i, column = 3).value
        opening = lifts_sheet.cell(row = i, column = 4).value
        note = lifts_sheet.cell(row = i, column = 5).value

        lift_list.append(Lift(id, photo, state, site, opening, note))

def add_lift(lift : Lift):
    wb = openpyxl.load_workbook('lifts.xlsx')
    lifts_sheet = wb['lifts']

    r = lift.id + 3

    lifts_sheet.cell(row = r, column = 1).value = lift.id
    lifts_sheet.cell(row = r, column = 2).value = lift.state.name
    lifts_sheet.cell(row = r, column = 3).value = lift.site
    lifts_sheet.cell(row = r, column = 4).value = lift.opening
    lifts_sheet.cell(row = r, column = 5).value = lift.note

    wb.save('lifts.xlsx')

    print("Lift added!")

def save_lifts(lift_list : List):
    wb = openpyxl.load_workbook('lifts.xlsx')


