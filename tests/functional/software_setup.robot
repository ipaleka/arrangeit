*** Settings ***
Library           Process
Library           arrangeit_keywords.py

*** Keywords ***
Start Programs
    Start Process    /usr/bin/inkscape    ./resources/sample.svg
    Start Process    /usr/bin/gimp    ./resources/sample.xcf
    Start Process    /usr/bin/libreoffice    --calc    ./resources/sample.ods    --norestore
    Start Process    /usr/bin/libreoffice    --writer    ./resources/sample.odt    --norestore
    Start Process    /usr/bin/gedit    ./resources/sample.txt
    Sleep    8s
    ${arr_handle} =    Start Process    ./arrangeitstart.sh
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
