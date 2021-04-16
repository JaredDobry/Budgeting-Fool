from enum import Enum

class Frequency(Enum):
    DAILY = 1.0
    WEEKLY = 7.0
    BI_WEEKLY = 14.0
    BI_MONTHLY = 365.0 / 24.0
    MONTHLY = 365.0 / 12.0
    BI_ANUALLY = 365.0 / 2.0
    YEARLY = 365.0

    def get_names():
        return [ 'Daily',
                'Weekly',
                'Bi-Weekly',
                'Bi-Monthly',
                'Monthly',
                'Bi-Anually',
                'Yearly' ]

    def at(i: int):
        vals = [1.0, 7.0, 14.0, 365.0 / 24.0, 365.0 / 12.0, 365.0 / 2.0, 365.0]
        return vals[i]

    def at_str(s: str):
        i = 0
        names = Frequency.get_names()
        while i < len(names):
            if s == names[i]:
                return Frequency.at(i)
            i += 1
        return Frequency.at(4) #Monthly as default

class Item:
    name: str
    amount: float #dollars
    frequency: float #days
    frequency_period: str #What tag

class Budget:
    items: list = []

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item: Item):
        for i in self.items:
            if item.name == i.name and item.amount == i.amount and item.frequency == i.frequency and item.frequency_period == i.frequency_period:
                self.items.remove(i)
                break

    def find_item(self, name: str):
        for item in self.items:
            if name == item.name:
                return item
        return None

    def name_used(self, name: str):
        for item in self.items:
            if name == item.name:
                return True
        return False