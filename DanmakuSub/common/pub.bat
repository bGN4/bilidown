@ECHO OFF
ECHO %~dp0
ECHO %cd%
SET basedir=D:\home\site\wwwroot\
CD "%basedir%"
ECHO %cd%
:: COPY /Y ..\repository\DanmakuSub\static\favicon.ico .\static\
:: COPY /Y ..\repository\DanmakuSub\static\suit\css\* .\static\suit\css\
MKDIR download
MKDIR queue
CALL env\Scripts\activate.bat
python.exe manage.py bilicomment --mark-expired --output queue
CALL env\Scripts\deactivate.bat
