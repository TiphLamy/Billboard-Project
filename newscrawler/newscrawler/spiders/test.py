import pandas as pd
import matplotlib.pyplot as plt
scrap = pd.read_json("scrap200.json")
# a = ""
#
# for i in scrap["artist"]:
#     a = a+i+"\n"
# print(a)
#print(scrap["artist"].duplicated())
#print(scrap['artist'].values_count())
artist = scrap.groupby('artist').size()
plt.hist(x=artist, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
