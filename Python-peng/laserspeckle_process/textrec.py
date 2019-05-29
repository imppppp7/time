import  numpy as np
import  PyQt5
import  pyqtgraph as pg
import  sys

win = pg.GraphicsWindow(title="v distribution")
win.resize(500, 300)
win.setWindowTitle('v distribution plotting')
p = win.addPlot(title='v distribution')
p.setLabel(axis='left', text='number')
p.setLabel(axis='bottom', text='v')
p.setRange(yRange=[0, 1], padding=0)
curve = p.plot(pen='y')
curve.setData(np.arange(10))

a=1


