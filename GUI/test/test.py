from PySide6.QtCore import QAbstractState, QEvent, QPointF, Property, QEasingCurve, Qt, QSignalTransition, QTimer
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QMainWindow


class SwipeAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_pos = QPointF()
        self.current_pos = QPointF()
        self.animating = False
        self.animation_duration = 200
        self.swipe_threshold = 50

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            self.current_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            delta_x = self.current_pos.x() - self.start_pos.x()
            if delta_x > self.swipe_threshold:  # Swipe Right
                self.swipe_right_animation()
            elif delta_x < -self.swipe_threshold:  # Swipe Left
                self.swipe_left_animation()

    def swipe_right_animation(self):
        if self.animating:
            return

        self.animating = True
        stacked_widget = self.parent().parent()  # Assuming SwipeAnimation is a direct child of QStackedWidget

        current_index = stacked_widget.currentIndex()
        next_index = current_index - 1
        if next_index < 0:
            next_index = stacked_widget.count() - 1

        current_widget = stacked_widget.widget(current_index)
        next_widget = stacked_widget.widget(next_index)

        current_geometry = current_widget.geometry()
        next_geometry = next_widget.geometry()

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.finished.connect(self.animation_finished)

        self.current_animation = QPropertyAnimation(current_widget, b"geometry")
        self.current_animation.setDuration(self.animation_duration)
        self.current_animation.setStartValue(current_geometry)
        self.current_animation.setEndValue(
            QRect(-current_geometry.width(), 0, current_geometry.width(), current_geometry.height())
        )
        self.animation_group.addAnimation(self.current_animation)

        self.next_animation = QPropertyAnimation(next_widget, b"geometry")
        self.next_animation.setDuration(self.animation_duration)
        self.next_animation.setStartValue(QRect(next_geometry.width(), 0, next_geometry.width(), next_geometry.height()))
        self.next_animation.setEndValue(next_geometry)
        self.animation_group.addAnimation(self.next_animation)

        stacked_widget.setCurrentIndex(next_index)
        self.animation_group.start()

    def swipe_left_animation(self):
        if self.animating:
            return

        self.animating = True
        stacked_widget = self.parent().parent()  # Assuming SwipeAnimation is a direct child of QStackedWidget

        current_index = stacked_widget.currentIndex()
        next_index = (current_index + 1) % stacked_widget.count()

        current_widget = stacked_widget.widget(current_index)
        next_widget = stacked_widget.widget(next_index)

        current_geometry = current_widget.geometry()
        next_geometry = next_widget.geometry()

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.finished.connect(self.animation_finished)

        self.current_animation = QPropertyAnimation(current_widget, b"geometry")
        self.current_animation.setDuration(self.animation_duration)
        self.current_animation.setStartValue(current_geometry)
        self.current_animation.setEndValue(
            QRect(current_geometry.width(), 0, current_geometry.width(), current_geometry.height())
        )
        self.animation_group.addAnimation(self.current_animation)

        self.next_animation = QPropertyAnimation(next_widget, b"geometry")
        self.next_animation.setDuration(self.animation_duration)
        self.next_animation.setStartValue(QRect(-next_geometry.width(), 0, next_geometry.width(), next_geometry.height()))
        self.next_animation.setEndValue(next_geometry)
        self.animation_group.addAnimation(self.next_animation)

        stacked_widget.setCurrentIndex(next_index)
        self.animation_group.start()

    def animation_finished(self):
        self.animating = False
        self.animation_group = None
        self.current_animation = None
        self.next_animation = None


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stacked_widget = QStackedWidget(self)
        self.swipe_animation = SwipeAnimation(self)

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.stacked_widget)
        self.central_layout.addWidget(self.swipe_animation)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        # Add your widgets to the QStackedWidget
        widget1 = QWidget()
        widget2 = QWidget()
        widget3 = QWidget()

        self.stacked_widget.addWidget(widget1)
        self.stacked_widget.addWidget(widget2)
        self.stacked_widget.addWidget(widget3)

        self.stacked_widget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
