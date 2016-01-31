import pandas as pd
import os.path
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import heapq




#Read in csv into dataframe
df = pd.read_csv(os.path.normpath("C:/Data/Jail_Bookings_-_May_29__2015_to_current.csv"))

print(df.columns.values.tolist()) # put the each of the columns into an array of a multi-dimensional array
#d = df.DOB
#d = [str(x).split("/")[2] for x in d if str(x) != 'nan']
#print(d[1])

charges = list( df.Charge1 )

d = dict()
ageGroups = dict()

for i in range(len(charges)):
    if(charges[i] in d):
        d[charges[i]]+=1
    else:
        d[charges[i]] = 1
    #print(charges[i])


hist = list( zip(d.values(), d.keys())  )
hist = [x for x in hist if str(x[1]) != 'nan']
topTen = heapq.nlargest(10, hist)
print(topTen)






N = 10
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

#ind is the x coordinates of the left sides of the bars
#second is a list containing all values of bars
#third is just color
p1 = plt.bar(ind, [x[0] for x in topTen] , width, color='r')

#label of y axis

plt.ylabel('# of Arrests')

#title of graph
plt.title('Top 10 Causes for Arrest in Miami')

#distance between markers of x-axis
#second argument are x labels for each marker
plt.xticks(ind + .35, [str(x[1])[:12] for x in topTen])

plt.show()

