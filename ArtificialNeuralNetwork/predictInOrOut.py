import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:-1].values
y = dataset.iloc[:, -1].values

print(X)
print(y)


# Change labels of male, female -> 0, 1
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])


# Encode country to one-hot array, since giving it a continous value wouldn't make sense
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# Split into training and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature scaling!
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Building the actual ANN
ann = tf.keras.models.Sequential()

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid')) # We want sigmoid since it's a binary output, would have taken 'softmax' otherwise


# Compile
ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy']) 
# adam is preferred for stochastic gradient descent
# binary_crossentropy for classification, crossentropy for non-binary

# Run the epochs
ann.fit(X_train, y_train, batch_size = 32, epochs = 100)

# Cheggit
to_check = sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])
print(ann.predict(to_check) > 0.7)

# Check bulk
y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.7)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

# Confusion matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))

