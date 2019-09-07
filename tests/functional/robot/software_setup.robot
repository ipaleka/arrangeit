*** Settings ***
Library           Process
Library           arrangeit_keywords.py

*** Keywords ***
Start Programs
    Start Process    /usr/bin/inkscape    ./resources/sample.svg
    Start Process    /usr/bin/gimp    ./resources/sample.xcf
    Start Process    /usr/bin/libreoffice    --calc    ./resources/sample.ods
    Start Process    /usr/bin/libreoffice    --writer    ./resources/sample.odt

End Programs
    Terminate All Processes
