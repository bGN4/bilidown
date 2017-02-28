@ECHO OFF
SET basedir=D:\home\site\wwwroot\
CD "%basedir%"
ECHO %cd%
MKDIR download
MKDIR queue
CALL env\Scripts\activate.bat
python.exe manage.py bilicomment --mark-expired --output queue debug-task.txt
CALL env\Scripts\deactivate.bat
