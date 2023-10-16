import json
from operator import index
import numpy as np
from decimal import Decimal


arr = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5,'Jun':6,'Jul':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12}

def init():
    print('\nWelcome to CorrR')
    print('Data format is [Jan-1997]\n')

def error(callback, c1, c2):
    if callback == 1:
        print('Data does not include 1915, 1916')
    elif callback == 2:
        print('June-Dec 1914 not included')
    elif callback == 5:
        print('Mar 1917-Aug 1997 not included')
    elif callback == 3:
        print('No adjustment needed')
    elif callback == 6:
        print('FATAL ERROR: Check Algorithm')
        print('Entered date: ', c1)
        print('Computed date based on index: ', c2)
    
    print('**********PROCESS TERMINATED**********\n')
    exit()

def process_post(y, m):
    if y == 1917 and m == 1:
        return 29
    elif y == 1917 and m == 2:
        return 29
    elif y > 1917:
        return 995
    else:
        return error(3)

def datr(date):
    x = date.split("-") #split data at -
    #print(x[0] + ' ' + x[1]) #restate input

    yri = int(x[1]) # Raw values
    mname = x[0]

    month = arr[x[0]] # Convert text month to month code

    if yri == 1915 or yri == 1916: # If a WWI year is selected...
        return error(1, 0, 0)
    elif yri == 1914 and month > 7: # If end of 1914 is selected (also WWI)...
        return error(2, 0, 0)
    elif (1918 <= yri <= 1996) or (yri == 1997 and month < 9) or (yri == 1917 and month > 2): # If selected is between Mar 1917-Aug 1997
        return error(5, 0, 0)

    ind_adjust = 0

    if yri > 1914:
        # process after 1914 data
        ind_adjust = process_post(yri, month)

    year = int(x[1])-1865 # Calulate which year of the index the date is in...

    index = (month-1) + (12*year) - ind_adjust

    if(data[index]['month'] != date):  # Make sure inputed date matches computed date from index ...
        error('6', data[index]['month'], date)

    return int(index)


def change(d1, d2):
    print(d1 + ' ' + d2)
    data[1]['SPSE']

def arr_dist(date1, date2): # Return index for dates
    a = datr(date1)
    b = datr(date2)
    pricel = []
    datel = []
    for x in range(a, b):
        datel.append(data[x]['month'])
        pricel.append(data[x]['SPSE'])
    # or np.array
    return list(pricel) 

def arr_name(date1, date2): # Return list of dates for range of dates
    a = datr(date1)
    b = datr(date2)
    pricel = []
    datel = []
    for x in range(a, b):
        datel.append(data[x]['month'])
        pricel.append(data[x]['SPSE'])
    # or np.array
    return list(date1) 

def euc_dist():

    # August 2019 - December 2020
    a = arr_dist('Aug-2019', 'Dec-2020')
    b = arr_dist('Jan-1865', 'Dec-1913')
    aint = [Decimal(numeric_string) for numeric_string in a] # Convert to decimals

    # Normalize Aug-2019 - Dec-2020
    norm_aint = []
    place = aint[0] # Store first value as it will turn into 100 immediately
    for y in range(15):
        norm_aint.append((aint[y] / place) * 100) # Add new indexed value to new array (cannot append to aint)

    numposs = (len(b) - len(a)) + 1 # Computer number of possiblities for both
    print('historic data set length: ', len(b))
    print("possibilities: ", numposs)
    fullarr = [] # Array of all index numbers required (use number to access stock prices)
    fulldat = [] # Array of arrays of all 16 number selections

    # Run through all possiblities (each loop = one possiblity)
    for x in range(numposs):
        y = (x)

        # Compute index value for each possiblity
        rayarr = [1+y, 2+y, 3+y, 4+y, 5+y, 6+y, 7+y, 8+y, 9+y, 10+y, 11+y, 12+y, 13+y, 14+y, 15+y, 16+y]

        # Turn into values     
        raydat = []
        for z in range(15):
            h = Decimal(data[z+y]['SPSE'])
            raydat.append(h)
        
        fulldat.append(raydat)
        fullarr.append(rayarr)

    diffind = []

    # Normalize and compute eucledian distance for each possiblity
    for x in range(len(fulldat)):
        
        placeholder = fulldat[x][0]

        # Normalize data to 100
        for y in range(15):
            fulldat[x][y] = (fulldat[x][y] / placeholder) * 100

        # Calc euclidean distance
        euclidean_distance = np.linalg.norm(np.array(fulldat[x]) -  np.array(norm_aint))
        #print("Euclidean distance between two time-series is:", euclidean_distance)
        diffind.append(euclidean_distance)

    index_val = diffind.index(min(diffind))

    # Sort Values to find second and 3rd smallest
    s = sorted(diffind, key=float)
    print(s)
    index_val_s1 = diffind.index(s[1])
    index_val_s2 = diffind.index(s[2])

    print('Smallest Eucledian Distance is: ', min(diffind), '(index:', index_val, ') ', 'For ', data[fullarr[index_val][0]]['month'], ' - ', data[fullarr[index_val][15]]['month'])
    print('Second Smallest Eucledian Distance is: ',  s[1], '(index:', index_val_s1, ') ', 'For ', data[fullarr[index_val_s1][0]]['month'], ' - ', data[fullarr[index_val_s1][15]]['month'])
    print('Third Smallest Eucledian Distance is: ',  s[2], '(index:', index_val_s2, ') ', 'For ', data[fullarr[index_val_s2][0]]['month'], ' - ', data[fullarr[index_val_s2][15]]['month'])


with open('C:/Users/will/OneDrive/Desktop/SPSE.json', 'r') as f:
  data = json.load(f)

#d = input('RETRIEVE INDEX FOR DATE ~: ')

#for x in range(901):
#    print(datr[x])


euc_dist()