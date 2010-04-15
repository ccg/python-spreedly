# -*- coding: utf-8 -*-
import unittest

from api import Client

SPREEDLY_AUTH_TOKEN = '59f064f450af88df24f54281f3d78ad8ee0eb8f0'
SPREEDLY_SITE_NAME = 'shelfworthytest'


class TestCase(unittest.TestCase):
    subscriber_keys = set([
        'active', 'active_until', 'card_expires_before_next_auto_renew',
        'created_at', 'customer_id', 'date_changed', 'email', 'first_name',
        'feature_level', 'gift', 'last_name', 'lifetime', 'name', 'recurring',
        'screen_name', 'token', 'trial_active', 'trial_eligible', #'plan',
    ])

    def setUp(self):
        self.sclient = Client(SPREEDLY_AUTH_TOKEN, SPREEDLY_SITE_NAME)

        # Remove all subscribers
        self.sclient.cleanup()

    def tearDown(self):
        # Remove all subscribers
        self.sclient.cleanup()

    def test_get_plans(self):
        keys = set([
            'date_changed', 'terms', 'name', 'force_recurring', 'feature_level',
            'price', 'enabled', 'plan_type', 'force_renew', 'duration_units',
            'version', 'spreedly_site_id', 'duration', 'created_at',
            'spreedly_id', 'return_url', 'description'
        ])

        for plan in self.sclient.get_plans():
            self.assertEquals(set(plan.keys()), keys)

    def test_create_subscriber(self):
        subscriber = self.sclient.create_subscriber(1, 'test')
        self.assertEquals(set(subscriber.keys()), self.subscriber_keys)

        # Delete subscriber
        self.sclient.delete_subscriber(1)

    def test_subscribe(self):
        # Create a subscriber first
        subscriber = self.sclient.create_subscriber(1, 'test')

        # Subscribe to a free trial
        subscription = self.sclient.subscribe(1, 1824, True)
        self.assertEquals(set(subscriber.keys()), self.subscriber_keys)
        assert subscription['trial_active']

        # Delete subscriber
        #self.sclient.delete_subscriber(1)

    def test_delete_subscriber(self):
        self.sclient.create_subscriber(1, 'test')
        self.failUnlessEqual(self.sclient.delete_subscriber(1), 200)

    def test_get_info(self):
        self.sclient.create_subscriber(1, 'test')
        subscriber = self.sclient.get_info(1)
        self.assertEquals(set(subscriber.keys()), self.subscriber_keys)
        self.assertEquals(subscriber['email'], '')
        self.assertEquals(subscriber['screen_name'], 'test')

        self.sclient.set_info(1, email='jack@bauer.com', screen_name='jb')
        subscriber = self.sclient.get_info(1)
        self.assertEquals(subscriber['email'], 'jack@bauer.com')
        self.assertEquals(subscriber['screen_name'], 'jb')

    def test_get_or_create(self):
        #test non existent subscriber
        result = self.sclient.get_or_create_subscriber(123, 'tester')
        self.assertEquals(set(result.keys()), self.subscriber_keys)

        #assure that we won't overwrite existing subscriber
        result2 = self.sclient.get_or_create_subscriber(123, 'tester2')
        self.assertEquals(result, result2)

    def test_comp_subscription(self):
        result = self.sclient.get_or_create_subscriber(123, 'tester')

        self.sclient.create_complimentary_subscription(123, 2, 'months', 'Pro')


if __name__ == '__main__':
    unittest.main()

