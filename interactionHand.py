#!/usr/bin/python2.4
# demo for interactive object motion
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
from mouseInteractor import MouseInteractor

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Fehler: PyOpenGL nicht intalliert !!'''
  sys.exit(  )


def display(  ):
    """Glut display function."""
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity( )
    xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
    gluPerspective(30, float(xSize) / float(ySize), 0.1, 50)

    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity( )
    glTranslatef( 0, 0, -4 )
    #global mouseInteractor
    mouseInteractor.applyTransformation( )
    glCallList( tkList )
    #glDisable( GL_LIGHTING )
    #glColor3f( 1, 1, 0.3 )
    #glRasterPos3f( 1.8, .5, 0 )
    #for c in "tip":
    #q  glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )
    #glEnable( GL_LIGHTING )

    drawHandFunc( )
    
    glutSwapBuffers( )

def init(  ):
    """Glut init function."""
    glClearColor ( 0, 0, 0, 0 )
    glEnable( GL_DEPTH_TEST )
    glShadeModel( GL_SMOOTH )
    glEnable( GL_LIGHTING )
    glEnable( GL_LIGHT0 )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, 0 )
    glLightfv( GL_LIGHT0, GL_POSITION, [4, 4, 4, 1] )
    lA = 0.8
    glLightfv( GL_LIGHT0, GL_AMBIENT, [lA, lA, lA, 1] )
    lD = 1
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
    lS = 1
    glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
    glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.2, 1] )
    glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.7, 1] )
    glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
    glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
    global mouseInteractor
    mouseInteractor = MouseInteractor( .01, 1 )
    global tkList
    tkList = glGenLists( 1 )
    glNewList( tkList, GL_COMPILE )

    global thumb_angle
    global index_angle
    global middle_angle
    global ring_angle
    global little_angle

    thumb_angle = [70,50]
    index_angle = [0,0,0]
    middle_angle = [20,0,0]
    ring_angle = [70,90,90]
    little_angle = [70,90,90]
    #glutSolidTeapot( 1.0 )
    drawHandFunc()
    glEndList( )



def createSphere():
    #glTranslatef(sphere_position[0],sphere_position[1],sphere_position[2])
    glutSolidSphere(0.05,32,32)
   

def drawBone(lengthOfBone,Rangle,Rx,Ry,Rz):
    glPushMatrix()
    glRotatef(Rangle,Rx,Ry,Rz)
    quadric = gluNewQuadric()
    gluCylinder(quadric,0.03,0.03,lengthOfBone,100,10)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def connectJoint(lengthOfBone):
    glPushMatrix()
    quadric = gluNewQuadric()
    gluCylinder(quadric,0.03,0.03,lengthOfBone,100,10)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def drawFinger_2(origiral_ang, ang_len_tuples):
    glPushMatrix()

    glRotatef(*origiral_ang)

    for ang, leng in ang_len_tuples:
        glRotatef(ang, 1, 0, 0)
        connectJoint(leng)
        glTranslatef(0.0, 0.0, leng)
        createSphere()

    glPopMatrix()  

def drawFinger(origiral_ang,proximal_len, distal_len, intermediate_len, distal_ang=0, intermediate_ang=0, proximal_ang=0):
    glPushMatrix()
    glRotatef(origiral_ang[0],origiral_ang[1],origiral_ang[2],origiral_ang[3])
    glRotatef(proximal_ang,1,0,0)
    connectJoint(proximal_len)
    glTranslatef(0.0,0.0,proximal_len)
    createSphere()
    glRotatef(intermediate_ang,1,0,0)
    connectJoint(intermediate_len)
    glTranslatef(0.0,0.0,intermediate_len)
    createSphere()
    glRotatef(distal_ang,1,0,0)
    connectJoint(distal_len)
    glTranslatef(0.0,0.0,distal_len)
    createSphere()
    glPopMatrix()

def drawThumb(distal_len, intermediate_len, distal_ang=0, intermediate_ang=0):
    glPushMatrix()
    glRotatef(-90,0,1,0)
    glRotatef(intermediate_ang,0,1,0)
    glRotatef(45,-1,0,0)
   
    connectJoint(intermediate_len)
    glTranslatef(0.0,0.0,intermediate_len)
    createSphere()
    glRotatef(distal_ang,0,1,0)
    connectJoint(distal_len)
    glTranslatef(0.0,0.0,distal_len)
    createSphere()
    glPopMatrix()

def drawHandFunc():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glRotatef(1,0,1,0)
    
    glPushMatrix()
    glTranslatef(-0.05,-0.4,0.8)
    
    drawBone(0.5,90,-1,0,0)
    
    
    
    #draw thumb
    thumb_position = [90,-1,-1,0]
    proximal_len=0.2
    intermediate_len = 0.2
    distal_len=0.12
    drawThumb(distal_len=0.22,intermediate_len=0.3,intermediate_ang=thumb_angle[0],distal_ang=thumb_angle[1])
    #drawBone(0.52,90,-1,-1,0)
    


    glTranslatef(0.0,0.5,0.0)
    createSphere()

    #draw index finger
    #drawBone(0.6,90,-1,-0.1,0)
    index_position = [90,-1,-0.1,0]
    drawFinger(distal_len=0.2,origiral_ang=index_position,proximal_len=0.2,intermediate_len=0.2,proximal_ang=index_angle[0], intermediate_ang=index_angle[1],distal_ang=index_angle[2])
    


    drawBone(0.2,90,0,1,0)
    glTranslatef(0.2,0.0,0.0)
    createSphere()
    
    #draw middle finger
    #drawBone(0.7,10,1,0,0)
    middle_position = [90,-1,0,0]
    drawFinger(distal_len=0.2,origiral_ang=middle_position,proximal_len=0.3,intermediate_len=0.2,proximal_ang=middle_angle[0], intermediate_ang=middle_angle[1],distal_ang=middle_angle[2])
    


    drawBone(0.2,90,0,1,0)
    glTranslatef(0.2,0.0,0.0)
    createSphere()

    #draw ring finger
    #drawBone(0.62,90,-1,0,0)
    ring_position = [90,-1,0,0]
    drawFinger(distal_len=0.17,origiral_ang=ring_position,proximal_len=0.25,intermediate_len=0.2,proximal_ang=ring_angle[0], intermediate_ang=ring_angle[1],distal_ang=ring_angle[2])
    
    drawBone(0.2,90,0,1,0)
    glTranslatef(0.2,0.0,0.0)
    createSphere()
    
    #draw little finger
    #drawBone(0.45,90,-1,0.1,0)
    little_position = [90,-1,0.1,0]
    drawFinger(distal_len=0.15,origiral_ang=little_position,proximal_len=0.15,intermediate_len=0.15,proximal_ang=little_angle[0], intermediate_ang=little_angle[1],distal_ang=little_angle[2])
   

    
    drawBone(0.5,90,1,0,0)

    glTranslatef(0.0,-0.5,0.0)
    createSphere()

    
    drawBone(0.6,270,0,1,0)

    glTranslatef(-0.6,0.0,0.0)
    createSphere()

    glPopMatrix()
    
    glFlush()

def reshape(w, h):
   glViewport(0, 0, w, h)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if (w <= h):
      glOrtho(0.0, 16.0, 0.0, 16.0*h/w, -10.0, 10.0)
   else:
      glOrtho(0.0, 16.0*w/h, 0.0, 16.0, -10.0, 10.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   #glPostRedisplay()


glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
glutInitWindowSize( 1500, 1500 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( 'Sense It' )
glutReshapeFunc(reshape)
init(  )
mouseInteractor.registerCallbacks( )
glutDisplayFunc( display )
while True:
    line = raw_input()

    if not line:
        break

    joint_angle_data = map(float, line.split())

    thumb_angle = [joint_angle_data[0],joint_angle_data[1]]
    index_angle = [joint_angle_data[2],joint_angle_data[3],joint_angle_data[4]]
    middle_angle = [joint_angle_data[5],joint_angle_data[6],joint_angle_data[7]]
    ring_angle = [joint_angle_data[8],joint_angle_data[9],joint_angle_data[10]]
    little_angle = [joint_angle_data[11],joint_angle_data[12],joint_angle_data[13]]

    glutPostRedisplay( )
    print thumb_angle
    print len(joint_angle_data)
glutMainLoop(  )


