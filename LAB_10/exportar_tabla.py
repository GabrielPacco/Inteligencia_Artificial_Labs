import pandas as pd
import dataframe_image as dfi

data = [
    ['sí', 'grave', 'leve', 'leve', 'Covid-19'],
    ['sí', 'moderado', 'leve', 'moderado', 'Covid-19'],
    ['no', 'moderada', 'leve', 'moderada', 'SARS-CoV1'],
    ['no', 'grave', 'leve', 'leve', 'Covid-19'],
    ['sí', 'moderado', 'leve', 'moderado', 'Covid-19'],
    ['sí', 'grave', 'moderado', 'moderado', 'SARS-CoV1'],
    ['no', 'moderado', 'moderado', 'moderado', 'SARS-CoV1'],
    ['no', 'moderado', 'grave', 'leve', 'Covid-19'],
    ['sí', 'moderado', 'grave', 'moderado', 'SARS-CoV1'],
    ['no', 'moderado', 'grave', 'grave', 'SARS-CoV1'],
    ['no', 'grave', 'leve', 'grave', 'Covid-19'],
    ['no', 'leve', 'leve', 'grave', 'SARS-CoV1']
]

columns = ['fiebre', 'tos', 'fatiga', 'dolor', 'enfermedad']

df = pd.DataFrame(data, columns=columns)

dfi.export(df, 'tabla.png')