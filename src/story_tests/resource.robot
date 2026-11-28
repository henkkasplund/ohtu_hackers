*** Settings ***
Library  Browser

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Reset Application
    Go To  ${RESET_URL}
    Get Text  body  *=  db reset
    Add Tag    Gradu

Add Tag
    [Arguments]    ${tag_name}
    Go To    ${HOME_URL}/add_reference
    Fill Text    input#new_tag_name    ${tag_name}
    Click    button >> text=Lisää tagi