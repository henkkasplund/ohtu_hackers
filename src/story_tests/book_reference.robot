*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
Book Reference Can Be Submitted
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=style  label  Kirja
    Click  button >> text=Valitse

    Fill Text  id=citation_key  Martin09
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  Clean Code
    Fill Text  id=year  2008
    Fill Text  id=publisher  Prentice Hall

    Click  button >> text=Tallenna kirja
    Get Url  ==  ${HOME_URL}/

Book Reference With Blank Title Is Rejected
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=style  label  Kirja
    Click  button >> text=Valitse

    Fill Text  id=citation_key  Martin09
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  ${SPACE}
    Fill Text  id=year  2008
    Fill Text  id=publisher  Prentice Hall

    Click  button >> text=Tallenna kirja
    Get Text  body  *=  Kaikki kirjan kentät ovat pakollisia!

Book Reference With Zero Year Is Rejected
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=style  label  Kirja
    Click  button >> text=Valitse

    Fill Text  id=citation_key  Martin09
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  Clean Code
    Fill Text  id=year  0000
    Fill Text  id=publisher  Prentice Hall

    Click  button >> text=Tallenna kirja
    Get Text  body  *=  Vuoden täytyy olla kokonaisluku väliltä
