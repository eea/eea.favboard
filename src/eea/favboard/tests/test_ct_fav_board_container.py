# -*- coding: utf-8 -*-
from eea.favboard.content.fav_board_container import IFavBoardContainer  # NOQA E501
from eea.favboard.testing import EEA_FAVBOARD_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


class FavBoardContainerIntegrationTest(unittest.TestCase):

    layer = EEA_FAVBOARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_fav_board_container_schema(self):
        fti = queryUtility(IDexterityFTI, name='FavBoard Container')
        schema = fti.lookupSchema()
        self.assertEqual(IFavBoardContainer, schema)

    def test_ct_fav_board_container_fti(self):
        fti = queryUtility(IDexterityFTI, name='FavBoard Container')
        self.assertTrue(fti)

    def test_ct_fav_board_container_factory(self):
        fti = queryUtility(IDexterityFTI, name='FavBoard Container')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IFavBoardContainer.providedBy(obj),
            u'IFavBoardContainer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_fav_board_container_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='FavBoard Container',
            id='fav_board_container',
        )

        self.assertTrue(
            IFavBoardContainer.providedBy(obj),
            u'IFavBoardContainer not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('fav_board_container', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('fav_board_container', parent.objectIds())

    def test_ct_fav_board_container_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='FavBoard Container')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_fav_board_container_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='FavBoard Container')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'fav_board_container_id',
            title='FavBoard Container container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
