# pylint: disable=R0903
from logging import getLogger
from typing import Optional
from enum import Enum, auto

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QLabel, QWidget
from shiboken6 import Shiboken

from rare.utils.qt_requests import QtRequests
from rare.widgets.loading_widget import QLoadingIndicator


class ImageSize(Enum):
    Icon = auto()
    LibraryIcon = auto()
    StoreItem = auto()


class CoverImage(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def paintEvent(self, a0) -> None:
        if not self.pixmap():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        brush = QBrush(self.pixmap())
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 7, 7)


class ImageWidget(CoverImage):
    image_loaded = Signal(bool)

    def __init__(self, parent=None, size: Optional[QSize] = None):
        super(ImageWidget, self).__init__(parent=parent)
        self.setObjectName(type(self).__name__)
        self.logger = getLogger(type(self).__name__)
        self.image_url = None
        self.image_data = None
        self.manager = QtRequests(parent=self)
        if size:
            self.setFixedSize(size)
        self.setScaledContents(False)
        self._loading = False
        self._loaded = False
        self.image_loaded.connect(self.on_image_loaded)

    def on_image_loaded(self, loaded: bool):
        self._loaded = loaded
        self._loading = False

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def loading(self) -> bool:
        return self._loading

    def setPixmap(self, a0: QPixmap) -> None:
        if self.size().width() > self.size().height():
            super(ImageWidget, self).setPixmap(a0.scaledToWidth(self.size().width()))
        else:
            super(ImageWidget, self).setPixmap(a0.scaledToHeight(self.size().height()))
        self.update()

    def set_faded_pixmap(self, pixmap: QPixmap, fade_color: str):
        if not pixmap:
            return
        image = pixmap.toImage()
        painter = QPainter(image)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), QColor(fade_color))
        painter.end()
        faded_pixmap = QPixmap.fromImage(image)
        self.setPixmap(faded_pixmap)

    def set_url(self, url: str, high_res_url: str = None, callback=None) -> None:
        if not url or self.image_url == url:
            return
        self.image_url = url
        self._loading = True
        self.manager.get(url, lambda data: self._on_image_ready(data, high_res_url, callback))

    def _on_image_ready(self, data, high_res_url: str = None, callback=None):
        # Check if the C++ object is still alive, otherwise it will crash
        if not Shiboken.isValid(self):
            self.logger.debug("ImageWidget is no longer valid, skipping pixmap set")
            return

        self.image_data = data
        cover = QPixmap()
        cover.loadFromData(data)
        if not cover.isNull():
            self.image_loaded.emit(True)
        else:
            self.image_loaded.emit(False)
        self.setPixmap(cover)
        if callback:
            callback(data)
        if high_res_url:
            self.manager.get(high_res_url, lambda data: self._on_high_res_ready(data, callback))

    def _on_high_res_ready(self, data, callback=None):
        self.image_data = data
        cover = QPixmap()
        cover.loadFromData(data)
        self.setPixmap(cover)
        if callback:
            callback(data)

    def sizeHint(self):
        return self.size()

    def heightForWidth(self, w: int) -> int:
        return int(w / 1.5)


class StoreItemImage(ImageWidget):
    def __init__(self, parent=None, size: Optional[QSize] = None):
        super().__init__(parent, size)

    def _on_image_ready(self, data, high_res_url: str = None, callback=None):
        super()._on_image_ready(data)
        self.set_url(high_res_url)


class LoadingImageWidget(ImageWidget):
    def __init__(self, manager: QtRequests, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.url = ""

    def fetchPixmap(self, url: str):
        if url == self.url:
            return
        self.url = url
        self.manager.get(url, self._on_image_ready)


class LoadingSpinnerImageWidget(ImageWidget):
    def __init__(self, parent=None, size: Optional[QSize] = None):
        super().__init__(parent, size)
        self.spinner = QLoadingIndicator(parent=self)
        self.image_loaded.connect(self.spinner.stop)

    def set_url(self, url: str, high_res_url: str = None, callback=None) -> None:
        super().set_url(url, high_res_url, callback)
        if not self.loaded and self.loading:
            self.spinner.start()
