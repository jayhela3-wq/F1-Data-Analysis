import pandas as pd

def preprocess():
    drivers = pd.read_csv('drivers.csv')
    constructors = pd.read_csv('constructors.csv')
    races = pd.read_csv('races.csv')
    results = pd.read_csv('results.csv')

    df = results.merge(drivers, on='driverId', how = 'left')
    df = df.merge(constructors, on='constructorId', how = 'left')
    df = df.merge(races, on='raceId', how = 'left')

    df['Driver'] = df['forename'] + ' ' + df['surname']

    df.rename(columns={
        'name_x' : 'Constructor',
        'name_y' : 'Race_Name',
        'year' : 'Year',
        'positionOrder' : 'Position',
        'points' : 'Points',
        

    }, inplace=True)

    df = df[[
        'Driver',
        'Constructor',
        'Race_Name',
        'Year',
        'Position',
        'Points',
      
    ]]



    return df
