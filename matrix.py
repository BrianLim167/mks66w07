import math
from vector import *

class Matrix(object):

    #m1 * m2 -> m2
    @staticmethod
    def mult( m1, m2 ):
        m = Matrix(0, m1.rows)
        for c in range( m2.cols ):
            m.append([])
            for r in range( m1.rows ):
                m[-1].append( 0 )
                for i in range(m1.cols):
                    m[c][r] += (m1[i][r] * m2[c][i])
        return m

    @staticmethod
    def ident(s=4):
        m = Matrix(s,s)
        for c in range( m.cols ):
            m[c][c] = 1
        return m

    @staticmethod
    def mover(x,y,z):
        m = Matrix.ident(4)
        m[3][0] = x
        m[3][1] = y
        m[3][2] = z
        return m

    @staticmethod
    def scaler(x,y,z):
        m = Matrix.ident(4)
        m[0][0] = x
        m[1][1] = y
        m[2][2] = z
        return m

    @staticmethod
    def rotx(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[1][1] = math.cos(a)
        m[1][2] = math.sin(a)
        m[2][1] = -math.sin(a)
        m[2][2] = math.cos(a)
        return m
    
    @staticmethod
    def roty(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[2][2] = math.cos(a)
        m[2][0] = math.sin(a)
        m[0][2] = -math.sin(a)
        m[0][0] = math.cos(a)
        return m
    
    @staticmethod
    def rotz(a):
        m = Matrix.ident(4)
        a = math.radians(a)
        m[0][0] = math.cos(a)
        m[0][1] = math.sin(a)
        m[1][0] = -math.sin(a)
        m[1][1] = math.cos(a)
        return m

    @staticmethod
    def bezier():
        m = Matrix(4,4)
        m[0] = [-1, 3,-3, 1]
        m[1] = [ 3,-6, 3, 0]
        m[2] = [-3, 3, 0, 0]
        m[3] = [ 1, 0, 0, 0]
        return m

    @staticmethod
    def hermite():
        m = Matrix(4,4)
        m[0] = [ 2,-3, 0, 1]
        m[1] = [-2, 3, 0, 0]
        m[2] = [ 1,-2, 1, 0]
        m[3] = [ 1,-1, 0, 0]
        return m
    
    def __init__(self, cols = 4, rows = 4):
        if ( isinstance(cols, list) ):
            self.ary = cols
            self.cols = len(cols)
            self.rows = len(cols[0])
            return
        self.ary = []
        self.rows = rows
        self.cols = 0
        for c in range( cols ):
            self.append( [] )
            for r in range( rows ):
                self[c].append( 0 )

    def copy(self):
        m = Matrix(self.cols,self.rows)
        for c in range( self.cols ):
            for r in range( self.rows ):
                m[c][r] = self[c][r]
        return m

    def __mul__(self, other):
        if ( isinstance(other, Matrix) ):
            return Matrix.mult(self,other)
        m = self.copy()
        for c in range( self.cols ):
            for r in range( self.rows ):
                m[c][r] *= other
        return m

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self = other * self
        return self

    def __neg__(self):
        return -1 * self

    def __getitem__(self, i):
        return self.ary[i]

    def __setitem__(self, i, val):
        self.ary[i] = val
        return self.ary[i]

    def __len__(self):
        return len(self.ary)

    def __str__(self):
        s = ""
        for r in range(self.rows):
            for c in range(self.cols):
                s += ("     "+str(self[c][r]))[:10][-5:]
                s += ' '
            s += '\n'
        return s

    def append(self, val):
        if ( isinstance(val, list) ):
            self.ary.append(val)
            self.cols += 1
            return
        if ( isinstance(val, Matrix) ):
            for c in range(val.cols):
                self.append(val[c])
            return

    def print( self ):
        print(self)

    def add_polygon( self, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
        self.add_point(x0,y0,z0)
        self.add_point(x1,y1,z1)
        self.add_point(x2,y2,z2)

    def add_edge( self, x0, y0, z0, x1, y1, z1 ):
        self.add_point(x0,y0,z0)
        self.add_point(x1,y1,z1)

    def add_point( self, x, y, z=0 ):
        self.append([x,y,z,1])

    def add_circle( self, cx, cy, cz, r, edge=True, count=1000 ):
        step = 1/count
        t = 0
        m = Matrix(0,4)
        while ( t < 1 ):
            a = math.radians(360*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            a = math.radians(360*(t+step))
            if ( edge ):
                m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            t += step
        if ( not edge ):
            a = math.radians(360*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
        self.append(m)
        
    def add_semicircle( self, cx, cy, cz, r, edge=True, count=1000 ):
        step = 1/count
        t = 0
        m = Matrix(0,4)
        while ( t < 1 ):
            a = math.radians(180*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            if ( edge ):
                a = math.radians(180*(t+step))
                m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
            t += step
        if ( not edge ):
            a = math.radians(180*t)
            m.add_point(cx + r*math.cos(a), cy + r*math.sin(a), cz)
        m *= Matrix.rotz(270)
        self.append(m)

    def add_curve( self, x0, y0, x1, y1, x2, y2, x3, y3, count, curve_type ):
        step = 1/count
        if ( curve_type.lower() == "bezier" ):
            curve_type = Matrix.bezier
        elif ( curve_type.lower() == "hermite" ):
            curve_type = Matrix.hermite
        x_coeff = curve_type() * Matrix([[x0,x1,x2,x3]])
        y_coeff = curve_type() * Matrix([[y0,y1,y2,y3]])
        t = 0
        m = Matrix(0,4)
        while ( t <= 1 ):
            x = x_coeff[0][0]*t**3 + x_coeff[0][1]*t**2 + x_coeff[0][2]*t + x_coeff[0][3]
            y = y_coeff[0][0]*t**3 + y_coeff[0][1]*t**2 + y_coeff[0][2]*t + y_coeff[0][3]
            m.add_point(x,y,0)
            x = x_coeff[0][0]*(t+step)**3 + x_coeff[0][1]*(t+step)**2 + x_coeff[0][2]*(t+step) + x_coeff[0][3]
            y = y_coeff[0][0]*(t+step)**3 + y_coeff[0][1]*(t+step)**2 + y_coeff[0][2]*(t+step) + y_coeff[0][3]
            m.add_point(x,y,0)
            t += step
        self.append(m)

    def add_box( self, x, y, z, width, height, depth ):
        x, y, z, a, b, c = x, y-height, z-depth, x+width, y, z

        self.add_point(x,y,z)
        self.add_point(a,b,z)
        self.add_point(a,y,z)

        self.add_point(a,b,z)
        self.add_point(x,y,z)
        self.add_point(x,b,z)


        self.add_point(x,y,c)
        self.add_point(a,y,c)
        self.add_point(x,b,c)

        self.add_point(x,b,c)
        self.add_point(a,y,c)
        self.add_point(a,b,c)


        self.add_point(x,y,z)
        self.add_point(a,y,z)
        self.add_point(x,y,c)

        self.add_point(x,y,c)
        self.add_point(a,y,z)
        self.add_point(a,y,c)


        self.add_point(x,b,z)
        self.add_point(a,b,c)
        self.add_point(a,b,z)

        self.add_point(a,b,c)
        self.add_point(x,b,z)
        self.add_point(x,b,c)


        self.add_point(a,b,z)
        self.add_point(a,b,c)
        self.add_point(a,y,z)
        
        self.add_point(a,b,c)
        self.add_point(a,y,c)
        self.add_point(a,y,z)

        
        self.add_point(x,y,z)
        self.add_point(x,y,c)
        self.add_point(x,b,z)
        
        self.add_point(x,y,c)
        self.add_point(x,b,c)
        self.add_point(x,b,z)

    def add_sphere( self, cx, cy, cz, r, poly=True, count=14 ):
        m = Matrix.sphere(cx,cy,cz, r, poly, count)
        self.append(m)

    @staticmethod
    def sphere( cx, cy, cz, r, poly=True, count=10 ):
        step = 1/count
        m = Matrix(0,4)
        t = 0
        rot = Matrix.roty(360 * step)
        rotb = Matrix.roty(-360 * step)
        while ( t < 1 ):
            if ( poly ):
                a,b,c = Matrix(0,4),Matrix(0,4),Matrix(0,4)
                a.add_semicircle(0,0,0, r, False, count)
                b.add_semicircle(0,0,0, r, False, count)
                c.add_semicircle(0,0,0, r, False, count)
                b *= rot
                c *= rotb
                for i in range(count):
                    m.append(a[i])
                    m.append(a[(i+1)%len(a)])
                    m.append(b[i])
                    
                    m.append(a[i])
                    m.append(c[(i+1)%len(c)])
                    m.append(a[(i+1)%len(a)])
            else:
                m.add_semicircle(0,0,0, r, True, count)
            m *= rot
            t += step
        m *= Matrix.mover(cx, cy, cz)
        return m

    def add_torus( self, cx, cy, cz, r, poly=True, count=10 ):
        m = Matrix.torus(cx,cy,cz, r, poly, count)
        self.append(m)

    @staticmethod
    def torus( cx, cy, cz, r0, r1, poly=True, count=10 ):
        step = 1/count
        m = Matrix(0,4)
        t = 0
        rot = Matrix.roty(360 * step)
        rotb = Matrix.roty(-360 * step)
        while ( t < 1 ):
            if ( poly ):
                a,b,c = Matrix(0,4),Matrix(0,4),Matrix(0,4)
                a.add_circle(r1,0,0, r0, False, count)
                b.add_circle(r1,0,0, r0, False, count)
                c.add_circle(r1,0,0, r0, False, count)
                b *= rot
                c *= rotb
                for i in range(count):
                    m.append(a[i])
                    m.append(a[(i+1)%len(a)])
                    m.append(b[i])
                    
                    m.append(a[i])
                    m.append(c[(i+1)%len(c)])
                    m.append(a[(i+1)%len(a)])
            else:
                m.add_circle(r1,0,0, r0, False, count)
            m *= rot
            t += step
        m *= Matrix.rotx(90)
        m *= Matrix.mover(cx, cy, cz)
        return m

    def backface_cull(self):
        m = Matrix(0,self.rows)
        for c in range(self.cols//3):
            for r in range(self.rows):
                v0 = Vector(self[c*3+1]) - Vector(self[c*3])
                v1 = Vector(self[c*3+2]) - Vector(self[c*3])
                if ( Vector.cross(v0,v1)[2] >= 0 ):
                    m.append(self[c*3])
                    m.append(self[c*3+1])
                    m.append(self[c*3+2])
        return m
                
            
        
