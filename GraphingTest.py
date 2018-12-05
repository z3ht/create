import Grapher

graph = Grapher.Graph(Grapher.Settings())

plot = Grapher.Plot(graph)
plot.plotEquation(lambda x: x**2)

plot2 = Grapher.Plot(graph)
plot2.plotEquation(lambda x: x**3)

graph.registerPlot(plot)
graph.registerPlot(plot2)

graph.drawPlots()

data2 = Grapher.Data(plot2)
print(data2.getMax())

graph.wn.exitonclick()