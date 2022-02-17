import pandas as pd
import numpy as np
import pathlib
from app import app
def queryData():
    # database query step goes here, importing for CSV for demo purposes

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../datasets").resolve()


    df = pd.read_csv(DATA_PATH.joinpath("dataset.csv"))
    # format passenger class
    df['Pclass'] = df['Pclass'].astype('str')
    df['Pclass'] = df['Pclass'].replace(
        to_replace=['1', '2', '3'],
        value=['First', 'Second', 'Third'])

    # format passenger gender
    df['Sex'] = df['Sex'].replace(
        to_replace=['male', 'female'],
        value=['Male', 'Female'])

    # format embark location

    df['Embarked'] = df['Embarked'].replace(
        to_replace=['C', 'Q', 'S'],
        value=['Cherbourg', 'Queenstown', 'Southampton'])

    # format ticket price into currency
    #    df['Fare'] = df['Fare'].apply(lambda x: f"${x:.2f}")
    df['Fare'] = df['Fare'].round(2)
    # rename and reorder columns
    df.rename(columns={'PassengerId': 'PassengerID', 'Pclass': 'Class'}, inplace=True)
    df = df[['PassengerID', 'Name', 'Age', 'Sex', 'Class', 'Survived', 'Ticket', 'Fare', 'Cabin', 'Embarked']]

    # drop any rows containing a null value in age col
    df['Age'].fillna(df['Age'].mean(), inplace=True)
    df['Age'] = df['Age'].round(0)

    # create age grouping helper column
    age_group_criteria = [(df['Age'] <= 10),
                          ((df['Age'] > 10) & (df['Age'] <= 20)),
                          ((df['Age'] > 20) & (df['Age'] <= 30)),
                          ((df['Age'] > 30) & (df['Age'] <= 40)),
                          ((df['Age'] > 40) & (df['Age'] <= 50)),
                          ((df['Age'] > 50) & (df['Age'] <= 60)),
                          ((df['Age'] > 60) & (df['Age'] <= 70)),
                          (df['Age'] > 70)]

    age_group_names = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']

    df['Age_Group'] = np.select(age_group_criteria, age_group_names)
    df['Age_Group'] = df['Age_Group'].astype('category')

    return df


