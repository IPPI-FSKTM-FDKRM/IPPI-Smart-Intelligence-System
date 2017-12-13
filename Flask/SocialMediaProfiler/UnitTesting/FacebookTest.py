import unittest
from Flask.SocialMediaProfiler.Facebook import Facebook

class TestFacebook(unittest.TestCase):
    id = '1362815530452737'
    facebook = Facebook()

    def test_getUsername(self):
        self.facebook.setUsername('312312312')
        self.assertEqual(self.facebook.getUsername(), '312312312')

    def test_getCache(self):
        testTags = {}
        testLikes = {}
        testComments = {}

        self.assertTupleEqual(self.facebook.getCacheCommentsAndLikes(), (testComments,testLikes, testTags))

    def test_getLocationAddress(self):
        address = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        self.assertDictEqual(self.facebook.getLocationAddress(),address)

    def test_getAmountLikesandComments(self):
        testAmountLikes, testAmountComments = {} , {}
        self.facebook.loadCache('test')
        self.assertAlmostEqual(self.facebook.getAmountLikesAndComments(), (testAmountComments,testAmountLikes))


if __name__ == "__main__":
    unittest.main()