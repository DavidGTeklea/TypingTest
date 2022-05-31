import curses
# wrapper allows curses module to take over terminal
from curses import wrapper
# to keep track of wpm
import time
import history
# to get random lines of green eggs and ham
import random



def start_screen(stdscr):
	# clears the terminal screen
	stdscr.clear()
	stdscr.addstr("Welcome to David's Typing Test!")
	stdscr.addstr("\nPress any letter key to begin!")



	# refreshes the terminal screen
	stdscr.refresh()
	stdscr.getkey()




# wpm is an optional parameters, setting the default to 0
def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	# allows you to display wpm increase through python f string
	stdscr.addstr(1, 0, F"WPM: {wpm}")


	# allows you to place colored characters on top of normal characters
	for i, char in enumerate(current):
		correct_char = target[i]

		# overlays character with yellow
		color = curses.color_pair(1)

		# overlays character with red if it's incorrect
		if char != correct_char:
			color = curses.color_pair(2)

		# starts from char 0, i increments to char 1,2,3...
		stdscr.addstr(0, i, char, color)

# opens text.txt and loads random lines for typing test
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		# .strip() removes the \n that comes implicitly
		# with every line in text.txt because that's how
		# the editor reads the text
		return random.choice(lines).strip()

def wpm_test(stdscr):
	# load in Green Eggs and Ham as the target text
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	# do not delay waiting for user to enter a key, so wpm
	# can decrease when there's no keyboard movement
	stdscr.nodelay(True)


	# every time user types a character, it overlays the target text
	while True:
		# tells you how many seconds has elapsed
		# max function prevents zero integer division errors
		time_elapsed = max(time.time() - start_time, 1)

		# assuming avg word has 5 characters, this translates
		# characters per minute to words per minute, and the
		# round function prevents any decimals
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		# every time loop runs, the screen gets cleared
		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)

		# refresh the screen so you can see the results of display_text function
		stdscr.refresh()

		# converts the current_text list into a string
		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		# this try and excepts prevents stdscr.nodelay from crashing
		# the program
		try:

			key = stdscr.getkey()
		except:
			continue

		# any key that has an ASCII = 27, which is the escape keu
		# since arrow keys has no ASCII values, this also exits program

		if ord(key) == 27:
			break

		# allows backspace to actually delete characters, not just
		# bring the cursor back

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:

				# does the actual deletion from the list
				current_text.pop()

		# makes user stop from adding more characters than the target text
		elif len(current_text) < len(target_text):
			current_text.append(key)



# writes to screen
def main(stdscr):
	# allows you to wrap text with yellow background, black foreground
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	# allows you to wrap text with red background, black foreground
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

	# lets you to wrap text with white background, black background
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	# initalize characters, then call screen function
	start_screen(stdscr)




	# allows user to keep playing again if desired
	while True:

		wpm_test(stdscr)

		game_counter = "Games played: " + str(history.counter)

		# Two lines down at the 0th character, it outputs this text
		stdscr.addstr(2, 0, game_counter)

		stdscr.addstr(3, 0, "You completed the text! Press the enter key to continue...")

		key = stdscr.getkey()

		if ord(key) == 27:
			break

		once = 0
		if once == 0:
			history.counter += 1

			once = 1








# calls function
wrapper(main)
