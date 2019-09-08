*** Settings ***
Resource          software_setup.robot

*** Test Cases ***
Do Nothing
    [Setup]    Start Programs
    Start Process    ./arrangeitstart.sh
    Take Screenshot
    [Teardown]    End Programs
