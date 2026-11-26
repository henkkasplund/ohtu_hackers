*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
Navbar Links Open Correct Pages
    Go To  ${HOME_URL}
    Click  nav >> text=Lisää viite
    Get Url  ==  ${HOME_URL}/add_reference
    Click  nav >> text=Viiteluettelo
    Get Title  ==  Viiteluettelo
