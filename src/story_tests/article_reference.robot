*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
Article Reference Can Be Submitted
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Artikkeli
    Click  button >> text=Valitse

    Fill Text  id=citation_key  CBH91
    Fill Text  id=author  Allan Collins and John Seely Brown and Ann Holum
    Fill Text  id=title  Cognitive apprenticeship: making thinking visible
    Fill Text  id=journal  American Educator
    Fill Text  id=year  1991
    Fill Text  id=volume  6
    Fill Text  id=pages  38--46

    Click  button >> text=Tallenna artikkeli
    Get Url  ==  ${HOME_URL}/

    Get Text  tbody tr  *=  American Educator
    Get Text  tbody tr td:nth-child(7)  ==  6
    Get Text  tbody tr  *=  38--46
    Get Text  tbody tr  *=  CBH91
    Get Text  tbody tr  *=  Cognitive apprenticeship: making thinking visible
    Get Text  tbody tr  *=  Artikkeli

    Click  text=CBH91
    Get Text  tbody tr  *=  American Educator
    Get Text  pre  *=  @article{CBH91,
    Get Text  pre  *=  volume = {6}
    Get Text  pre  *=  pages = {38--46}

Article Reference Can Be Submitted Without Optional Fields
    Add Article Reference
    Get Url  ==  ${HOME_URL}/
    Get Text  tbody tr  *=  CBH91

    Click  text=CBH91
    Get Text  tbody tr  *=  American Educator

    ${bibtex}=  Get Text  pre
    Should Not Contain  ${bibtex}  volume =
    Should Not Contain  ${bibtex}  pages =

Article Reference Can Be Edited
    Add Article Reference
    Click  text=CBH91
    Click  button >> text=Muokkaa

    Fill Text  id=volume  6
    Fill Text  id=pages  38--46

    Click  button >> text=Muokkaa artikkeli
    Get Title  ==  Viitteen tiedot
    Get Text  pre  *=  volume = {6}
    Get Text  pre  *=  pages = {38--46}

*** Keywords ***
Add Article Reference
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Artikkeli
    Click  button >> text=Valitse

    Fill Text  id=citation_key  CBH91
    Fill Text  id=author  Allan Collins and John Seely Brown and Ann Holum
    Fill Text  id=title  Cognitive apprenticeship: making thinking visible
    Fill Text  id=journal  American Educator
    Fill Text  id=year  1991

    Click  button >> text=Tallenna artikkeli