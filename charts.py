import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('downloads/data-all-theses.csv')

cat_cols=list(df.dtypes[df.dtypes=='object'].index)
# df['Discipline(s)'] = df['Discipline(s)'].str.split('>', n = 1, expand = True)
# df['Language'] = df['Language'].str.split('>', n = 1, expand = True)
# df[df['Discipline(s)']] = df[df['Discipline(s)']][:10]
# for c in cat_cols:
#     print(c)
#     print('========')
#     print(df[c].unique())
#     print()

def pct_more_than_1(pct):
    return ('%1.f%%' % pct) if pct > 1 else ''

df['Language'].value_counts().plot(kind='pie', autopct = pct_more_than_1, labels=None, figsize=(15, 15), title='Language')
plt.legend(df['Language'].value_counts().index.tolist())
plt.savefig('all-majors-langs.png')
print(df['Language'].unique())