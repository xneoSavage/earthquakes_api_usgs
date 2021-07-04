import requests
from plotly.graph_objects import Layout
from plotly import offline
print('Type a date in format dd-mm-yy')
starttime = input('Start time: ')
endtime = input('End time: ')
parameters = {
    "format": 'geojson',
    "starttime": starttime,
    "endtime": endtime,
}

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
response = requests.get(url, params=parameters)
data = response.json()

mags, lons, lats, hover_texts = [], [], [], []
map_name = data['metadata']['title']
all_data_dict = data['features']
eq_dict = {}

for eq_dict in all_data_dict:
    if (eq_dict['properties']['mag'] is None) is not True and (eq_dict['properties']['mag'] > 0.0):
        mags.append(eq_dict['properties']['mag'])
        lons.append(eq_dict['geometry']['coordinates'][0])
        lats.append(eq_dict['geometry']['coordinates'][1])
        hover_texts.append(eq_dict['properties']['title'])
    else:
        print(f"{eq_dict['properties']['mag']} is not valid data")

data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text': hover_texts,
    'marker': {
        'size': [3 * mag for mag in mags],
        'color': mags,
        'colorscale': 'Viridis',
        'reversescale': True,
        'colorbar': {'title': 'Magnitude'}
    },
}]

my_layout = Layout(title=map_name)
fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='global.html')
