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
import json
import logging
import constants

from PySide2.QtWidgets import (
	QApplication, QLabel, QWidget, QMainWindow,
	QCheckBox, QGroupBox, QLineEdit,
	QButtonGroup, QRadioButton, QFormLayout,
	QHBoxLayout, QPushButton, QVBoxLayout, QDesktopWidget,
)
from PySide2.QtCore import (
	Signal, Qt
)
from PySide2.QtGui import QFont


class LandingPage(QMainWindow):
	
	next_step = Signal(dict)

	def __init__(self):
		super().__init__()
		self._logger = logging.getLogger(__name__)
		self.user_type, self.username, self.password = '', '', ''
		self._initUI()
		
	def _setUserType(self):
		sender = self.sender()
		if isinstance(sender, QRadioButton):
			self.user_type = sender.text()
			self._logger.info(self.user_type)
			if isinstance(self.password, QLineEdit):
				self.password.clear()
			if isinstance(self.username, QLineEdit):
				self.username.clear()
			self.repaint()
				
	def _enableBtn(self):
		if all([len(self.password.text()) >= 8, 
			len(self.username.text()) >= 5]):
			self._logger.info('ERFR')
			self.newgame_btn.setEnabled(True)
			self.joingame_btn.setEnabled(True)
		else:
			self.newgame_btn.setEnabled(False)
			self.joingame_btn.setEnabled(False)
	
	def _create_user(self):
		sender = self.sender()
		if isinstance(sender, QPushButton):
			self._logger.info('Calling create game for the api')
			if sender.text().lower() == 'new game':
				self.next_step.emit(dict(page=constants.NEW_GAME,
					previouspage=constants.LANDING_AREA,
					payload=self.username.text()))
			elif sender.text().lower() == 'join game':
				self.next_step.emit(dict(page=constants.JOIN_GAME,
					previouspage=constants.LANDING_AREA,
					payload=self.username.text()))

	# Layouts
	def _create_btn_grp(self):
		box = QGroupBox()
		layout = QHBoxLayout()
		btn_types = QButtonGroup()
		
		anon_user = QRadioButton('Anonymous User', self)
		anon_user.toggled.connect(self._setUserType)
		returning_user = QRadioButton('Returning User', self)
		returning_user.toggled.connect(self._setUserType)
		new_user = QRadioButton('New User', self)
		new_user.toggled.connect(self._setUserType)
		new_user.setChecked(True)
		
		btn_types.addButton(anon_user)
		btn_types.addButton(returning_user)
		btn_types.addButton(new_user)
		layout.addWidget(anon_user)
		layout.addWidget(returning_user)
		layout.addWidget(new_user)
		
		box.setLayout(layout)
		return box
	
	def _create_form(self):
		form = QFormLayout()
		self.username = QLineEdit()
		self.username.setMaxLength(16)
		self.username.textChanged.connect(self._enableBtn)
		form.addRow('Username: ', self.username)
		self.password = QLineEdit()
		self.password.setEchoMode(QLineEdit.Password)
		self.password.setMaxLength(16)
		self.password.textChanged.connect(self._enableBtn)
		form.addRow('Password: ', self.password)
		checkbox = QCheckBox('Show Password')
		checkbox.setChecked(False)
		checkbox.stateChanged.connect(
			lambda state: self.password.setEchoMode(QLineEdit.Normal if bool(state) else QLineEdit.Password))
		form.addRow('', checkbox)
		return form
	
	def _create_cmd_btns(self):
		layout = QHBoxLayout()
		
		self.newgame_btn = QPushButton('New Game')
		self.newgame_btn.clicked.connect(self._create_user)
		self.newgame_btn.setEnabled(False)
		self.joingame_btn = QPushButton('Join Game')
		self.joingame_btn.clicked.connect(self._create_user)
		self.joingame_btn.setEnabled(False)
		exit_btn = QPushButton('Exit')
		exit_btn.clicked.connect(self.close)
		
		layout.addWidget(exit_btn)
		layout.addWidget(self.newgame_btn)
		layout.addWidget(self.joingame_btn)
		
		return layout
	
	def _center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	def _show(self):
		self.show()
		self._logger.info('Starting landingpage window')	
		
	def _initUI(self):
		self.setWindowTitle('Discard Game - Login')
		title_label = QLabel('Discard')
		title_label.setFont(QFont('Times New Roman', 30))
		title_label.setAlignment(Qt.AlignCenter)
		title_label.setStyleSheet('QLabel { background-color : green; color : black;}')
		
		cmd_btns = self._create_cmd_btns()
		user_types = self._create_btn_grp()
		info_label = QLabel('Username >= 5 characters and Password >= 8 characters')
		info_label.setAlignment(Qt.AlignCenter)
		form = self._create_form()
		
		layout = QVBoxLayout()
		layout.addWidget(title_label)
		layout.addWidget(user_types)
		layout.addWidget(info_label)
		layout.addLayout(form)
		layout.addLayout(cmd_btns)
		
		main_widget = QWidget()
		main_widget.setLayout(layout)
		self.setCentralWidget(main_widget)

		self.setAttribute(Qt.WA_DeleteOnClose)
		
		self._center()
		
		self.setMinimumHeight(400)
		self.setMinimumWidth(400)
		
		#self._show()
		
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LandingPage()
    sys.exit(app.exec_())
