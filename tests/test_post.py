import unittest
from app.models import User,Post,Comments


class PostTest(unittest.TestCase):
    """
    Test Class to test the behaviour of the class
    """

    def setUp(self):
        """
        Set up method that will run before every Test
        """
        self.post= Post(category='Product', content='Yes we can!')


    def tearDown(self):
        Post.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_check_instance_variables(self):
        self.assertEquals(self.post.category,'Product')
        self.assertEquals(self.post.content,'Yes we can!')
