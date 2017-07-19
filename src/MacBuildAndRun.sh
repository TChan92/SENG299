#!/bin/bash
osascript -e 'tell application "Terminal" to activate' 
osascript -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' 
osascript -e 'tell application "Terminal" to do script "python /Users/academia/Desktop/peanut/src/IMServer.py" in selected tab of the front window'
for VARIABLE in {1..2}
	do
		osascript -e 'tell application "Terminal" to activate' 
		osascript -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' 
		osascript -e 'tell application "Terminal" to do script "python /Users/academia/Desktop/peanut/src/IMClient.py" in selected tab of the front window'
	done

