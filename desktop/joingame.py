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

from collections import namedtuple
from PySide2.QtWidgets import (
	QApplication, QLabel, QWidget, QMainWindow,
    QListWidget, QAbstractItemView, QMessageBox,
	QHBoxLayout, QPushButton, QVBoxLayout, QDesktopWidget,
)
from PySide2.QtCore import (
	Signal, Qt
)

GameInfo = namedtuple('GameInfo','players max_player_num')

class JoinGamePage(QMainWindow):

    next_step = Signal(dict)

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._games_players = {}
        # self._username = 'Mine'
        # self._set_up_games_players()
        self._previous_page = ''

    def insert_game(self, game, username, max_players):
        self._games_players.update({game:GameInfo(players=[username],
            max_player_num=max_players)})
        print('Games_players: ', self._games_players)

    def set_previous_page(self, page):
        self._previous_page = page

    def _return_listWidget(self, layout):
        for cnt in range(layout.count()):
            item = layout.itemAt(cnt)
            if isinstance(item.wid, QListWidget):
                return item.wid

    def _return_listwidget_data(self, widget):
        return [widget.item(cnt).text() for cnt in range(widget.count())]

    def _add_player_to_game_extern(self):
        # for updating the list from external sources
        pass

    def _add_game_extern(self):
        # for updating the list from external sources
        pass

    def _add_player_to_game(self):
        plistWidget = self._return_listWidget(self.players_layout)
        if self._username not in self._return_listwidget_data(plistWidget):
            plistWidget.addItem(self._username)
        glistWidget = self._return_listWidget(self.games_layout)
        currentItem = glistWidget.currentItem().text()
        for key, value in self._games_players.items():
            if key == currentItem:
                if self._username not in value.players:
                    value.players.append(self._username)
                    self.join_btn.setEnabled(True)
                    self._swap_btn_states()

    def _swap_btn_states(self):
        if self._add_to_game_btn.isEnabled():
            self._remove_from_game_btn.setEnabled(True)
            self._add_to_game_btn.setEnabled(False)
        else:
            self._remove_from_game_btn.setEnabled(False)
            self._add_to_game_btn.setEnabled(True)

    def _remove_player_from_game(self):
        plistWidget = self._return_listWidget(self.players_layout)
        for cnt in range(plistWidget.count()):
            item = plistWidget.item(cnt).text()
            if item == self._username:
                plistWidget.takeItem(cnt)
                break
        glistWidget = self._return_listWidget(self.games_layout)
        currentItem = glistWidget.currentItem().text()
        for key, value in self._games_players.items():
            if key == currentItem:
                if self._username in value.players:
                    value.players.remove(self._username)
                    self.join_btn.setEnabled(False)
                    self._swap_btn_states()

    def set_up_games_players(self):
        self._games_players = dict(
            GameA=GameInfo(players=['Player1', 'Player2', 'Player3'], max_player_num=4),
            GameB=GameInfo(players=['Player4', 'Player5'], max_player_num=3),
        )

    def _change_players_pane(self,data):
        itemlist = self._games_players.get(data.text()).players
        listWidget = self._return_listWidget(self.players_layout)
        listWidget.clear()
        for datum in itemlist:
            listWidget.addItem(datum)
        self.repaint()

    def set_username(self, username):
        self._username = username

    def _move_to_next_page(self):
        listWidget = self._return_listWidget(self.players_layout)
        if self._username in self._return_listwidget_data(listWidget):
            message = QMessageBox()
            message.setIcon(QMessageBox.Question)
            message.setText('Do you want to continue with this configuration or not?')

            wait_for_game_btn = message.addButton(QMessageBox.Apply)
            _ = message.addButton(QMessageBox.Abort)

            message.setDefaultButton(wait_for_game_btn)
            message.exec_()

            if message.clickedButton() == wait_for_game_btn:
                self.next_step.emit(dict(page=constants.GAME_AREA,
                    previouspage=constants.JOIN_GAME,
                    payload=dict(
                        gamename=self._return_listWidget(self.games_layout).currentItem(),
                        players=self._return_listwidget_data(listWidget)
                    )
                ))
            else:
                if self._previous_page:
                    self.next_step.emit(dict(page=constants.NEW_GAME,
                        previouspage=constants.JOIN_GAME,
                        payload=self._username
                    ))
                return


    #Layouts
    def _create_pane(self, title, itemdict, use_keys=True, cb=None):
        layout = QVBoxLayout()
        label = QLabel(title)
        view = QListWidget()
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        itemlist = []
        if len(itemdict) > 0:
            if use_keys:
                itemlist = list(itemdict.keys())
            else:
                itemlist = itemdict.get(list(itemdict.keys())[0]).players
        for item in itemlist:
            view.addItem(item)
        if cb:
            view.itemClicked.connect(cb)
        layout.addWidget(label)
        layout.addWidget(view)
        return layout

    def _create_middle_cmds(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self._add_to_game_btn = QPushButton('>>')
        self._add_to_game_btn.clicked.connect(self._add_player_to_game)
        self._remove_from_game_btn = QPushButton('<<')
        self._remove_from_game_btn.clicked.connect(self._remove_player_from_game)
        if self._previous_page == constants.NEW_GAME:
            self._add_to_game_btn.setEnabled(False)
        else:
            self._remove_from_game_btn.setEnabled(False)
        layout.addWidget(self._add_to_game_btn)
        layout.addWidget(self._remove_from_game_btn)
        return layout

    def _create_main_cmd(self):
        layout = QHBoxLayout()
        layout.addStretch(1)
        self.join_btn = QPushButton('Wait for players')
        if self._previous_page != constants.NEW_GAME:
            self.join_btn.setEnabled(False)
        self.join_btn.clicked.connect(self._move_to_next_page)
        layout.addWidget(self.join_btn)
        return layout

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _show(self):
        self._initUI()
        self.show()
        self._logger.info('Starting joingamepage window')

    def _initUI(self):
        self.setWindowTitle('Discard - Player Lobby')
        layout = QVBoxLayout()

        inner_layout = QHBoxLayout()
        self.players_layout = self._create_pane('Players', self._games_players, use_keys=False)
        self.games_layout = self._create_pane('Games', self._games_players, cb=self._change_players_pane)
        middle_layout = self._create_middle_cmds()
        inner_layout.addLayout(self.games_layout)
        inner_layout.addLayout(middle_layout)
        inner_layout.addLayout(self.players_layout)
        cmd_btn_layout = self._create_main_cmd()

        layout.addLayout(inner_layout)
        layout.addLayout(cmd_btn_layout)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._center()

        self.setMinimumHeight(500)
        self.setMinimumWidth(500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = JoinGamePage()
    sys.exit(app.exec_())
