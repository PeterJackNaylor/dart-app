
import plotly.express as px
import pandas as pd 
import json

def dart_plot():
    ## dart figure
    df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')
    with open('ressources/darts.geojson', 'r') as f:
        geo_darts = json.loads(f.read())

    fig = px.choropleth(df_darts, geojson=geo_darts, color="color",
                        locations="id", featureidkey="properties.id", hover_data={ 'id' : False, 'value': ':.2d', 'coef': ':.2d', 'color' : False }

                    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(coloraxis_showscale=False)

    return fig




#hover_data=[df_darts["value"], df_darts["coef"]]