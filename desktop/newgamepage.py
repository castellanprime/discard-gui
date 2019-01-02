"""
	Copyright 2018 Okusanya David
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

		http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
"""

import sys
import logging
import constants

from PySide2.QtWidgets import (
	QApplication, QWidget, QMainWindow,
	QGroupBox, QGridLayout, QTabWidget,
	QFormLayout, QSpinBox, QHBoxLayout,
	QAction,QLineEdit,
	QLabel, QListWidget, QAbstractItemView,
	QPushButton, QVBoxLayout, QDesktopWidget,
)
from PySide2.QtCore import (
	Signal, Qt
)
from PySide2.QtGui import QIcon

class NewGamePage(QMainWindow):
	
	next_step = Signal(dict)
	
	def __init__(self):
		super().__init__()
		self._logger = logging.getLogger(__name__)
		self.username = ''
		self._initGUI()
		
	def setUsername(self, strs):
		self.username = strs
		
	# Layout	
	def _show(self):
		self.show()
		self._logger.info('Starting new page window')	
		
	def _center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	def _launch_help_window(self):
		pass
	
	def _enableBtn(self):
		sender = self.sender()
		if len(sender.text()) > 3:
			self.joingame_btn.setEnabled(True)
		else:
			self.joingame_btn.setEnabled(False)
	
	def _create_form(self):
		form = QFormLayout()
		
		self.gamename = QLineEdit()
		self.gamename.setMaxLength(16)
		self.gamename.textChanged.connect(self._enableBtn)
		form.addRow('Name of game: ', self.gamename)
		self.playersnum = QSpinBox()
		self.playersnum.setMinimum(2)
		self.playersnum.setMaximum(8)
		form.addRow('Number of players: ', self.playersnum)
		form.setFormAlignment(Qt.AlignCenter)
		return form
	
	def _wait_for_players(self):
		sender = self.sender()
		if isinstance(sender, QPushButton):
			self.next_step.emit(dict(page=constants.JOIN_GAME,
				payload=dict(gamename=self.gamename.text(), 
					playersnum=self.playersnum.value(), username=self.username
				)
			))
	
	def _create_cmd_btn(self):
		self.joingame_btn = QPushButton('Wait for players')
		self.joingame_btn.setEnabled(False)
		self.joingame_btn.clicked.connect(self._wait_for_players)
		layout = QHBoxLayout()
		layout.addStretch(1)
		layout.addWidget(self.joingame_btn)
		return layout
		
	def _initGUI(self):
		self.setWindowTitle('Discard - Create new game')
		
		exit_action = QAction(QIcon('exit.png'), 'Exit', self)
		exit_action.setShortcut('Ctrl+Q')
		exit_action.triggered.connect(self.close)
		
		help_action = QAction(QIcon('help.png'), 'Help', self)
		help_action.setShortcut('Ctrl+H')
		help_action.triggered.connect(self._launch_help_window)
	
		self.toolbar = self.addToolBar('Actions')
		self.toolbar.addAction(help_action)
		self.toolbar.addAction(exit_action)
	
		cmd_btns = self._create_cmd_btn()
		form = self._create_form()
		
		layout = QVBoxLayout()

		layout.addLayout(form)
		layout.addLayout(cmd_btns)
		
		main_widget = QWidget()
		main_widget.setLayout(layout)
		self.setCentralWidget(main_widget)
		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self._center()
		
		self.setMinimumHeight(300)
		self.setMinimumWidth(300)
		# self._show()
		
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NewGamePage()
    sys.exit(app.exec_())
