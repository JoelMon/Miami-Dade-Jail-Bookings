import pandas as pd
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import heapq





#Read in csv into dataframe
df = pd.read_csv(os.path.normpath("C:/Data/Jail_Bookings_-_May_29__2015_to_current.csv"))

#print(df.columns.values.tolist()) # put the each of the columns into an array of a multi-dimensional array


# I'm placing all the relevant fields, into a simplified list of tuples
records = list( zip(df.Charge1,df.BookDate,df.DOB) ) 

'''I'm initializing the dictionaries for chargeCount and ageGroups'''

chargeCount = dict() #Later in the code, chargeCount is essentially going to initialize
# a charge (which is a string in the records tuples) to 1, and it's going to raise that number
#every time another tuple in records of the same charge is encountered, effectively counting arrests per charge

ageGroups = dict() # Think of this as a two dimensional array, with first index being age, the second index
#being charges, and the value being the number of people in that age bracket who commited that charge
'''==============================================================='''



'''Count total number jailed by charge and number jailed by age AND charge'''
for i in range(len(records)):

    #Think of this if statement as just checking whether there's a valid date or not, and skipping
    #an entry if it's not, with 'continue'
    if( len(str(records[i][1]).split("/")) < 3 or len(str(records[i][2]).split("/")) < 3):
        continue
    #Get's the year arrested by formatting the string in 'mm/dd/yyyy' format, to just get the 3rd thing after the '/'
    yearArrested = int(str(records[i][1]).split("/")[2]) 
    #Similar to above
    yearBorn = int(str(records[i][2]).split("/")[2]) 
    #The age is the age at the time of arrest
    age = str(yearArrested - yearBorn)
    if(records[i][0] in chargeCount):  #If the charge has been counted at least once already
        chargeCount[records[i][0]]+=1 #Add one to the existing count
    else:
        chargeCount[records[i][0]] = 1 #Otherwise count it for the first time

    if( age in ageGroups): #if an entry of that age is in the dictionary
        if(records[i][0] in ageGroups[age]): #If an entry for that crime for that age is made (counted at least once)
            ageGroups[age][records[i][0]]+=1 #Add to count
        else:
            ageGroups[age][records[i][0]]=1 #Otherwise, since the age has been created,
            #Create the charge index and count for the first time
    else: #Otherwise, if an age index has been created
       ageGroups[age] = dict() #Create the age index
       ageGroups[age][records[i][0]]=1 #And start the charge count
'''======================================================================='''


ages = ageGroups.keys() #Gets list of all ages found in dataset

chargeCountReverse = list( zip(chargeCount.values(), chargeCount.keys())  ) #Reversing the order of (key,value) to (value,key)
#And placing it into a list to make it easiert ot sort

chargeCountReverse = [x for x in chargeCountReverse if str(x[1]) != 'nan'] #Making sure I'm removing any input without a charge (it would all map into index 'nan')
topTen = heapq.nlargest(10, chargeCountReverse) #Using a heapify algorithm to get the 10 laegest charges by arrest number


'''This part is where I actually plot the points on a scatter plot'''
for age in ages:
    for i in range (len(topTen)): #For all the charges in the topTen 
        if topTen[i][1] in ageGroups[age] : #If the charge exists in the age bracker
            numArrested = ageGroups[age][topTen[i][1]] #Get the exact number of people in age bracket charged
            if(i%2 == 0):
                i += 2
            plt.scatter(age, numArrested, s=75, c=cm.rainbow(i/10) , alpha=1,lw =0) #And graph with a scatter plot(plt.scatter)
            #Here I'm plotting single points, using age as an x coordinate, numArrested as the y coordinate,and s being a scale for width
            #The c is to specify a color, and since I wanted every crime to have a distinct color, I just took the index of the top ten,
            #divided it by 10 and placed it into the method cm.rainbow which takes in a value between 0 and 1 and maps it to an actual color
            #Also, the alpha value is a transparency level from 0 to 1 (.1 being barely visible and 1 being normal)
            #FOR UNLISTED CHARGES: change above alpha to .1
    if np.nan in ageGroups[age]: #The unlisted charges
        numArrested = ageGroups[age][np.nan]
        plt.scatter(age, numArrested, s=75, c='black',alpha=0 )
        #FOR UNLISTED CHARGES: change above alpha to .9

'''==============================================================='''


x = cm.rainbow([i/10 for i in np.arange(1,10)])
legendValues = []
for i in range(len(topTen)):
    g = i
    if(g%2 == 0):
                g += 2
    legendValues.append( mpatches.Patch(color=cm.rainbow(g/10), label=topTen[i][1], alpha=1) )

    
plt.legend(handles=legendValues,title="Charges by Color")

#Label y axis
plt.ylabel('Number of Arrests')

#Label x axis
plt.xlabel('Age')

#Title of graph
plt.title('Jail Bookings of Miami-Dade by Age and Charge')



plt.show()

