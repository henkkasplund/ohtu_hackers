*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Application

*** Test Cases ***
Inproceedings Reference Can Be Submitted
    Add Inproceedings Reference
    Get Url  ==  ${HOME_URL}/

    Get Text  tbody tr  *=  VPL11
    Get Text  tbody tr  *=  Konferenssiviite
    Get Text  tbody tr  *=  SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education

    Click  text=VPL11
    Get Title  ==  Viitteen tiedot
    Get Text  pre  *=  @inproceedings{VPL11,
    Get Text  pre  *=  year = {2011}
    Get Text  pre  *=  booktitle = {SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education}

Inproceedings Reference Can Be Edited
    Add Tag    Other
    Add Inproceedings Reference
    Click  text=VPL11
    Click  button >> text=Muokkaa

    Select Options By  id=tag_name  label  Other
    Fill Text  id=booktitle  SIGCSE '11
    Click  button >> text=Muokkaa konferenssiviite

    Get Title  ==  Viitteen tiedot
    Get Text  pre  *=  @inproceedings{VPL11,
    Get Text  pre  *=  booktitle = {SIGCSE '11}
    Go To  ${HOME_URL}
    Get Text  tbody tr  *=  Other

*** Keywords ***
Add Inproceedings Reference
    Go To  ${HOME_URL}/add_reference
    Select Options By  id=reference_type_name  label  Konferenssiviite
    Click  button >> text=Valitse

    Fill Text  id=citation_key  VPL11
    Select Options By  id=tag_name  label  Gradu
    Fill Text  id=author  Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti
    Fill Text  id=title  Extreme Apprenticeship Method in Teaching Programming for Beginners.
    Fill Text  id=year  2011
    Fill Text  id=booktitle  SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education

    Click  button >> text=Tallenna konferenssiviite
