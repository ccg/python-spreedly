# -*- coding: utf-8 -*-
import unittest

from api import Client

SPREEDLY_AUTH_TOKEN = '8cd66e5116f83c800d6fe4292c832ed7cdd3db37'
SPREEDLY_SITE_NAME = 'pybrew-pyspreedly-test'


class TestCase(unittest.TestCase):
    subscriber_keys = set([
        'active', 'active_until', 'card_expires_before_next_auto_renew',
        'created_at', 'customer_id', 'date_changed', 'email', 'first_name',
        'feature_level', 'gift', 'last_name', 'lifetime', 'name', 'recurring',
        'screen_name', 'token', 'trial_active', 'trial_eligible', #'plan',
    ])
    plans = []

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
            self.plans.append(plan)

    def test_create_subscriber(self):
        subscriber = self.sclient.create_subscriber(1, 'test')
        self.assertEquals(set(subscriber.keys()), self.subscriber_keys)

        # Delete subscriber
        self.sclient.delete_subscriber(1)

    def test_subscribe_free_trial(self):
        # Create a subscriber first
        subscriber = self.sclient.create_subscriber(1, 'test')

        # Subscribe to a free trial
        if not self.plans:
            self.plans = self.sclient.get_plans()
        for plan in self.plans:
            if plan['enabled'] and plan['plan_type'] == 'free_trial':
                break
        else:
            raise Exception("You need to set an active free-trial plan on your spreedly.com account.")
        plan_id = plan['spreedly_id']
        subscription = self.sclient.subscribe(1, plan_id, True)
        self.assertEquals(set(subscriber.keys()), self.subscriber_keys)
        assert subscription['trial_active']

        # Delete subscriber
        self.sclient.delete_subscriber(1)

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

