"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_user_model.py


import os
from unittest import TestCase
import re

from models import db, User, Message, Follows


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

##########MAKE SURE TO CREATE A SEPERATE DATABASE##############
os.environ['DATABASE_URL'] = "postgresql:///warbler-unittest"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

#####connect_db(app) causes a conflict with SQLAlchemy because another instance is using..

#added the below  - JH 11-6
with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        #added app.app_context() - JH 11-6
        with app.app_context():
            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            self.client = app.test_client()
            #added a commit to prevent duplicates...not sure if this is correct - JH 11-6
            #db.session.commit()  <---removed to preserve the database values

    def test_user_model(self):
        """Does basic model work?"""
        #added app.app_context() - JH 11-6
        with app.app_context():
            u = User(
                email="test5@test.com",
                username="test5user",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            #db.session.commit()  <---removed to preserve the database values

        # User should have no messages & no followers
            self.assertEqual(len(u.messages), 0)
            self.assertEqual(len(u.followers), 0)

    def tearDowm(self):
        db.session.rollback()
    
    def check_is_following(self):
        """checks if user is following another user or not"""

        with app.app_context():
            user1 = User(
                email="test_follow1@test.com",
                username="test_follow_user1",
                password="HASHED_PASSWORD",
                
            )
            user2 = User(
                email="test_follow2@test.com",
                username="test_follow_user2",
                password="HASHED_PASSWORD",
             )
            
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            user1.following.append(user2)
            db.session.commit()

            self.assertIn(user2, user1.following)
            self.assertNotIn(user1, user2.following) #takes care of the check_is_follow_by?

            db.session.rollback()
    
    def check_is_followed_by(self):
        """checks when user is followed or not follow"""
        with app.app_context():
             
             user1 = User(
                email="test_follow1@test.com",
                username="test_follow_user1",
                password="HASHED_PASSWORD",
                
            )
             user2 = User(
                email="test_follow2@test.com",
                username="test_follow_user2",
                password="HASHED_PASSWORD",
             )
             db.session.add(user1)
             db.session.add(user2)
             user1.is_followed_by.append(user2)
             db.session.commit()

             self.assertIn(user2, user1.is_followed_by)
             self.assertNotIn(user1, user2.is_followed_by)

             db.session.rollback()
        
    def test_user_with_validation(self):
        with app.app_context():
            with self.assertRaises(ValueError):
                 self.create_user_with_validation(
                   email="notanemail",
                    password="longenoughpassword",
                    username="testuser6"
               )   
            with self.assertRaises(ValueError):
                self.create_user_with_validation(
                email="test@example.com",
                password="shor",
                username="testuser6"
            )      
            with self.assertRaises(ValueError):
                self.create_user_with_validation(
                email="test@example.com",
                username="",
                password="longenoughpassword"
                )

    def create_user_with_validation(self, email, username, password):
         with app.app_context():
              if len(password) < 6:
                 raise ValueError("Password too short")
              if not re.match(r"[^@]+@[^@]+\.[^@]+", email): 
                 raise ValueError("Invalid email format")
              if not username:
                 raise ValueError("Username required")
                  


    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "testtest@test.com", "password", None)
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password", None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password", None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None)
 
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))  
    def test_user_authentication(self, password, username):
        with app.app_context():
            
    #not needed...
    #def tearDowm(self):
    #    db.session.rollback() 
