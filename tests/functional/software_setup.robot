*** Settings ***
Library           Process
Library           arrangeit_keywords.py

*** Keywords ***
Start Programs
    Start Process    /usr/bin/inkscape    ./resources/sample.svg
    Start Process    /usr/bin/gimp    ./resources/sample.xcf
    Start Process    /usr/bin/libreoffice    --calc    ./resources/sample.ods    --norestore
    Start Process    /usr/bin/libreoffice    --writer    ./resources/sample.odt    --norestore
    # Start Process    /usr/bin/thunar    .
    Sleep    8s
    Start Process    ./arrangeitstart.sh
    Sleep    4s

End Programs
    Terminate All Processes

Quit Arrangeit
    Release Cursor
    ${pos} =    Locate Image    button-quit
    Length Should Be    ${pos}    2
    Left Mouse Press On Position    ${pos}

Quit Options Dialog
    ${continue} =    Locate Image    button-continue
    Should Not Be Equal    ${continue}    ${None}
    Left Mouse Press On Position    ${continue}
