import requests
import json
import polyline
import folium

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc)
    if r.status_code!= 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }

    return out

def getRouteFigure(route):
    figure = folium.Figure(width=100,height=100)
    m = folium.Map(location=[(route['start_point'][0]),
                            (route['start_point'][1])], 
                            zoom_start=15)
    m.add_to(figure)
    m._id = "map"
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(color='red')).add_to(m)
    figure.render()
    return figure