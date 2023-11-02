import pandas as pd
from sklearn.cluster import KMeans

#def start_boomb():
print('Boombastic machine starting')

print('IMPORTING DATA')
df = pd.read_excel('test.xlsx')
#df = pd.read_csv('data.csv')
print('DATA IMPORTED')

print('ENCODING DATA')
# we need to encode with one hot encoder only the values that have not an order
PORT_PREFIX = 'Port_'
cols_to_onehotencode = [col for col in df.columns if col.startswith(PORT_PREFIX)]
cols_to_onehotencode += ['Title']
print('\t     Onehot encoded features', cols_to_onehotencode)
print('\t NOT Onehot encoded features', [col for col in df.columns if col not in cols_to_onehotencode])
encoded_df = pd.get_dummies(df, columns=cols_to_onehotencode)
print('DATA ENCODED')

print('INITILIZING CLUSTERING MODEL')
ID = 'ID'
NUMBER_OF_CLUSTERS = 3
#todo OPTIMIZE HYPERPARAMETERS
#initialize algorithm
clustering_model = KMeans(n_clusters=NUMBER_OF_CLUSTERS, random_state=0)
#fit algorithm
clustering_model.fit(encoded_df.drop([ID], axis=1))
print('INITILIZED CLUSTERING MODEL')

# add cluster labels on the side of the initial df
clustered_df = df.copy()
clustered_df['cluster'] = clustering_model.predict(encoded_df.drop([ID], axis=1))

print('5 RANDOM examples for each cluster')
for cl in range(NUMBER_OF_CLUSTERS):
    print('\t Cluster', cl)
    print(clustered_df[clustered_df['cluster'] == cl])



print('Done, ciao.')


