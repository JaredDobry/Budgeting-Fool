from Budget import Budget, Item

FILENAME = 'Budget.txt'

def scrape_off_char(s, c):
    out = ''
    for ch in s:
        if ch != c:
            out += ch
    return out

def load_budget():
    try:
        fr = open(FILENAME, 'r')
        lines = fr.readlines()
        fr.close()
        b = Budget()
        for line in lines:
            spl = line.split(',')
            if len(spl) != 4:
                raise ValueError
            item = Item()
            item.name = scrape_off_char(spl[0], '\n')
            item.amount = float(scrape_off_char(spl[1], '\n'))
            item.frequency = float(scrape_off_char(spl[2], '\n'))
            item.frequency_period = scrape_off_char(spl[3], '\n')
            b.add_item(item)
        return b
    except Exception:
        return Budget()

def save_budget(budget: Budget):
    try:
        fw = open(FILENAME, 'w')
        first = True
        for item in budget.items:
            if not first:
                fw.write('\n')
            else:
                first = False
            fw.write(item.name + ',' + str(item.amount) + ',' + str(item.frequency) + ',' + item.frequency_period)
        fw.close()
    except Exception:
        return