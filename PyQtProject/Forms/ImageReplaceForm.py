from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTabWidget, QGridLayout, QTableWidget, \
    QTableWidgetItem, QPushButton, QWidget, QDialog, QScrollArea, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPalette
from UIs.ImageReplaceUI_ui import Ui_Form


class ImageReplaceForm(QDialog, Ui_Form):
    def __init__(self, element_id, element_property, image_data):
        super(ImageReplaceForm, self).__init__()
        self.setupUi(self)

        self.new_image_name = None
        self.image_scale = 0.0

        self.element_id = element_id
        self.element_property = element_property

        self.image.setBackgroundRole(QPalette.Base)
        self.image.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image.setScaledContents(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)

        qimg = QImage.fromData(image_data)
        pixmap = QPixmap.fromImage(qimg)
        self.image.setPixmap(pixmap)
        self.image.adjustSize()
        self.image_scale = 1.0

        self.connect_buttons_to_functions()

    def connect_buttons_to_functions(self):
        self.openImageButton.clicked.connect(self.open_image)
        self.zoomInBtn.clicked.connect(self.zoom_in)
        self.zoomOutBtn.clicked.connect(self.zoom_out)
        self.normalSizeZoomBtn.clicked.connect(self.set_normal_size)

    def open_image(self):
        self.new_image_name = QFileDialog.getOpenFileName(self, "Выберите картинку", '', "*.jpeg, *.jpg")[0]
        if self.new_image_name:
            pixmap = QPixmap(self.new_image_name)
            self.image.setPixmap(pixmap)
            self.image_scale = 1.0
            self.image.adjustSize()
            self.replaceImageButton.setEnabled(True)
        else:
            self.replaceImageButton.setEnabled(False)

    def zoom_in(self):
        self.scale_image(1.1)

    def zoom_out(self):
        self.scale_image(0.9)

    def set_normal_size(self):
        self.image.adjustSize()
        self.image_scale = 1.0

    def scale_image(self, scale):
        self.image_scale *= scale
        self.image.resize(self.image_scale * self.image.pixmap().size())



