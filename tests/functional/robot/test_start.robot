*** Settings ***
Resource          software_setup.robot

*** Test Cases ***
Do Nothing
    [Setup]    Start Programs
    No Operation
    [Teardown]    End Programs
