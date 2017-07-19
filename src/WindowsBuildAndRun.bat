@ECHO off

ECHO Run the IMServer
start python "C:\Users\Clami\OneDrive\University\SENG 299\SENG299\src\IMServer.py"

ECHO Run the IMClient
REM start,step,end
REM change 20 to 1000 when testing with many clients
FOR /L %%i IN (1, 1, 2) DO (
	start python "C:\Users\Clami\OneDrive\University\SENG 299\SENG299\src\IMClient.py"
)

