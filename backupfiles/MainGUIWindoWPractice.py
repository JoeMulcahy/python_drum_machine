import sys
class MainGUIWindow(QMainWindow):
    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height
        super(MainGUIWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Window Title")
        # self.setFixedSize(self.width, self.height)

        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)

        self.setWindowTitle("My App")

        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")
        print(e.pos)

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")

    def wheelEvent(self, event):
        angle = event.angleDelta().y()

        if angle > 0:
            self.label.setText("Wheel Up")
        elif angle < 0:
            self.label.setText("Wheel Down")


    def the_button_was_clicked(self):
        print("Clicked.")
        new_window_title = choice(window_titles)
        print("Setting title:  %s" % new_window_title)
        self.setWindowTitle(new_window_title)
        sound = SinWave('sine', 880, 2, 0.5, 44100)
        sound.play()

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)

