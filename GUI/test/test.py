from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QTransform

app = QApplication([])

# Load the pixmap from a file (change this to your own file)
pixmap = QPixmap('MDPSaver.png')

# Create the graphics items
scene = QGraphicsScene()
pixmap_item = scene.addPixmap(pixmap)

# Create the view
view = QGraphicsView(scene)

# Use a transform to scale down the view
transform = QTransform()
transform.scale(0.5, 0.5)  # This will make the view half the original size
view.setTransform(transform)

view.show()

app.exec()