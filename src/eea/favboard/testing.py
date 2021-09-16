# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import eea.favboard


class EeaFavboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=eea.favboard)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'eea.favboard:default')


EEA_FAVBOARD_FIXTURE = EeaFavboardLayer()


EEA_FAVBOARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_FAVBOARD_FIXTURE,),
    name='EeaFavboardLayer:IntegrationTesting',
)


EEA_FAVBOARD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_FAVBOARD_FIXTURE,),
    name='EeaFavboardLayer:FunctionalTesting',
)


EEA_FAVBOARD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EEA_FAVBOARD_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EeaFavboardLayer:AcceptanceTesting',
)
