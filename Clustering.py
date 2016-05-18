
#File:    Clustering.py
#Author:  Matthew Wheeler
#Date:    05/17/2016
#Section: 02
#E-mail:  mwheel1@umbc.edu
#Description: A python program that preforms K-means
# clustering on an input file of nodes and graphs results

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

COLOR_MAP = ['b','g','r','c','m','y','k','w']
INPUT_ARGS = 3

def main():
    if (len(sys.argv) != INPUT_ARGS):
        print("Invalid number of Arguments. Check Syntax.")
        print("Syntax: Clustering.py <# of clusters> <input file>")
        print("Where <# of cluters> = number of clusters")
        print("      <input file> = File with 2D points")
        print("Exiting...")
        exit()
    else:
        print("Executing Program...")
        s = 'Opening stream to file ' + str(sys.argv[2]) + '...'
        print(s)
        try:
            inputFile = open(str(sys.argv[2]), 'r')
            print("File stream opened sucessfully.")
        except IOError:
            s = 'Could not find the specified file: ' + inputFile
            print(s)
            print("Make sure the file exists and is readable then try again.")
            print("Exiting...")
            exit()
        print("Reading nodes from file stream...")
        Nodes = []
        Centers = []
        xMin = float("inf")
        xMax = float("-inf")
        yMin = float("inf")
        yMax = float("-inf")
        for line in inputFile:
            args = line.split()
            X = float(args[0])
            Y = float(args[1])
            if X < xMin:
                xMin = X
            if X > xMax:
                xMax = X
            if Y < yMin:
                yMin = Y
            if Y > yMax:
                yMax = Y
            Nodes.append([(X,Y),None,None])
        print("Nodes imported sucessfully.")
        print("Closing file stream...")
        inputFile.close()
        print("File stream closed.")
        print("Generating "+str(sys.argv[1])+" centers...")
        for center in range(int(sys.argv[1])):
            XY = Nodes[random.randint(0,len(Nodes)-1)][0]
            color = COLOR_MAP[center%8]
            Centers.append([XY,color])
        print("Centers generated successfully.")
        print("Computing K-Means clustering with "+str(sys.argv[1])+" centers...")
        change = True
        while (change):
            change = False
            for node in Nodes:
                nodeX = node[0][0]
                nodeY = node[0][1]
                oldCenter = node[1]
                bestCenter = 0
                bestDist = float("inf")
                c = 0
                for center in Centers:
                    centerX = center[0][0]
                    centerY = center[0][1]
                    tempDist = math.sqrt(((nodeX-centerX)**2)+((nodeY-centerY)**2))
                    if (tempDist < bestDist):
                        bestDist = tempDist
                        bestCenter = c
                    c += 1
                if ((oldCenter != bestCenter) or (oldCenter == None)):
                    node[1] = bestCenter
                    node[2] = COLOR_MAP[(bestCenter%8)]
                    change = True
            if (change == True):
                total = [0] * len(Centers)
                sumX = [0] * len(Centers)
                sumY = [0] * len(Centers)
                for node in Nodes:
                    total[node[1]] += 1
                    sumX[node[1]] += node[0][0]
                    sumY[node[1]] += node[0][1]
                c = 0
                for center in Centers:
                    if (total[c] != 0):
                        centerX = sumX[c]/total[c]
                        centerY = sumY[c]/total[c]
                        center[0] = (centerX, centerY)
                        c += 1
        print("Cluster centers computed sucessfully.")
        print("Displaying results...")
        for node in Nodes:
            plt.scatter(node[0][0],node[0][1],s=40,marker='.',color=node[2])
        for center in Centers:
            plt.scatter(center[0][0],center[0][1],s=100,marker='*',color=center[1])
        axes = plt.gca()
        axes.set_xlim([(xMin-1),(xMax+1)])
        axes.set_ylim([(yMin-1),(yMax+1)])
        plt.show()
        print("Done.")
main()
