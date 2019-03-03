import os.path
import pickle

import matplotlib.dates as mdates
import mpldatacursor
import numpy as np
import youtube_dl
from dateutil.parser import parse
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

#from datetime import datetime

user = 'GameGrumps'
min_views = 200000

fname = user + '.pkl'

if os.path.isfile(fname):
    print('Found file')
    result = pickle.load(open(user + '.pkl', 'rb'))

else:
    print('Scraping...')
    ydl_opts = {
        'format': 'worst',
        'skip_download': True,
        'ignoreerrors': True,
        'geo_bypass': True,
        'youtube_include_dash_manifest': False
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        result = ydl.extract_info(
            'https://www.youtube.com/user/' + user
        )

    with open(fname, 'wb') as output:
        pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)

e = result['entries']
data = []
for i in e:
    d = {k: v for k,v in i.items() if k in ('title', 'webpage_url', 'view_count', 'like_count', 'dislike_count')}
    d['upload_date'] = parse(i['upload_date'])  # not returning time?
    data.append(d)

data2 = [n for n in data if n['view_count'] > min_views]

#min_date = datetime(2016, 6, 13)
#max_date = datetime(2016, 6, 29)
## youtube deleted bots around this time
#[d for d in data if min_date <= d['upload_date'] <= max_date]


# - Plot

def show_plot():
    plt.ioff()

    degree = 1

    register_matplotlib_converters()

    plt.rcParams['figure.figsize'] = [20, 15]

    years_fmt = mdates.DateFormatter('%Y-%m-%d')

    fig, ax = plt.subplots()

    dataset = data2

    dates = [y['upload_date'] for y in dataset]

    y_a = np.array([x['view_count'] for x in dataset])
    x_a = np.array([dd.timestamp() / 10000 for dd in dates])

    z, resid = np.polyfit(x_a, y_a, degree, full=True)[:2]

    #y_a_fit = np.polyval(z, x_a)
    #y_a_adj = y_a - y_a_fit

    p = np.poly1d(z)

    scats = []
    for v in dataset:
        y = v['view_count']
        x = v['upload_date']
        sc = ax.scatter(x, y, s=20, label='{} | {} | {:,}'.format(
            v['title'], x.strftime('%Y-%m-%d'), y
        ))

        scats.append(sc)

    ax.plot(dates, p(x_a), 'r--')

    ax.xaxis.set_major_formatter(years_fmt)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d %H')

    fig.autofmt_xdate()

    plt.title('y = {0:.4f}(x) {2} {1:+.4f}  RSq: {3}'.format(
        round(z[0], 4), round(z[-1], 4),
        ' '.join(['{:+.4f}(x^{})'.format(round(fc, 4), ii + 2) for ii, fc in enumerate(z[1:-1])]),
        round(1 - (resid / (y_a.size * y_a.var()))[0], 4)
    ))
    plt.xlabel('date')
    plt.ylabel('views')

    plt.subplots_adjust(top=.94, bottom=.12, right=.98, left=.04)

    #plt.show()

    mpldatacursor.datacursor(
        scats, formatter='{label}'.format, keep_inside=True, hover=True, bbox={
            'boxstyle': 'round,pad=0.5',
            'fc': 'lightblue',
            'alpha': 0.95,
            'edgecolor': 'black'
        }
    )

    plt.ion()
