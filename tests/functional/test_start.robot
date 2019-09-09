*** Settings ***
Resource          software_setup.robot

*** Test Cases ***
Do Nothing
    [Setup]    Start Programs
    Sleep    45s
    Start Process    ./arrangeitstart.sh
    Sleep    10s
    Take Screenshot
    [Teardown]    End Programs
