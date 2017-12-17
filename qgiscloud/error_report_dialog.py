# -*- coding: utf-8 -*-
"""
/***************************************************************************
OpenLayers Plugin
A QGIS plugin

                             -------------------
begin                : 2015-06-08
copyright            : (C) 2015 by Sandro Mani, Sourcepole
email                : smani at sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries

try:
    from PyQt5.QtCore import * 
    from PyQt5.QtGui import * 
    from PyQt5.QtWidgets import *
    from PyQt5.QtXml import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtXml import *
    
from qgis.core import *
from .about.metadata import MetaData
#from . import apicompat
import urllib.request, urllib.parse, urllib.error
import sys
import platform


class ErrorReportDialog(QDialog):
    def __init__(self, title, message, errors, username, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)

        self.verticalLayout = QVBoxLayout(self)

        self.label = QLabel(message, self)
        self.verticalLayout.addWidget(self.label)

        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.setPlainText(errors)
        self.plainTextEdit.setReadOnly(True)
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.verticalLayout.addWidget(self.buttonBox)
        self.reportButton = self.buttonBox.addButton(self.tr("Report error"), QDialogButtonBox.ActionRole)

        self.reportButton.clicked.connect(self.__reportError)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.username = username

    def __reportError(self):
        body = ("Please provide any additional information here:\n\n\n"
                "If you encountered an upload error, if possible please attach a zip file containing a minimal extract of the dataset, as well as the QGIS project file.\n\n\n"
                "Technical information:\n%s\n\n"
                "Versions:\n"
                " QGIS: %s\n"
                " Python: %s\n"
                " OS: %s\n"
                " QGIS Cloud Plugin: %s\n\n"
                "Username: %s\n") % (
                    self.plainTextEdit.toPlainText(),
                    Qgis.QGIS_VERSION,
                    sys.version.replace("\n", " "),
                    platform.platform(),
                    MetaData().version(), 
                    self.username)
        url = QUrl()
        url.setEncodedUrl("mailto:support@qgiscloud.com?subject=%s&body=%s" % (
                urllib.parse.quote(pystring(self.windowTitle())),
                urllib.parse.quote(body)),
        )
        QDesktopServices.openUrl(url)
