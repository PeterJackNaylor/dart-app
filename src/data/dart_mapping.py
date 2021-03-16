import pandas as pd



mapping_id_value = {
    0: 6,
    1: 13,
    2: 4,
    3: 18,
    4: 1,
    5: 20,
    6: 5,
    7: 12,
    8: 9,
    9: 14,
    10: 11,
    11: 8,
    12: 16,
    13: 7,
    14: 19,
    15: 3,
    16: 17,
    17: 2,
    18: 15,
    19: 10
}

ids, value, coef, color = [], [], [], []

ids = ids + ["25.0", "25.2"]#, "25.2"]
value = value + [25, 25]#, 25]
coef = coef + [1, 2]#, 2]
color = color + [0, 1]#, 1]

for i in range(0, 20):
    ids = ids + [f"{i}.2", f"{i}.3", f"{i}.0.0", f"{i}.0.1"]
    value = value + [mapping_id_value[i] for j in range(4)]
    coef = coef + [2, 3, 1, 1]
    if i % 2:
        spec = 0 # green
        cent = 2 # white
    else:
        spec = 1 # red
        cent = 3 # black
    color = color + [spec, spec, cent, cent]



dic_darts = {
    'id': ids,
    'value': value,
    'coef': coef,
    'color': color
}


df_darts = pd.DataFrame(dic_darts)
df_darts.to_csv('ressources/mapping_dart_geojson.csv', index=False)
