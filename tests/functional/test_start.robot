*** Settings ***
Resource          software_setup.robot
Test Setup       Start Programs
Test Teardown    End Programs

*** Test Cases ***
Quit Arrangeit By Quit Button
    Quit Arrangeit
    Process Should Be Stopped    handle=${arr_handle}

Show Options Dialog
    Release Cursor
    Sleep    1s
    ${pos} =    Locate Image    button-options
    Length Should Be    ${pos}    2
    Left Mouse Click On Position    ${pos}
    Sleep    2s
    ${about} =    Locate Image    button-about
    Should Not Be Equal    ${about}    ${None}
    Quit Options Dialog
    Quit Arrangeit

Show About Dialog
    Release Cursor
    Sleep    1s
    ${pos} =    Locate Image    button-options
    Length Should Be    ${pos}    2
    Left Mouse Click On Position    ${pos}
    Sleep    2s
    ${about} =    Locate Image    button-about
    Left Mouse Click On Position    ${about}
    Sleep    2s
    ${help} =    Locate Image    button-onlinehelp
    Should Not Be Equal    ${help}    ${None}
    ${exit} =    Locate Image    button-exit
    Should Not Be Equal    ${exit}    ${None}
    Left Mouse Click On Position    ${exit}
    Sleep    2s
    Quit Options Dialog
    Quit Arrangeit
