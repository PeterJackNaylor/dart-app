
import plotly.express as px
import pandas as pd 
import json

def dart_plot():
    ## dart figure
    df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')
    with open('ressources/darts.geojson', 'r') as f:
        geo_darts = json.loads(f.read())

    fig = px.choropleth(df_darts, geojson=geo_darts, color="color",
                        locations="id", featureidkey="properties.id"
                    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig