*** Settings ***
Resource          software_setup.robot
Test Setup       Start Programs
Test Teardown    End Programs

*** Test Cases ***
Quit Arrangeit By Quit Button
    Quit Arrangeit
    Process Should Be Stopped

Show Options Dialog
    Release Cursor
    ${pos} =    Locate Image    "button-options"
    Length Should Be    ${pos}    2
    Left Mouse Press On Position    ${pos}
    ${about} =    Locate Image    "button-about"
    Should Not Be Equal    ${about}    ${None}
    Quit Options Dialog
    Quit Arrangeit

Show About Dialog
    Release Cursor
    ${pos} =    Locate Image    "button-options"
    Length Should Be    ${pos}    2
    Left Mouse Press On Position    ${pos}
    ${about} =    Locate Image    "button-about"
    Left Mouse Press On Position    ${about}
    ${help} =    Locate Image    "button-onlinehelp"
    Should Not Be Equal    ${help}    ${None}
    ${exit} =    Locate Image    "button-exit"
    Should Not Be Equal    ${exit}    ${None}
    Left Mouse Press On Position    ${exit}
    Quit Options Dialog
    Quit Arrangeit