from tkinter import *
import tkinter.messagebox as mb
from Budget import *
from Loader import load_budget, save_budget

TITLE = 'Budgeting Fool'
BUTTON_WIDTH = 10
NUMBER_ENTRY_WIDTH = 10
PAD_PIXELS = 4
TEXT_HEIGHT = 10
TEXT_WIDTH = 30
NUMERIC_CHARACTERS = set({ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' })

class Budgeting_Fool(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('600x300')
        self.title(TITLE)
        self.budget = load_budget()
        self.items = []
        
        #Set up the UI
        self.item_frame = Frame(self)
        self.item_frame.pack(expand = 'true', fill = 'both', anchor = 'n')
        self.button_frame = Frame(self)
        self.button_frame.pack(expand = 'true', fill = 'x', anchor = 's')
        Button(self.button_frame, text = 'Calculate', command = self.calculate, width = BUTTON_WIDTH).pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)
        Button(self.button_frame, text = '-', command = self.remove_item, width = BUTTON_WIDTH).pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)
        Button(self.button_frame, text = '+', command = self.add_item, width = BUTTON_WIDTH).pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)

        #Load in saved data if it's there
        for item in self.budget.items:
            self.add_item(item)

    def add_item(self, item = None):
        new_item = Item_Frame(self.item_frame, item)
        new_item.pack(expand = 'true', fill = 'x', anchor = 'n')
        self.items.append(new_item)
        if item == None:
            save_budget(self.budget)

    def remove_item(self):
        self.bind_class('Label', '<Button-1>', self.remove_item_event)

    def remove_item_event(self, event: Event):
        self.budget.remove_item(event.widget.master.item)
        event.widget.master.destroy()
        self.unbind_class('Label', '<Button-1>')
        save_budget(self.budget)

    def calculate(self):
        incomes = 0
        expenses = 0
        total = 0
        for item in self.budget.items:
            total += item.amount
            if item.amount < 0:
                expenses += item.amount / item.frequency * Frequency.YEARLY.value
            else:
                incomes += item.amount / item.frequency * Frequency.YEARLY.value

        message = 'Yearly income: \t{yinc:,.2f}\tYearly expenses: \t{yexp:.2f}\tYearly net: \t{ynet:.2f}\n'
        message += 'Monthly income:\t{minc:.2f}\tMonthly expenses:\t{mexp:.2f}\tMonthly net:\t{mnet:.2f}\n'
        message += 'Weekly income: \t{winc:.2f}\tWeekly expenses: \t{wexp:.2f}\tWeekly net: \t{wnet:.2f}\n'
        message = message.format(yinc = incomes, yexp = expenses, ynet = total,
                                 minc = incomes / 12.0, mexp = expenses / 12.0, mnet = total / 12.0,
                                 winc = incomes / 52.0, wexp = expenses / 52.0, wnet = total / 52.0)
        calculation_frame = Calculation_Frame(None, message)
        self.item_frame.pack_forget()
        self.button_frame.pack_forget()
        calculation_frame.pack(expand = 'true', fill = 'both')

class Item_Frame(Frame):
    def __init__(self, master: Frame, item = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        if item != None:
            self.item = item
        else:
            self.item = Item()
            self.item.name = 'item'
            self.item.amount = 0
            self.item.frequency = Frequency.at(4)
            master.master.budget.add_item(self.item)
        
        #Set up the frame
        #Name label and text entry
        Label(self, text = 'Name:').pack(side = 'left', anchor = 'w', padx = PAD_PIXELS, pady = PAD_PIXELS)
        self.name_string = StringVar()
        if item != None:
            self.name_string.set(item.name)
        else:
            self.name_string.set('item')
        self.name_entry = Entry(self, text = self.item.name, textvariable = self.name_string)
        self.name_entry.pack(side = 'left', anchor = 'w', padx = PAD_PIXELS, pady = PAD_PIXELS, expand = 'true', fill = 'x')
        #Dropdown for frequency and text entry
        self.frequency_string = StringVar()
        if item != None:
            self.frequency_string.set(str(item.frequency / Frequency.at_str(item.frequency_period)))
        else:
            self.frequency_string.set('1')
        self.frequency_entry = Entry(self, width = NUMBER_ENTRY_WIDTH, textvariable = self.frequency_string)
        self.frequency_entry.pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)
        self.frequency_options = Frequency.get_names()
        self.frequency = StringVar()
        if item != None:
            self.frequency.set(item.frequency_period)
        else:
            self.frequency.set('Monthly')
        OptionMenu(self, self.frequency, *self.frequency_options).pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)

        #Amount label and text entry
        self.amount_string = StringVar()
        if item != None:
            self.amount_string.set(str(item.amount))
        else:
            self.amount_string.set('0')
        self.amount_entry = Entry(self, text = str(self.item.amount), width = NUMBER_ENTRY_WIDTH, textvariable = self.amount_string)
        self.amount_entry.pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)
        Label(self, text = 'Amount:').pack(side = 'right', anchor = 'e', padx = PAD_PIXELS, pady = PAD_PIXELS)

        #Kick off the poller
        self.after(16, self.poll_updates)

    def poll_updates(self):
        self.item.name = self.name_string.get()

        #Amount update?
        text = self.amount_string.get()
        #Parse out illegal characters
        parsed = ''
        first = True
        contains_period = False
        contains_dash = False
        for c in text:
            if c == '.':
                if not contains_period:
                    contains_period = True
                    if first:
                        parsed += '0'
                    parsed += c
            elif c == '-':
                if not contains_dash and first:
                    contains_dash = True
                    parsed += c
            elif c in NUMERIC_CHARACTERS:
                parsed += c
            first = False

        self.amount_string.set(parsed)
        if parsed == '-':
            self.item.amount = 0
            self.amount_string.set('-0')
        elif parsed == '.':
            self.item.amount = 0
            self.amount_string.set('0.0')
        elif len(parsed) == 0:
            self.item.amount = 0
            self.amount_string.set('0')
        else:
            self.item.amount = float(parsed)

        #Frequency update?
        text = self.frequency_string.get()
        #Parse out illegal characters
        parsed = ''
        first = True
        contains_period = False
        for c in text:
            if c == '.':
                if not contains_period:
                    contains_period = True
                    if first:
                        parsed += '0'
                    parsed += c
            elif c in NUMERIC_CHARACTERS:
                parsed += c
            first = False

        self.frequency_string.set(parsed)
        if len(parsed) == 0:
            self.item.frequency = 0.0
            self.frequency_string.set('0')
        else:
            self.item.frequency = float(parsed) * Frequency.at(self.frequency_options.index(self.frequency.get()))

        #Frequency OptionMenu
        self.item.frequency_period = self.frequency.get()
        self.after(16, self.poll_updates)

class Calculation_Frame(Frame):
    def __init__(self, master: Frame, message: str, **kwargs):
        Frame.__init__(self, master, **kwargs)
        text = Text(self, height = TEXT_HEIGHT, width = TEXT_WIDTH)
        text.insert(1.0, message)
        text.config(state = 'disabled')
        text.pack(expand = 'true', fill = 'both', anchor = 'n')
        Button(self, text = 'Back', command = self.back_button).pack(anchor = 'se', padx = PAD_PIXELS, pady = PAD_PIXELS)

    def back_button(self):
        self.pack_forget()
        self.master.item_frame.pack(expand = 'true', fill = 'both', anchor = 'n')
        self.master.button_frame.pack(expand = 'true', fill = 'x', anchor = 's')
        self.destroy()

if __name__ == '__main__':
    bf = Budgeting_Fool()
    bf.mainloop()
    save_budget(bf.budget)