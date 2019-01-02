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


import sys, logging, constants
from PySide2.QtWidgets import (
	QApplication, QDialog
)
from landingpage import LandingPage
from newgamepage import NewGamePage
from modals import Modal
from joingame import JoinGamePage

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('run.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(' - %(name)s - %(levelname)-8s: %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

class App(object):
	
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self.app = QApplication(sys.argv)
		self.landingpage = LandingPage()
		self.newgamepage = NewGamePage()
		self.joinpage = JoinGamePage()
		
		self.landingpage.next_step.connect(self.goToNextPage)
		self.newgamepage.next_step.connect(self.goToNextPage)
		self.joinpage.next_step.connect(self.goToNextPage)
		self.landingpage._show()
	
	def goToNextPage(self, diction):
		self._logger.info('Changing')
		page = diction.get('page')
		if page == constants.NEW_GAME:
			prev = diction.get('previouspage')
			if prev == constants.LANDING_AREA:
				modal = Modal(initial_text='Logging In', final_text='Logged in',
					parent=self.landingpage)
				if modal.exec_() == QDialog.Accepted:
					self.landingpage.hide()
			elif prev == constants.JOIN_GAME:
				self.joinpage.hide()
			self.newgamepage.setUsername(diction.get('payload'))
			self.newgamepage._show()
		elif page == constants.JOIN_GAME:
			if self.newgamepage.isVisible():
				self.newgamepage.hide()
				self.joinpage.set_previous_page(constants.NEW_GAME)
				print('Diction: ', diction)
				self.joinpage.set_username(diction.get('payload').get('username'))
				self.joinpage.insert_game(diction.get('payload').get('gamename'),
					diction.get('payload').get('username'),
					diction.get('payload').get('playersnum')
				)
			else:
				self.joinpage.set_username(diction.get('payload'))
				self.joinpage.set_up_games_players()
			self.joinpage._show()
		elif page == constants.GAME_AREA:
			modal = Modal(initial_text='Initialization', final_text='Finished Initialization',
				parent=self.joinpage)
			if modal.exec_() == QDialog.Accepted:
				self.joinpage.hide()


	def start(self):
		return self.app.exec_()
	
if __name__ == "__main__":
	app = None
	try: 
		app = App()
		ret = app.start()
		sys.exit(ret)
	except NameError:
		logger.debug("Name Error:", sys.exc_info()[1])
	except (SystemExit, KeyboardInterrupt):
		logger.info("Closing Window..")
