import turtle
import re
import uuid
from enum import Enum


class Graph:

    def __init__(self, settings):
        self.plots = {}
        self.isDrawn = False

        self.settings = settings

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()

    def registerPlot(self, plot):
        self.plots[plot.id] = plot

    def setup(self):
        self.wn = turtle.Screen()

        if (len(self.plots) == 0):
            print("No points set. The graph could not be scaled")
            return

        isScalable = False
        xMax = 0
        yMax = 0
        for plot in self.plots.values():
            if (len(plot.points) == 0):
                continue
            xMax = plot.points[0][0]
            yMax = plot.points[0][1]
            isScalable = True
            break

        if (not isScalable):
            print("The graph could not be scaled. This is likely because no points were set")
            return

        for plot in self.plots.values():
            for point in plot.points:
                if (xMax < point[0]):
                    xMax = point[0]
                if (yMax < point[1]):
                    yMax = point[1]

        self.scale = min(self.settings.xMax / xMax, self.settings.yMax / yMax)

        self.wn.screensize(self.settings.xMax, self.settings.yMax)

    def drawGraph(self):
        self.isDrawn = True
        self.setup()

        self.turtle.penup()
        self.turtle.setpos(-1 * self.settings.xMax, 0)
        self.turtle.pendown()
        self.turtle.setpos(self.settings.xMax, 0)
        self.turtle.penup()
        self.turtle.setpos(0, -1 * self.settings.yMax)
        self.turtle.pendown()
        self.turtle.setpos(0, self.settings.yMax)

    def drawPlots(self):
        if (not self.isDrawn):
            self.drawGraph()

        for plotId in self.plots:
            self.plots[plotId].drawSlope(self.settings.slope)

    def drawPlot(self, plotId):

        if (not self.isDrawn):
            self.drawGraph()

        if (plotId == None or not plotId in self.plots):
            print("The plot could not be found")
            return

        self.plots[plotId].drawSlope(self.settings.slope)


class Plot:

    def __init__(self, graph):
        self.points = []
        self.isDrawn = False
        self.id = uuid.uuid4()

        self.graph = graph

    def plotPoint(self, x, y):
        self.points.append([x, y])

    def plotEquation(self, eq, range=[-1, 1, .01]):
        x = range[0]
        while x <= range[1]:
            self.plotPoint(x, eq(x))
            x += range[2]

    def plotTxt(self, filePath):
        try:
            c = 0
            for line in open(filePath, "r").readlines():
                point = line.split()
                if (len(point) == 1):
                    self.plotPoint(float(c * self.graph.settings.xStep), float(point[0]))
                elif (len(point) == 2):
                    self.plotPoint(float(re.sub("\D+", "", point[0])), float(re.sub("\D+", "", point[1])))
                c += 1
        except OSError:
            print("The file at: %s could not be found." % filePath)
            return

    def drawSlope(self, slope):
        if (not Preconditions.isInstance(slope(self), Slope, " ## WARN ## :: Settings file does not contain a slope value. Using SimpleSlope.")):
            slope = SimpleSlope

        self.graph.turtle.penup()
        self.graph.turtle.setpos(self.points[0][0] * self.graph.scale, self.points[0][1] * self.graph.scale)
        self.graph.turtle.pendown()

        slope(self).drawSlope()


class Slope:

    def __init__(self, plot):
        self.plot = plot

    def drawSlope(self):
        pass


class SimpleSlope(Slope):
    def __init__(self, plot):
        Slope.__init__(self, plot)

    def drawSlope(self):
        for point in self.plot.points:
            self.plot.graph.turtle.setpos(float(point[0]) * self.plot.graph.scale,
                                          float(point[1] * self.plot.graph.scale))


class SlopeType(Enum):
    SIMPLE_SLOPE = SimpleSlope


class Settings:

    def __init__(self):
        self.slope = SimpleSlope
        self.color = "red"
        self.point = "circle"

        self.xRange = [-1, 1]
        self.yRange = [-1, 1]

        self.xMax = 300
        self.yMax = 300

        self.xStep = 2
        self.yStep = 2


class Data:

    def __init__(self, plot):
        self.plot = plot

    def getMax(self):
        try:
            return self.max
        except AttributeError:
            max = self.plot.points[0][1]
            for point in self.plot.points:
                if (point[1] > max):
                    max = point[1]
            self.max = max
            return self.getMax()

    def getMin(self):
        try:
            return self.min
        except AttributeError:
            min = self.plot.points[0][1]
            for point in self.plot.points:
                if (point[1] < min):
                    min = point[1]
            self.min = min
            return self.getMin()

    def getSum(self):
        try:
            return self.sum
        except AttributeError:
            sum = 0
            for point in self.plot.points:
                sum += point[1]
            self.sum = sum
            return self.getSum()

    def getAvg(self):
        try:
            return self.avg
        except AttributeError:
            self.avg = self.getSum() / len(self.plot.points)
            return self.getAvg()


class Preconditions:

    @staticmethod
    def isInstance(obj, objType, errorMessage=""):
        if (isinstance(obj, objType)):
            return True
        print(errorMessage)
        return False
