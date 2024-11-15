import unittest

from flask_testing import TestCase

from app import create_app, db
from app.models import Employee


class TestBase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root:123456789@127.0.0.1:3306/employee_management_test')
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(username='test_admin', password='admin', is_admin=True)

        # create test non-admin user
        employee = Employee(username='test_user', password='testuser')

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_employee_model(self):
        """
        Test number of record in Employees table
        """
        self.assertEqual(Employee.query.count(), 2)


if __name__ == '__main__':
    unittest.main()
