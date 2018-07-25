"""
   Convex Hull Assignment: COSC262 (2017)
   Student Name: Ahmad Alsaleh
   Usercode: aaa113
   
"""


def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    i = 0
    file = open(filename)
    lines = file.readlines()
    file.close()
    listPts = []
    while i < N:
        place = lines[i]
        place = place.split()
        listPts.append((float(place[0]), float(place[1]))) ; i += 1
 
    return listPts

def isCCW(pointA, pointB, pointC):
    """An 'algorithm' to check for clockwise and anticlockwise turns"""
    return ((pointB[0] - pointA[0]) * (pointC[1] - pointA[1])) - ((pointB[1] - pointA[1]) * (pointC[0] - pointA[0])) > 0

def theta(pointA, pointB):
    """Returns the angle using the theta approximation. For purposes of the giftwrap algorithm. Used in both the grahamscan and giftwrapscan
       """
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.6e-6:
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))
    if t == 0:
        t = 4    
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = t + 4

    return t * 90

def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of 'h' tuples
          [(u0,v0), (u1,v1), ...]    
    """
    i = 0
    v = 0
    listPts.append(listPts[min_point_function(listPts)])  
    k = min_point_function(listPts)
    n = len(listPts) - 1
    nrange = len(listPts)
    
    while k != n:
        listPts[i],listPts[k] = listPts[k],listPts[i] 
        minAngle = 361      
        for j in range(i,nrange):
            angle = theta(listPts[i], listPts[j])  
            if (angle < minAngle and angle > v and listPts[j] != listPts[i]):
                            minAngle = angle;
                            k = j              
            if abs(angle) < 1.e-6:
                angle = 360                 
        i += 1
        v = minAngle
    chull = listPts[:i]  
    return chull

    
def min_point_function(listPts):
    """Returns the minimum point index in points"""
    min_point_function = 0
    i = 0
    nrange = len(listPts)
    while i < nrange:
        if listPts[i][1] == listPts[min_point_function][1]: 
            if listPts[i][0] > listPts[min_point_function][0]: 
                min_point_function = i                       
        elif listPts[i][1] < listPts[min_point_function][1]: 
            min_point_function = i        
        i = i + 1
    return min_point_function


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  
    """
    sort_points = sorted(listPts, key=lambda x: x[1])
    right = sort_points[0]
    degrees_bet = [(0, right)]
    for i in sort_points:
        if i != right:
            degree = theta(i, right)
            degrees_bet.append((degree, i))
    degrees_bet.sort() 
    chull = [degrees_bet[0][1], degrees_bet[1][1], degrees_bet[2][1]] 
    for result in degrees_bet[3:]:
        while isCCW(chull[-2], chull[-1], result[1]) == False:
            chull.pop()
        chull.append(result[1])
    return chull


def amethod(listPts):
    """Returns the convex hull vertices computed using the
         Monotone chain convex hull algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  
    """
    listPts.sort() 
    upper = []
    lower = []
    for i in listPts:
        while len(lower) >= 2 and isCCW(lower[-2], lower[-1], i) == False:
            lower.pop()
        lower.append(i)
    listPts.reverse()
    for p in listPts:
        while len(upper) >= 2 and isCCW(upper[-2], upper[-1], p) == False:
            upper.pop()
        upper.append(p)
    upper.pop() 
    lower.pop() 
    chull = lower + upper
    #Same values but gives different order
    return chull
    
def main():
    #listPts = readDataPts('Set_A.dat', 1000) 
    listPts = readDataPts('A_3000.dat', 3000) 
    #listPts = readDataPts('Set_A.dat', 500)  #File name, numPts given as example only
    #listPts = readDataPts('Set_A.dat', 50) 
    print(giftwrap(listPts))      #You may replace these three print statements
    print (grahamscan(listPts))   #with any code for validating your outputs
    print (amethod(listPts))     
 
if __name__  ==  "__main__":
    main()
    


  