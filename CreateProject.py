import turtle
import glob
from enum import Enum


class Graph:

    def __init__(self, settings):
        self.points = []
        self.isDrawn = False
        self.scale = 1

        self.settings = settings

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

        self.wn = turtle.Screen()

    def plotTxt(self, filePath):
        try:
            for line in open(filePath, "r").readlines():
                point = line.split()
                self.plotPoint(int(point[0]), int(point[1]))
        except OSError:
            print("The file at: %s could not be found." % filePath)
            return


    def plotPoint(self, x, y):
        self.points.append([x, y])

    def setup(self):
        self.isDrawn = True

        xMax = self.points[0][0]
        yMax = self.points[0][1]
        for point in self.points:
            if (xMax < point[0]):
                xMax = point[0]
            if (yMax < point[1]):
                yMax = point[1]

        self.scale = min(self.settings.xMax/xMax, self.settings.yMax/yMax, 1)

        self.wn.screensize(self.settings.xMax*1.2, self.settings.yMax*1.2)

    def drawGraph(self):
        self.setup()

    def drawSlope(self):
        if (not self.isDrawn):
            self.drawGraph()

        slope = None
        try:
            slope = self.settings.slope(self)
        except TypeError:
            x = 0

        if(not Preconditions.isInstance(slope, Slope, " ## WARN ## :: Settings file does not contain a slope value. Using SimpleSlope.")):
            slope = SimpleSlope(self)

        slope.drawSlope()


class Slope:

    def __init__(self, graph):
        self.graph = graph

    def drawSlope(self):
        pass


class SimpleSlope(Slope):
    def __init__(self, graph):
        Slope.__init__(self, graph)

    def drawSlope(self):
        for point in self.graph.points:
            self.graph.turtle.setpos(int(point[0])*graph.scale, int(point[1]*graph.scale))


class SlopeType(Enum):
    simple_slope = SimpleSlope


class Settings:

    def __init__(self, filePath=None):
        try:
            self.file = open(filePath, "r")

            self.slope = SlopeType[self.getString("slope").lower()]
            self.color = self.getString("color")
            self.point = self.getString("point")

            self.xMax = int(self.getString("xmax"))
            self.yMax = int(self.getString("ymax"))

        except OSError:
            # With more time I could add GUI support here
            print(" ## ERROR ## :: filePath must be a string path to a .txt file")
            return

    def getString(self, key):
        for line in self.file.readlines():
            words = line.split()
            if(not words[0] == "%s:" % key.lower()):
                continue
            return words[1]


class TestSettings(Settings):

    def __init__(self):
        self.slope = SimpleSlope
        self.color = "red"
        self.point = "circle"

        self.xMax = 200
        self.yMax = 200


class File:

    @staticmethod
    def inferTxtFile(self, dir="."):
        return open(glob.glob("%s/*.txt" % dir)[0], "r")


class Preconditions:

    @staticmethod
    def isInstance(obj, objType, errorMessage=""):
        if(isinstance(obj, objType)):
            return True
        print(errorMessage)
        return False


graph = Graph(TestSettings())

graph.plotPoint(0, 0)
graph.plotPoint(100, 100)
graph.plotPoint(-20, 40)
graph.plotPoint(1000, 1000)
graph.drawSlope()

graph.wn.exitonclick()
