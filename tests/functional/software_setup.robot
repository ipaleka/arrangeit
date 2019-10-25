*** Settings ***
Library           Process
Library           arrangeit_keywords.py

*** Keywords ***
Start Programs
    Run Keyword If    sys.platform.startswith('linux')    Start Programs Linux
    ...    ELSE IF    sys.platform.startswith('darwin')    Start Programs Darwin
    ...    ELSE    Start Programs Windows

Start Programs Linux
    Start Process    /usr/bin/inkscape    ./resources/sample.svg
    Start Process    /usr/bin/gimp    ./resources/sample.xcf
    Start Process    /usr/bin/libreoffice    --calc    ./resources/sample.ods    --norestore
    Start Process    /usr/bin/libreoffice    --writer    ./resources/sample.odt    --norestore
    Start Process    /usr/bin/gedit    ./resources/sample.txt
    Sleep    12s
    ${arr_handle} =    Start Process    ./arrangeitstart.sh
    Set Suite Variable    ${arr_handle}
    Sleep    4s

Start Programs Darwin
    Start Process    /usr/bin/inkscape    ./resources/sample.svg
    Start Process    /usr/bin/gimp    ./resources/sample.xcf
    Start Process    /usr/bin/libreoffice    --calc    ./resources/sample.ods    --norestore
    Start Process    /usr/bin/libreoffice    --writer    ./resources/sample.odt    --norestore
    Start Process    /usr/bin/gedit    ./resources/sample.txt
    Sleep    12s
    ${arr_handle} =    Start Process    ./arrangeitstart.sh
    Set Suite Variable    ${arr_handle}
    Sleep    4s

Start Programs Windows
    Start Process    C:\\Program\ Files\\Inkscape\\inkscape.exe    .\\resources\\sample.svg
    Start Process    C:\\Program\ Files\\GIMP\ 2\\bin\\gimp-2.10.exe    .\\resources\\sample.xcf
    Start Process    C:\\Program\ Files\\LibreOffice\\program\\soffice.exe    --calc    .\\resources\\sample.ods    --norestore
    Start Process    C:\\Program\ Files\\LibreOffice\\program\\soffice.exe    --writer    .\\resources\\sample.odt    --norestore
    Start Process    C:\\Program\ Files (x86)\\gedit\\bin\\gedit.exe    .\\resources\\sample.txt
    Sleep    15s
    ${arr_handle} =    Start Process    arrangeitstart.bat
    Set Suite Variable    ${arr_handle}
    Sleep    4s

End Programs
    Terminate All Processes

Quit Arrangeit
    Release Cursor
    Sleep    1s
    ${pos} =    Locate Image    button-quit
    Length Should Be    ${pos}    2
    Left Mouse Click On Position    ${pos}
    Sleep    2s

Quit Options Dialog
    ${continue} =    Locate Image    button-continue
    Should Not Be Equal    ${continue}    ${None}
    Left Mouse Click On Position    ${continue}
    Sleep    2s
