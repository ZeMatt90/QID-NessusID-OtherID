import pandas as pd
from sklearn.cluster import KMeans

print('Boombastic machine starting')

print('IMPORTING DATA')
train_df = pd.read_csv('train.csv')
validate_df = pd.read_csv('validate.csv')
test_df = pd.read_csv('test.csv')
print('DATA IMPORTED')

print('ENCODING DATA')
# we need to encode with one hot encoder only the values that have not an order
PORT_PREFIX = 'Port_'
cols_to_onehotencode = [col for col in train_df.columns if col.startswith(PORT_PREFIX)]
print('\t     Onehot encoded features', cols_to_onehotencode)
print('\t NOT Onehot encoded features', [col for col in train_df.columns if col not in cols_to_onehotencode])
encoded_train_df = pd.get_dummies(train_df, columns=cols_to_onehotencode)
encoded_validate_df = pd.get_dummies(validate_df, columns=cols_to_onehotencode)
encoded_test_df = pd.get_dummies(test_df, columns=cols_to_onehotencode)

print('DATA ENCODED')

print('INITILIZING CLUSTERING MODEL')
#todo OPTIMIZE HYPERPARAMETERS
#initialize algorithm
clustering_model = KMeans(n_clusters=2, random_state=0)
#fit algorithm
clustering_model.fit(encoded_train_df)
print('INITILIZED CLUSTERING MODEL')


print('PREDICT ON NEW DATA')
# evaluate algorithm or predict or whatever
predicted_test = clustering_model.predict(encoded_test_df)


print('Done, ciao.')
