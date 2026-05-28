import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

results = pd.read_csv('results.csv')
drivers = pd.read_csv('drivers.csv')
constructors = pd.read_csv('constructors.csv')
races = pd.read_csv('races.csv')
qualifying = pd.read_csv('qualifying.csv')
circuits = pd.read_csv('circuits.csv')

df = results.merge(drivers, on='driverId')
df = df.merge(constructors,on = 'constructorId')
df = df.merge(races, on='raceId')
df = df.merge(circuits[['circuitId','name']],on='circuitId')

df['Driver'] = df['forename'] + " " + df['surname']

df['Win'] = df['positionOrder'].apply(lambda x: 1 if x==1 else 0)

ml_df = df[[
    'Driver',
    'name_x',
    'year',
    'name',
    'grid',
    'Win'
]]

print(ml_df.columns)

ml_df.columns = [
    'Driver',
    'Constructor',
    'Year',
    'Circuit',
    'GridPosition',
    'Win'
]

print(ml_df.head())

le_driver = LabelEncoder()
le_constructor = LabelEncoder()
le_circuit = LabelEncoder()

ml_df['Driver'] = le_driver.fit_transform(ml_df['Driver'])
ml_df['Constructor'] = le_constructor.fit_transform(ml_df['Constructor'])   
ml_df['Circuit'] = le_circuit.fit_transform(ml_df['Circuit'])

x = ml_df.drop('Win', axis=1)
y = ml_df['Win']

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(x_train, y_train)

predict = model.predict(x_test)

accuracy = accuracy_score(y_test, predict)
print("Accuracy: ", accuracy)

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(le_driver, open('label_encoder_driver.pkl', 'wb'))
pickle.dump(le_constructor, open('label_encoder_constructor.pkl', 'wb'))
pickle.dump(le_circuit, open('label_encoder_circuit.pkl', 'wb'))    

print('Model saved')