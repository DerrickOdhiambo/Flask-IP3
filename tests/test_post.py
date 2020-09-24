import unittest
from app.models import User,Post,Comments
from app import db


class PostTest(unittest.TestCase):

    def setUp(self):
        """
        Set up method that will run before every Test
        """
        self.post= Post(category='Product', content='Yes we can!')
        self.user_Derrick = User(username = 'Derrick',password = 'password', email = 'derrick@mail.com')
        self.new_comment = Comments(text='This is good', user=self.user_Derrick )

    def tearDown(self):
        Comments.query.delete()
        Post.query.delete()
        User.query.delete() 


    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_check_instance_variables(self):
        self.assertEquals(self.post.category,'Product')
        self.assertEquals(self.post.content,'Yes we can!')
        self.assertEquals(self.new_comment.text,'This is good')
        self.assertEquals(self.new_comment.user,self.user_Derrick)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all())>0)
