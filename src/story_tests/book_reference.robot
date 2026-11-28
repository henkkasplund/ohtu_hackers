*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application
Library          OperatingSystem

*** Test Cases ***
Book Reference Can Be Submitted
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Kirja
    Click  button >> text=Valitse

    Fill Text  id=citation_key  Martin09
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  Clean Code
    Fill Text  id=year  2008
    Fill Text  id=publisher  Prentice Hall

    Click  button >> text=Tallenna kirja
    Get Url  ==  ${HOME_URL}/

    Go To  ${HOME_URL}
    Get Title  ==  Viiteluettelo
    Get Text  tbody tr  *=  Martin09
    Get Text  tbody tr  *=  Robert Martin
    Get Text  tbody tr  *=  Clean Code
    Get Text  tbody tr  *=  2008
    Get Text  tbody tr  *=  Prentice Hall
    Get Text  tbody tr  *=  Kirja

Book Reference With Blank Title Is Rejected
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Kirja
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
    Select Options By  id=reference_type_name  label  Kirja
    Click  button >> text=Valitse

    Fill Text  id=citation_key  Martin09
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  Clean Code
    Fill Text  id=year  0000
    Fill Text  id=publisher  Prentice Hall

    Click  button >> text=Tallenna kirja
    Get Text  body  *=  Vuoden täytyy olla kokonaisluku väliltä

Book Reference With Existing Key Is Rejected
    Add Book Reference  Martin09  Clean Code
    Get Url  ==  ${HOME_URL}/

    Add Book Reference  Martin09  Toinen kirja
    Get Text  body  *=  Viiteavain 'Martin09' on jo käytössä!

    Go To  ${HOME_URL}
    Get Element Count  tbody tr  ==  1
    Get Text  tbody tr  *=  Martin09
    Get Text  tbody tr  *=  Clean Code

Front Page Shows Message When No References
    Go To  ${HOME_URL}
    Get Title  ==  Viiteluettelo
    Get Text  body  *=  Ei tallennettuja viitteitä.

Book Reference Page Shows BibTeX
    Add Book Reference  Martin09  Clean Code

    Go To  ${HOME_URL}
    Click  text=Martin09

    Get Text  pre  *=  @book{Martin09,
    Get Text  pre  *=  author = {Robert Martin}
    Get Text  pre  *=  title = {Clean Code}
    Get Text  pre  *=  year = {2008}
    Get Text  pre  *=  publisher = {Prentice Hall}

Book Reference Can Be Deleted
    Add Book Reference  Martin09  Clean Code
    Add Book Reference  Martin06  Clean Architecture

    Go To  ${HOME_URL}
    Get Element Count  tbody tr  ==  2
    Click  text=Martin09

    Click  button >> text=Poista
    Get Title  ==  Vahvista poisto
    Get Text  body  *=  Martin09

    Click  button >> text=Poista viite
    Get Url  ==  ${HOME_URL}/

    Get Element Count  tbody tr  ==  1
    Get Text  tbody tr  *=  Martin06

Cancelling Book Reference Deletion Keeps Reference
    Add Book Reference  Martin09  Clean Code

    Go To  ${HOME_URL}
    Click  text=Martin09

    Click  button >> text=Poista
    Get Title  ==  Vahvista poisto

    Click  text=Peruuta
    Get Title  ==  Viitteen tiedot

    Go To  ${HOME_URL}
    Get Element Count  tbody tr  ==  1
    Get Text  tbody tr  *=  Martin09
    Get Text  tbody tr  *=  Clean Code

BibTeX File Contains Saved References
    Add Book Reference  Martin09  Clean Code

    ${file}=  Download  ${HOME_URL}/download/references.bib
    ${content}=  Get File  ${file}[saveAs]
    Should Contain  ${content}  @book{Martin09,
    Should Contain  ${content}  title = {Clean Code}

Long Title Is Truncated In Reference List
    Add Book Reference  Martin09  Clean Code: A Handbook of Agile Software Craftsmanship
    Go To  ${HOME_URL}
    Get Text  tbody tr  *=  ...
    Get Attribute  td[title^="Clean Code: A Handbook"]  title  ==  Clean Code: A Handbook of Agile Software Craftsmanship

*** Keywords ***
Add Book Reference
    [Arguments]  ${key}  ${title}
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Kirja
    Click  button >> text=Valitse
    Fill Text  id=citation_key  ${key}
    Fill Text  id=author  Robert Martin
    Fill Text  id=title  ${title}
    Fill Text  id=year  2008
    Fill Text  id=publisher  Prentice Hall
    Click  button >> text=Tallenna kirja

