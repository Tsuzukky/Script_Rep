import hou
import zipfile
import os
import time
import hdefereval
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
Qt = QtCore.Qt

__VERSION__ = "0.0.2"

IGNORES = ["CONVERTED"]

class IconViewer(QtWidgets.QWidget):

    def __init__(self, icon_name, parent=None):
        super(IconViewer, self).__init__(parent=parent)

        self.raw_ico_file = icon_name
        self.icon_name = icon_name.replace('/', '_').replace('.svg', '')
        self.raw_name, self.raw_type = icon_name.split('/')

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignLeft)
        self.setFixedHeight(45)

        self.large_pixmap = None

        try:
            ico_xs = hou.ui.createQtIcon(self.icon_name, 12, 12)
            lbl_xs = QtWidgets.QLabel("")
            lbl_xs.setPixmap(ico_xs.pixmap(12, 12))
            main_layout.addWidget(lbl_xs)

            ico_m = hou.ui.createQtIcon(self.icon_name, 24, 24)
            lbl_m = QtWidgets.QLabel("")
            lbl_m.setPixmap(ico_m.pixmap(24, 24))
            main_layout.addWidget(lbl_m)

            ico_l = hou.ui.createQtIcon(self.icon_name, 32, 32)
            lbl_l = QtWidgets.QLabel("")
            self.large_pixmap = ico_l.pixmap(64, 64)
            lbl_l.setPixmap(ico_l.pixmap(32, 32))
            main_layout.addWidget(lbl_l)

            line = QtWidgets.QLineEdit(self.icon_name)
            line.setReadOnly(True)
            main_layout.addWidget(line)

            save_btn = QtWidgets.QPushButton("")
            save_btn.setFlat(True)
            save_btn.setToolTip("Extract icon as .svg file")
            save_btn.setIcon(hou.ui.createQtIcon("COMMON_file", 24 ,24))
            save_btn.setIconSize(QtCore.QSize(24, 24))
            save_btn.setFixedHeight(30)
            save_btn.setFixedWidth(30)
            save_btn.clicked.connect(self.save_ico)
            main_layout.addWidget(save_btn)

        except hou.OperationFailed:
            main_layout.addWidget(QtWidgets.QLabel("Invalid name: " + \
                                                   icon_name))

        self.setLayout(main_layout)

    def save_ico(self):

        icons_archive =  os.path.join(hou.expandString("$HH"),
                                      "help",
                                      "icons.zip")

        if os.path.exists(icons_archive):

            r = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                           ("Select a folder to "
                                                            "export the icon "
                                                            "( as .svg file )"))
            if not r:
                return

            with zipfile.ZipFile(icons_archive, 'r') as z:
                z.extract(self.raw_ico_file, r)

            msg = r + '/' + \
                  self.raw_ico_file + \
                  " extracted !"

            hou.ui.displayMessage(msg, title="Icon extracted")
            

class IconsFetcherSignals(QtCore.QObject):

    start_process = QtCore.Signal()
    init_progress = QtCore.Signal(int)
    add_icon = QtCore.Signal(str)
    raise_icon_types = QtCore.Signal(list)
    end_process = QtCore.Signal(int)

class IconFetcher(QtCore.QRunnable):

    def __init__(self, icons_archive):
        super(IconFetcher, self).__init__()

        self.setAutoDelete(True)
        self.cancel_proc = False
        self.icons_archive = icons_archive
        self.signals = IconsFetcherSignals()

    def run(self):

        self.signals.start_process.emit()

        icons_types = []
        icons = []
        with zipfile.ZipFile(self.icons_archive, 'r') as archive:
            icons = [ico for ico in archive.namelist() \
                     if ico.split('/')[0].isupper()]

        self.signals.init_progress.emit(len(icons))

        for ico in icons:
            if self.cancel_proc:
                self.signals.end_process.emit(0)
                self.signals.raise_icon_types.emit(icons_types)
                return

            ico_type = ico.split('/')[0]

            if ico_type in IGNORES:
                continue

            if not ico_type in icons_types:
                icons_types.append(ico_type)

            time.sleep(0.01)
            self.signals.add_icon.emit(ico)

        self.signals.raise_icon_types.emit(icons_types)

        self.signals.end_process.emit(1)
        

class IconsBrowser(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(IconsBrowser, self).__init__(parent=parent)

        self.setProperty("houdiniStyle", True)

        self.icons = []
        self.icons_types = {}

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(QtWidgets.QLabel("Icons Browser version " + \
                              __VERSION__))

        icons_archive =  os.path.join(hou.expandString("$HH"),
                                      "help",
                                      "icons.zip")
        
        valid_archive = True
        if not os.path.exists(icons_archive):
            main_layout.addWidget(QtWidgets.QLabel(("Error: icons.zip "
                                                    "not found in $HH/help")))
            valid_archive = False

        if valid_archive:

            progress_layout = QtWidgets.QHBoxLayout()
            progress_layout.setAlignment(Qt.AlignLeft)

            self.n_items = 0
            self.n_items_lbl = QtWidgets.QLabel("-")
            progress_layout.addWidget(self.n_items_lbl)

            self.progress_bar = QtWidgets.QProgressBar()
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setFixedHeight(5)
            progress_layout.addWidget(self.progress_bar)

            self.cancel_btn = QtWidgets.QPushButton("Cancel")
            self.cancel_btn.clicked.connect(self.cancel_progress)
            progress_layout.addWidget(self.cancel_btn)

            main_layout.addLayout(progress_layout)

            filter_layout = QtWidgets.QHBoxLayout()
            filter_layout.setAlignment(Qt.AlignLeft)

            filter_layout.addWidget(QtWidgets.QLabel("Filter:"))

            self.filter_types = QtWidgets.QComboBox()
            self.filter_types.currentTextChanged.connect(self.update_filter)
            self.filter_types.setDisabled(True)
            filter_layout.addWidget(self.filter_types)

            self.filter_input = QtWidgets.QLineEdit()
            self.filter_input.textChanged.connect(self.update_filter)
            self.filter_input.setDisabled(True)
            filter_layout.addWidget(self.filter_input)

            main_layout.addLayout(filter_layout)

            self.icons_scroll = QtWidgets.QScrollArea()
            self.icons_scroll.setWidgetResizable(True)
            self.icons_scrloll_widget = QtWidgets.QWidget(self)
            self.icons_layout = QtWidgets.QVBoxLayout()
            self.icons_layout.setAlignment(Qt.AlignTop)
            self.icons_scrloll_widget.setLayout(self.icons_layout)
            self.icons_scroll.setWidget(self.icons_scrloll_widget)
            main_layout.addWidget(self.icons_scroll)

            code_snip = ('Python code snippet:           '
                         'ico = hou.ui.createQtIcon("<NAME OF THE ICON>", '
                         'width=32, height=32)')
            snip_lbl = QtWidgets.QLabel(code_snip)
            main_layout.addWidget(snip_lbl)

            self.fetcher = IconFetcher(icons_archive)
            self.fetcher.signals.init_progress.connect(self.init_progress_sgn)
            self.fetcher.signals.raise_icon_types.connect(self.raise_icon_types_sgn)
            self.fetcher.signals.end_process.connect(self.end_proc_sgn)
            self.fetcher.signals.add_icon.connect(self.add_icon_sgn)

            QtCore.QThreadPool.globalInstance().start(self.fetcher)

        self.setLayout(main_layout)

    def raise_icon_types_sgn(self, items):

        types = ["All"] + items
        self.filter_types.addItems(types)

    def end_proc_sgn(self, r):

        self.cancel_btn.setDisabled(True)
        self.filter_types.setDisabled(False)
        self.filter_input.setDisabled(False)

        if r == 1:
            self.progress_bar.setValue(self.progress_bar.maximum())

    def init_progress_sgn(self, nitems):
        
        self.progress_bar.setMaximum(nitems)

    def add_icon_sgn(self, icon):
        
        w = IconViewer(icon, self)
        
        self.icons.append(w)
        self.icons_layout.addWidget(w)

        c = self.progress_bar.value()
        self.progress_bar.setValue(c + 1)

        self.n_items += 1
        self.n_items_lbl.setText(str(self.n_items) + " icons")

    def cancel_progress(self):

        self.fetcher.cancel_proc = True

    def update_filter(self):

        cur_type = self.filter_types.currentText()

        if cur_type != "All":
            cur_filter = cur_type + '_' + self.filter_input.text()

        else:
            cur_filter = self.filter_input.text()

        for ico in self.icons:

            if not cur_filter:
                ico.show()
                continue

            if cur_filter in ico.icon_name:
                ico.show()
            else:
                ico.hide()