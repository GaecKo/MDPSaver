from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QHBoxLayout, QSizePolicy, QLabel
from PySide6.QtGui import QTransform, QPixmap


class SceneImage(QWidget):
    def __init__(self, image_path, t_sx, t_sy) -> None:

        super(SceneImage, self).__init__()

        self.GenHBox = QHBoxLayout(self)

        # View and Scene creation
        self.graphic_view = QGraphicsView()
        self.graphic_scene = QGraphicsScene()

        self.graphic_view.setScene(self.graphic_scene)

        # Load and set the image
        pixmap = QPixmap(image_path)

        self.graphic_scene.addPixmap(pixmap)

        self.transform = QTransform()
        self.transform.scale(t_sx, t_sy)
        self.graphic_view.setTransform(self.transform)
        

        self.GenHBox.addWidget(self.graphic_view)
        self.graphic_view.show()
        self.setLayout(self.GenHBox)

        
    def set_transform(self, t_sx, t_sy):
        self.transform.scale(t_sx, t_sy)
        self.graphic_view.setTransform(self.transform)
        self.graphic_view.update()

    def setSizePolicy(self, horizontal, vertical):
        self.graphic_view.setSizePolicy(horizontal, vertical)
        self.graphic_view.update()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    image = SceneImage("../MDPSaverLogic.png", 0.5, 0.5)
    image.show()

    sys.exit(app.exec())