from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QHBoxLayout, QLabel, QMainWindow, QWidget
from PySide6.QtGui import QPixmap, QFont, QTransform

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a widget to hold the layout
        widget = QWidget()
        self.setCentralWidget(widget)

        # Create a QHBoxLayout
        layout = QHBoxLayout(widget)

        # Load an image
        user_path = "user.png"
        self.pixmap = QPixmap(user_path)

        # Create a QGraphicsView instance
        graphics_user = QGraphicsView()

        # Create a QGraphicsScene instance
        user_scene = QGraphicsScene()
        graphics_user.setScene(user_scene)

        # Create a QGraphicsPixmapItem and add it to the scene
        pixmap_item = user_scene.addPixmap(self.pixmap)

        # Adjust the width and height of the scene
        scene_width = self.pixmap.width() * 0.1  # Adjust the width as needed
        scene_height = self.pixmap.height() * 0.1  # Adjust the height as needed
        user_scene.setSceneRect(0, 0, scene_width, scene_height)

        # Scale the QGraphicsView to fit the scene
        transform_user = QTransform()
        transform_user.scale(1.0, 1.0)  # Adjust the scaling as needed
        graphics_user.setTransform(transform_user)

        # Create a QLabel for the text
        label_text = QLabel("GaecKo")
        font = QFont()
        font.setPointSize(16)  # Adjust the font size as needed
        label_text.setFont(font)

        # Add the QGraphicsView and QLabel to the QHBoxLayout
        layout.addWidget(graphics_user)
        layout.addWidget(label_text)

        # Set the QHBoxLayout as the main layout
        widget.setLayout(layout)


if __name__ == "__main__":
    # Create the application
    app = QApplication([])

    # Create the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    app.exec()
