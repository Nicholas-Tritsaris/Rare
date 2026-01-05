import webbrowser

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from rare.lgndr.core import LegendaryCore
from rare.models.signals import GlobalSignals
from rare.utils.account_manager import AccountManager
from rare.utils.misc import ExitCodes, qta_icon
from rare.shared import RareCore

class AccountWidget(QWidget):
    # int: exit code
    exit_app: Signal = Signal(int)
    logout: Signal = Signal()

    def __init__(self, signals: GlobalSignals, rcore: RareCore, parent):
        super(AccountWidget, self).__init__(parent=parent)
        self.signals = signals
        self.rcore = rcore
        self.core = rcore.core()
        self.account_manager = self.rcore.account_manager

        self.account_combo = QComboBox()
        accounts = self.account_manager.list_accounts()
        for account_id, display_name in accounts.items():
            self.account_combo.addItem(display_name, userData=account_id)

        current_account_id = self.core.lgd.userdata.get("accountId")
        if current_account_id:
            index = self.account_combo.findData(current_account_id)
            if index != -1:
                self.account_combo.setCurrentIndex(index)

        self.account_combo.currentIndexChanged.connect(self._on_account_changed)

        self.add_account_button = QPushButton(self.tr("Add Account"))
        self.add_account_button.clicked.connect(self._on_add_account)

        account_layout = QHBoxLayout()
        account_layout.addWidget(self.account_combo)
        account_layout.addWidget(self.add_account_button)

        self.open_browser = QPushButton(
            qta_icon("fa.external-link", "fa5s.external-link-alt"),
            self.tr("Account settings"),
        )
        self.open_browser.clicked.connect(self._on_browser_clicked)

        self.logout_button = QPushButton(self.tr("Logout"), parent=self)
        self.logout_button.clicked.connect(self._on_logout)
        self.quit_button = QPushButton(self.tr("Quit"), parent=self)
        self.quit_button.clicked.connect(self._on_quit)

        layout = QVBoxLayout(self)
        layout.addLayout(account_layout)
        vspacer = QSpacerItem(
            10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        layout.addSpacerItem(vspacer)
        layout.addWidget(self.open_browser)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.quit_button)

    @Slot()
    def _on_browser_clicked(self):
        webbrowser.open(
            "https://www.epicgames.com/account/personal?productName=epicgames"
        )

    @Slot()
    def _on_quit(self):
        self.exit_app.emit(ExitCodes.EXIT)

    @Slot()
    def _on_logout(self):
        self.exit_app.emit(ExitCodes.LOGOUT)

    @Slot(int)
    def _on_account_changed(self, index):
        account_id = self.account_combo.itemData(index)
        if account_id and account_id != self.core.lgd.userdata.get("accountId"):
            self.account_manager.switch_account(account_id)
            self.exit_app.emit(ExitCodes.RESTART)

    @Slot()
    def _on_add_account(self):
        self.rcore.adding_account = True
        self.exit_app.emit(ExitCodes.LOGOUT)
