import pandas as pd
df = pd.read_csv("../data/worldcities.csv")
df[df["country"]=='Belgium'][['city','lat','lng']].to_csv('../data/belgium_cities.csv')