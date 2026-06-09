# Creating a KMeans clustering algorithm in python
# NOTE: Most of this comes from a tutorial on the LMS

import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

column_names = [
    'sepal_length',
    'sepal_width',
    'petal_length',
    'petal_width',
    'species'
]

df = pd.read_csv('iris.csv', header=None, names=column_names)
# print(df.head())

# print(df.value_counts("species"))
assert df.shape == (150,5)

x = df[column_names[:-1]]
y = df["species"]

## Produce a pair plot
# sns.pairplot(df, hue='species', diag_kind='kde')
# plt.suptitle('Iris Dataset — True Species Labels', y=1.02)
# plt.tight_layout()
# plt.show()

## Build and run the kmeans model 
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(x)
# print(kmeans.cluster_centers_)

centres_df = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=x.columns,
    index=['Cluster 0', 'Cluster 1', 'Cluster 2']
).round(3)

# print("Final cluster centres (cm):")
# print(centres_df)
# print("\nCluster sizes:")
# print(pd.Series(kmeans.labels_).value_counts().sort_index())

contingency = pd.crosstab(df['species'], kmeans.labels_)
incorrect_assignments = 0
print("Dominant species for each cluster:")
for idx, series in contingency.iterrows():
    print(f"{idx}: {numpy.max(series)}")

    for elem in series.to_numpy():
        if elem > 0 and elem != numpy.max(series):
            incorrect_assignments += elem

print(f"Incorrect assignment: {incorrect_assignments / 150}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
sns.scatterplot(data=df, x='petal_width', y='petal_length', hue='species', ax=ax1).set_title('True Species')
sns.scatterplot(data=df, x='petal_width', y='petal_length', hue=kmeans.labels_, ax=ax2).set_title('K-Means Clusters')
plt.tight_layout()
plt.show()

