# -*- coding: utf-8 -*-
'''
This file is part of PyMbs.

PyMbs is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PyMbs is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public 
License along with PyMbs.
If not, see <http://www.gnu.org/licenses/>.

Copyright 2011, 2012 Carsten Knoll, Christian Schubert, 
                     Jens Frenkel, Sebastian Voigt
'''

'''
Created on 19.07.2009

@author: Christian Schubert
'''
from PyMbs.Input import *



world=MbsSystem([0,-1,0], name="Bar1")

# Parameter
l1=world.addParam('Length 1', 'l1', 0.13)

m2=world.addParam('Mass 2', 'm2', 0.6)
l2=world.addParam('Length 2', 'l2', 0.174)
I2=world.addParam('Inertia 2', 'I2', m2/12*l2**2)

m3a=world.addParam('Mass 3a', 'm3a', 0.25)
l3a=world.addParam('Length 3a', 'l3a', 0.025)
I3a=world.addParam('Inertia 3a', 'I3a', m3a/12*l3a**2)

m3b=world.addParam('Mass 3b', 'm3b', 0.25)
l3b=world.addParam('Length 3b', 'l3b', 0.025)
I3b=world.addParam('Inertia 3b', 'I3b', m3b/12*l3b**2)

# Create Bodies with Coordinate Systems
# Bar1 = Inertial System
bar1_A = world.addFrame(name='CS_A')
bar1_C = world.addFrame(name='CS_C', p=[l1,0,0])

bar2 = world.addBody(name='Bar2', mass=m2, cg=[l2/2,0,0], inertia=diag([0,I2,I2]))
bar2.addFrame(name='CS_A')
bar2.addFrame(name='CS_B', p=[l2,0,0])
bar2.addFrame(name='CS_Graphic', p=[l2/2,0,0])
bar2.addFrame(name='CS_B_Graphic', p=[l2,0,0], R=rotMat(pi/2,'x'))

bar3a = world.addBody(name='Bar3a', mass=m3a, cg=[l3a/2,0,0], inertia=diag([0,I3a,I3a]))
bar3a.addFrame(name='CS_B')
bar3a.addFrame(name='CS_Graphic', p=[-l3a/2,0,0])

bar3b = world.addBody(name='Bar3b', mass=m3b, cg=[l3b/2,0,0], inertia=diag([0,I3b,I3b]))
bar3b.addFrame(name='CS_C')
bar3b.addFrame(name='CS_Graphic', p=[l3b/2,0,0])

# Insert Joints
jA = world.addJoint('jA', world.CS_A, bar2.CS_A, 'Rz', 0.01)
jC = world.addJoint('jC', world.CS_C, bar3b.CS_C, 'Rz')
jCB = world.addJoint('jCB', bar3b.CS_C, bar3a.CS_B, 'Tx')

# Constraint
dae = False
if (dae == True):
    world.addConstraint('Constr_FB', bar2.CS_B, bar3a.CS_B, [1,1,0], [0,0,0])
else:
    world.addLoop.ThreeBarTrans(bar2.CS_B, bar3a.CS_B, name='ThreeBarLinkageTrans')


# Sensors
world.addSensor.Position(world.CS_A, world.CS_A, 'r1_A', world.CS_A, name='r1_A')
world.addSensor.Position(world.CS_A, world.CS_C, 'r1_C', world.CS_A, name='r1_C')

world.addSensor.Position(world.CS_A, bar2.CS_A, 'r2_A', world.CS_A, name='r2_A')
world.addSensor.Position(world.CS_A, bar2.CS_B, 'r2_B', world.CS_A, name='r2_B')

world.addSensor.Position(world.CS_A, bar3a.CS_B, 'r3a_B', world.CS_A, name='r3a_B')
world.addSensor.Position(world.CS_A, bar3b.CS_C, 'r3b_C', world.CS_A, name='r3b_C')

print("System has been assembled")


# Visualisation
world.addVisualisation.Box(bar2.CS_Graphic, 0.174, 0.005, 0.005, name='bar2')
world.addVisualisation.Box(bar3a.CS_Graphic, 0.1, 0.005, 0.005, name='bar3a')
world.addVisualisation.Box(bar3b.CS_Graphic, 0.1, 0.01, 0.01, name='bar3b')
world.addVisualisation.Cylinder(bar2.CS_B_Graphic, 0.005, 0.005, name='bar2_cyl')

print("System has been assembled")

world.genEquations(explicit=True)
world.genCode('m', 'ThreeBarLinkageTrans', '.\Output', debugMode=False)
world.show('ThreeBarLinkageTrans')