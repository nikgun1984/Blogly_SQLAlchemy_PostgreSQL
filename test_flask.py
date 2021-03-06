from unittest import TestCase
from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTest(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLastName", image_url="data:image/jpeg;base64,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")
        db.session.add(user)
        db.session.commit()

        post = Post(title="New Post", content="Some content goes here...", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h6 class="display-4">TestUser TestLastName</h6>', html)
            self.assertIn(self.user.first_name, html)
    
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h6 class="display-4">New Post</h6>', html)
            self.assertIn(self.post.content, html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "LastName", "picture": 'https://i.pinimg.com/originals/4f/f2/05/4ff2057a0e7c284d5aeb173d32c08f9f.jpg'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h6 class="display-4">TestUser2 LastName</h6>', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "New Post 2", "content": "Whatever content","user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h6 class="display-4">New Post 2</h6>', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            user = User(first_name="TestUser3", last_name="TestLastName", image_url="data:image/jpeg;base64,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")
            db.session.add(user)
            response = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            # import pdb
            # pdb.set_trace()
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)



