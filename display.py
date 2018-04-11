from subprocess import Popen, PIPE
from os import remove
from matrix import *

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

class PPMGrid(object):

    ############################################################################
    # original sauce
    ############################################################################

    #constants
    XRES = 500
    YRES = 500
    MAX_COLOR = 255
    RED = 0
    GREEN = 1
    BLUE = 2

    DEFAULT_COLOR = [0, 0, 0]

    def __init__( self, width = XRES, height = YRES ):
        self.screen = []
        self.width = width
        self.height = height
        for y in range( height ):
            row = []
            self.screen.append( row )
            for x in range( width ):
                self[y].append( PPMGrid.DEFAULT_COLOR[:] )

    def __getitem__(self, i):
        return self.screen[i]

    def __setitem__(self, i, val):
        self.screen[i] = val
        return self.screen[i]

    def __len__(self):
        return len(self.screen)

    def __str__(self):
        ppm = 'P3\n' + str(len(self[0])) +' '+ str(len(self)) +' '+ str(PPMGrid.MAX_COLOR) +'\n'
        for y in range( len(self) ):
            row = ''
            for x in range( len(self[y]) ):
                pixel = self[y][x]
                row+= str( pixel[ PPMGrid.RED ] ) + ' '
                row+= str( pixel[ PPMGrid.GREEN ] ) + ' '
                row+= str( pixel[ PPMGrid.BLUE ] ) + ' '
            ppm+= row + '\n'
        return ppm

    def plot( self, color, x, y ):
        (x,y) = (int(x),int(y))
        newy = PPMGrid.YRES - 1 - y
        if ( x >= 0 and x < PPMGrid.XRES and newy >= 0 and newy < PPMGrid.YRES ):
            self[newy][x] = color[:]

    def clear( self ):
        for y in range( len(self) ):
            for x in range( len(self[y]) ):
                self[y][x] = PPMGrid.DEFAULT_COLOR[:]

    def save_ppm( self, fname ):
        f = open( fname, 'w' )
        f.write( str(self) )
        f.close()

    def save_extension( self, fname ):
        ppm_name = fname[:fname.find('.')] + '.ppm'
        self.save_ppm( ppm_name )
        p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)

    def display( self ):
        ppm_name = 'pic.ppm'
        self.save_ppm( ppm_name )
        p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
        p.communicate()
        remove(ppm_name)

    ############################################################################
    # line
    ############################################################################

    def draw_line( self, x0, y0, x1, y1, color ):
        if ( x1 < x0 ):
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)
        a = y1 - y0
        b = x0 - x1
        (x,y) = (x0,y0)
        if ( 0 <= a <= -b ): # oct 1
            d = 2*a + b
            while ( x <= x1 ):
                self.plot( color, x, y)
                if ( d > 0 ):
                    y += 1
                    d += 2*b
                x += 1
                d += 2*a
            return
        if ( -b <= a ): # oct 2
            d = a + 2*b
            while ( y <= y1 ):
                self.plot( color, x, y)
                if ( d < 0 ):
                    x += 1
                    d += 2*a
                y += 1
                d += 2*b
            return
        if ( b <= a <= 0 ): # oct 8
            d = 2*a - b
            while ( x <= x1 ):
                self.plot( color, x, y)
                if ( d < 0 ):
                    y -= 1
                    d -= 2*b
                x += 1
                d += 2*a
            return
        if ( a <= b ): # oct 7
            d = a - 2*b
            while ( y >= y1 ):
                self.plot( color, x, y)
                if ( d > 0 ):
                    x += 1
                    d += 2*a
                y -= 1
                d -= 2*b
            return

    ############################################################################
    # matrix
    ############################################################################

    def draw_lines( self, matrix, color ):
        for c in range(matrix.cols//2):
            self.draw_line( *matrix[c*2][:2], *matrix[c*2+1][:2], color )

    ############################################################################
    # matrix
    ############################################################################

    def draw_polygons( self, matrix, color, backface_culling=True ):
        if ( backface_culling ):
            matrix = matrix.backface_cull()
        for c in range(matrix.cols//3):
            self.draw_line( *matrix[c*3][:2], *matrix[c*3+1][:2], color )
            self.draw_line( *matrix[c*3+1][:2], *matrix[c*3+2][:2], color )
            self.draw_line( *matrix[c*3+2][:2], *matrix[c*3][:2], color )


    ############################################################################
    # transform
    # curves
    # 3d
    ############################################################################
    def parse_file( self, fname, color ):
        fopen = open(fname,'r')
        fread = fopen.read()
        fopen.close()

        t = Matrix.ident()
        e = Matrix(0,4)
        p = Matrix(0,4)

        cmd = fread.split('\n')
        for i in range(len(cmd)):
            if ( i != len(cmd)-1 ):
                args = cmd[i+1].split()
                for j in range(len(args)):
                    if ( is_number(args[j]) ):
                        args[j] = float(args[j])
            if ( cmd[i] == "line" ):
                e.add_edge(*args)
            elif ( cmd[i] == "ident" ):
                t = Matrix.ident()
            elif ( cmd[i] == "scale" ):
                t *= Matrix.scaler(*args)
            elif ( cmd[i] == "move" ):
                t *= Matrix.mover(*args)
            elif ( cmd[i] == "rotate" ):
                if ( args[0] == 'x' ):
                    t *= Matrix.rotx(args[1])
                elif ( args[0] == 'y' ):
                    t *= Matrix.roty(args[1])
                elif ( args[0] == 'z' ):
                    t *= Matrix.rotz(args[1])
            elif ( cmd[i] == "apply" ):
                e *= t
                p *= t
            elif ( cmd[i] == "clear" ):
                e = Matrix(0,4)
                p = Matrix(0,4)
            elif ( cmd[i] == "display" ):
                self.clear()
                self.draw_lines(e, color)
                self.draw_polygons(p, color)
                self.display()
            elif ( cmd[i] == "save" ):
                self.clear()
                self.draw_lines(e, color)
                self.draw_polygons(p, color)
                self.save_extension(args[0])
            elif ( cmd[i] == "quit" ):
                return
            elif ( cmd[i] == "circle" ):
                e.add_circle(*args)
            elif ( cmd[i] == "bezier" or cmd[i] == "hermite" ):
                e.add_curve(*args,0.001,cmd[i])
            elif ( cmd[i] == "box" ):
                p.add_box(*args)
            elif ( cmd[i] == "sphere" ):
                p.add_sphere(*args)
            elif ( cmd[i] == "torus" ):
                p.add_torus(*args)
        

