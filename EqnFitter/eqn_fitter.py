# -*- coding: utf-8 -*-

"""
Code written by Darren Vawter
(14OCT20-current)

Github link:
"""

"""
user specifies spatial dimensions
	[1,2,3] --> [x,x&y,x&y&z]
	-start with just x&y
user enters # of adjustment parameters
	[1,2,3,4,...,21,22,23] --> [a,b,c,d,...,t,u,v]
	-determine max # parameters for reasonable performance?
	-warn users about low time efficiency with many parameters
user enters equation
	-parse equation & verify that no illegal dimensions or parameters were used
user enters type of error to minimize
	[min/max/mean/median/mode (x,y,z,xy,xz,yz,xyz)delta raws/squares/quartics]
user enters list of points
	-parse list of points
	-verify that list of points 
begin processing algorithm
"""

