import mock
from nose.tools import assert_raises, assert_equals

from ckan import model
from ckan.tests import factories as core_factories
from ckan.tests import helpers as test_helpers
from ckanext.ed.tests import factories

from ckanext.ed.mailer import mail_package_publish_request_to_admins


# Without jinja2 mocking it can't find a template in the test mode
class TestHelpers(test_helpers.FunctionalTestBase):
    context = {'model': model, 'ignore_auth': True}

    @mock.patch('ckanext.ed.mailer.mail_user')
    @mock.patch('ckanext.ed.mailer.render_jinja2')
    def test_mail_package_publish_request_to_admins(self, mock_render_jinja2, mock_mail_user):
        admin_1 = core_factories.User()
        admin_2 = core_factories.User()
        editor = core_factories.User()
        office = core_factories.Organization(
            users=[
                {'name': admin_1['name'], 'capacity': 'admin'},
                {'name': admin_2['name'], 'capacity': 'admin'},
                {'name': editor['name'], 'capacity': 'editor'},
            ],
            name='us-ed',
            id='us-ed'
        )
        mail_package_publish_request_to_admins(
            self.context,
            _create_dataset_dict('test', office['name'])
        )
        assert_equals(mock_mail_user.call_count, 2)
        assert_equals(mock_render_jinja2.call_args[0][0], 'emails/package_publish_request.txt')


def _create_dataset_dict(package_name, office_name='us-ed'):
    return {
        'name': package_name,
        'contact_name': 'Stu Shepard',
        'program_code': '321',
        'access_level': 'public',
        'bureau_code': '123',
        'contact_email': '%s@email.com' % package_name,
        'notes': 'notes',
        'owner_org': office_name,
        'title': 'Title',
        'identifier': 'identifier'
    }
