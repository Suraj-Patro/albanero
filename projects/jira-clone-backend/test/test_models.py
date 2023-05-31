import unittest


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        from model import UsersModel, TasksModel, CommentsModel
        from werkzeug.security import generate_password_hash

        self._user = UsersModel(user_name='Test Username', name="Test User Name", email="test_email@gmail.com", password=generate_password_hash("password", method='sha256'))
        self._task = TasksModel(title='Test Task', description="Test Task Description", reporter=self._user.id, assignee=self._user.id)
        self._comment = CommentsModel(message='New comment', task=self._task.id, user=self._user.id)

    
    def test_users_model(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the username, name, email and hashed_password fields are defined correctly
        """
        from werkzeug.security import check_password_hash

        assert self._user.user_name == 'Test Username'
        assert self._user.name == 'Test User Name'
        assert self._user.email == 'test_email@gmail.com'
        assert check_password_hash(self._user.password, "password")


    def test_tasks_model(self):
        """
        GIVEN a Tasks model
        WHEN a new Task is created
        THEN check the title, description, reporter and assignee fields are defined correctly
        """
        assert self._task.title == 'Test Task'
        assert self._task.description == "Test Task Description"
        assert self._task.reporter == self._user.id
        assert self._task.assignee


    def test_comments_model(self):
        """
        GIVEN a Comments model
        WHEN a new Comment is created
        THEN check the message, task and user fields are defined correctly
        """
        assert self._comment.message == 'New comment'
        assert self._comment.task == self._task.id
        assert self._comment.user == self._user.id
