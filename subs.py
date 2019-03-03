import utils.web as w
import re
import datetime

from matplotlib import pyplot as plt
import mpldatacursor

user = 'gamegrumps'

s = w.get_and_clean(f'https://www.trackalytics.com/youtube/user/{user}', tags=['link', 'style', 'noscript', 'meta', 'iframe'])

head = s.find('head')

last = head.find_all('script')[-1]

t = last.get_text(strip=True).replace('\n', '').replace('Date.UTC(', '').replace('-1', '')

r = re.findall(r'name: *\'Subscribers\', *data: *(.*)\], +\]', t)[0]

rs = r.split(',  ')

rso = rs[0]

l = [i.replace('[','').replace(']','').replace(')', '').strip().split(', ') for i in rso.split('],[')]

n = [(datetime.datetime(int(i[0]), int(i[1]), int(i[2])), int(i[3])) for i in l]

def show_plot():
    plt.ioff()

    plt.rcParams['figure.figsize'] = [20, 15]

    _fig, ax = plt.subplots()

    x = [d[0] for d in n]
    y = [d[1] for d in n]

    ax.scatter(x, y, s=5)

    mpldatacursor.datacursor(date_format="%x", bbox={
        'boxstyle': 'round,pad=0.5',
        'fc': 'lightblue',
        'alpha': 0.95,
        'edgecolor': 'black'
    })

    plt.ion()

    plt.show()
