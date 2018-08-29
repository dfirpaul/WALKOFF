from unittest import TestCase

from tests.util.mock_objects import MockRedisCacheAdapter
from walkoff.cache import unsubscribe_message


class TestRedisCacheAdapter(TestCase):

    def setUp(self):
        self.cache = MockRedisCacheAdapter()

    def tearDown(self):
        self.cache.clear()
        self.cache.shutdown()

    def test_singleton(self):
        cache = MockRedisCacheAdapter()
        self.assertIs(cache, self.cache)

    def test_set_get(self):
        self.assertTrue(self.cache.set('alice', 'something'))
        self.assertEqual(self.cache.get('alice'), 'something')
        self.assertTrue(self.cache.set('count', 1))
        self.assertEqual(self.cache.get('count'), '1')
        self.assertTrue(self.cache.set('count', 2))
        self.assertEqual(self.cache.get('count'), '2')

    def test_get_key_dne(self):
        self.assertIsNone(self.cache.get('invalid_key'))

    def test_add(self):
        self.assertTrue(self.cache.add('test', 123))
        self.assertEqual(self.cache.get('test'), '123')
        self.assertFalse(self.cache.add('test', 456))
        self.assertEqual(self.cache.get('test'), '123')

    def test_delete(self):
        self.assertTrue(self.cache.set('alice', 'something'))
        self.cache.delete('alice')
        self.assertIsNone(self.cache.get('alice'))

    def test_delete_dne(self):
        self.cache.delete('alice')
        self.assertIsNone(self.cache.get('alice'))

    def test_incr(self):
        self.cache.set('count', 1)
        self.assertEqual(self.cache.incr('count'), 2)
        self.assertEqual(self.cache.get('count'), '2')

    def test_incr_multiple(self):
        self.cache.set('uid', 3)
        self.assertEqual(self.cache.incr('uid', amount=10), 13)
        self.assertEqual(self.cache.get('uid'), '13')

    def test_incr_key_dne(self):
        self.assertEqual(self.cache.incr('count'), 1)
        self.assertEqual(self.cache.get('count'), '1')

    def test_incr_multiple_key_dne(self):
        self.assertEqual(self.cache.incr('workflows', amount=10), 10)
        self.assertEqual(self.cache.get('workflows'), '10')

    def test_decr(self):
        self.cache.set('count', 0)
        self.assertEqual(self.cache.decr('count'), -1)
        self.assertEqual(self.cache.get('count'), '-1')

    def test_decr_multiple(self):
        self.cache.set('uid', 3)
        self.assertEqual(self.cache.decr('uid', amount=10), -7)
        self.assertEqual(self.cache.get('uid'), '-7')

    def test_decr_key_dne(self):
        self.assertEqual(self.cache.decr('count'), -1)
        self.assertEqual(self.cache.get('count'), '-1')

    def test_decr_multiple_key_dne(self):
        self.assertEqual(self.cache.decr('workflows', amount=10), -10)
        self.assertEqual(self.cache.get('workflows'), '-10')

    def test_r_push_pop_single_value(self):
        self.cache.rpush('queue', 10)
        self.assertEqual(self.cache.rpop('queue'), '10')

    def test_r_push_pop_multiple_values(self):
        self.cache.rpush('big', 10, 11, 12)
        self.assertEqual(self.cache.rpop('big'), '12')

    def test_l_push_pop_single_value(self):
        self.cache.lpush('queue', 10)
        self.assertEqual(self.cache.lpop('queue'), '10')

    def test_l_push_pop_multiple_values(self):
        self.cache.rpush('big', 10, 11, 12)
        self.assertEqual(self.cache.lpop('big'), '10')
        self.assertEqual(self.cache.rpop('big'), '12')

    def test_scan_no_pattern(self):
        keys = ('a', 'b', 'c', 'd')
        for i, key in enumerate(keys):
            self.cache.set(key, i)
        ret_keys = self.cache.scan()
        self.assertSetEqual(set(ret_keys), set(keys))

    def test_scan_with_pattern(self):
        keys = ('1.a', '2.a', '3.b', 'd')
        for i, key in enumerate(keys):
            self.cache.set(key, i)
        ret_keys = self.cache.scan('*.a')
        self.assertSetEqual(set(ret_keys), {'1.a', '2.a'})

    def test_exists(self):
        key = 'abc'
        self.assertFalse(self.cache.exists(key))
        self.cache.set(key, 42)
        self.assertTrue(self.cache.exists(key))

    def test_subscribe(self):
        sub = self.cache.subscribe('channel1')
        self.assertEqual(sub.channel, 'channel1')

    def test_publish(self):
        sub = self.cache.subscribe('channel_a')
        self.cache.publish('channel_a', '42')
        result = sub._pubsub.get_message()
        self.assertEqual(result['data'], b'42')

    def test_unsubscribe(self):
        sub = self.cache.subscribe('channel_a')
        self.cache.unsubscribe('channel_a')
        result = sub._pubsub.get_message()
        self.assertEqual(result['data'], unsubscribe_message)

    def test_lock(self):
        r = self.cache.lock('myname', timeout=4.5, sleep=0.5, blocking_timeout=1.6)
        self.assertEqual(r.name, 'myname')