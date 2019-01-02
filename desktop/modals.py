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

import logging

from PySide2.QtWidgets import (
	QHBoxLayout,QDialog, QLabel,
	QPushButton, QVBoxLayout
)
from PySide2.QtCore import QTimer
from PySide2.QtGui import QMovie


class Modal(QDialog):

    def __init__(self, initial_text='', final_text='', parent=None):
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self.step, self.maxRuns = 0, 10
        layout = QVBoxLayout()

        inner_layout = QHBoxLayout()
        icon_container = QLabel()
        self.loading_icon = QMovie('ajax-loader.gif')
        icon_container.setMovie(self.loading_icon)
        self.status_label = QLabel(initial_text)
        inner_layout.addWidget(icon_container)
        inner_layout.addWidget(self.status_label)
        self.ok_button = QPushButton('OK')
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.submit_and_close)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.event_on_timeout)
        self.final_text = final_text

        layout.addLayout(inner_layout)
        layout.addWidget(self.ok_button)
        icon_container.show()
        self.loading_icon.start()
        self.setLayout(layout)
        self._logger.info('Showing modal')
        self.timer.start(2000)

    def event_on_timeout(self):
        self._logger.info('Timeout at step ' + str(self.step))
        if self.step >= self.maxRuns:
            self.timer.stop()
            self.status_label.setText(self.final_text)
            self.ok_button.setEnabled(True)
            self.loading_icon.stop()
            self.timer = None
            return
        self.step += 1

    def submit_and_close(self):
        self.accept()
