import Grapher

graph = Grapher.Graph(Grapher.Settings())

plot = Grapher.Plot(graph)
plot.plotTxt("sampledata.txt")

graph.registerPlot(plot)

# Turtle does not support multiple windows opening at once,
# so this should graph on top of the previous graph with a
# new scale
graph2 = Grapher.Graph(Grapher.Settings())

plot2 = Grapher.Plot(graph2)
plot2.plotEquation(lambda x: x**2)

plot3 = Grapher.Plot(graph2)
plot3.plotEquation(lambda x: x**3)

graph2.registerPlot(plot2)
graph2.registerPlot(plot3)

graph.drawPlots()
graph2.drawPlots()

data = Grapher.Data(plot)
print("Max: %d" % data.getMax())
print("Avg: %d" % data.getAvg())

graph.wn.exitonclick()
