# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s eea.favboard -t test_fav_board_container.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src eea.favboard.testing.EEA_FAVBOARD_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/eea/favboard/tests/robot/test_fav_board_container.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a FavBoard Container
  Given a logged-in site administrator
    and an add FavBoard Container form
   When I type 'My FavBoard Container' into the title field
    and I submit the form
   Then a FavBoard Container with the title 'My FavBoard Container' has been created

Scenario: As a site administrator I can view a FavBoard Container
  Given a logged-in site administrator
    and a FavBoard Container 'My FavBoard Container'
   When I go to the FavBoard Container view
   Then I can see the FavBoard Container title 'My FavBoard Container'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add FavBoard Container form
  Go To  ${PLONE_URL}/++add++FavBoard Container

a FavBoard Container 'My FavBoard Container'
  Create content  type=FavBoard Container  id=my-fav_board_container  title=My FavBoard Container

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the FavBoard Container view
  Go To  ${PLONE_URL}/my-fav_board_container
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a FavBoard Container with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the FavBoard Container title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
