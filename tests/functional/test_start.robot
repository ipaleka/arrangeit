*** Settings ***
Resource          software_setup.robot

*** Test Cases ***
Do Nothing
    [Setup]    Start Programs
    Sleep    20s
    Start Process    ./arrangeitstart.sh
    Sleep    5s
    Take Screenshot
    [Teardown]    End Programs
