from nose.tools import assert_raises, assert_equals

from ckan.lib.search import rebuild
from ckan.tests import factories as core_factories
from ckan.tests import helpers as test_helpers
from ckan.tests.helpers import call_action, FunctionalTestBase
import ckan.plugins.toolkit as toolkit

from ckanext.ed.tests import factories


class TestWorFlows(FunctionalTestBase):
    # For some reasons @classmethod does not work
    def setup(self):
        self.pkg_1 = 'test-dataset-1'
        self.pkg_2 = 'test-dataset-2'
        test_helpers.reset_db()
        rebuild()
        core_factories.User(name='george')
        core_factories.User(name='john')
        core_factories.User(name='paul')
        core_factories.Organization(
            users=[
                {'name': 'george', 'capacity': 'admin'},
                {'name': 'john', 'capacity': 'editor'},
                {'name': 'paul', 'capacity': 'reader'}
            ],
            name='us-ed-1',
            id='us-ed-1'
        )
        # Dataset created by factories seem to use sysadmin so approval_state
        # forced to be "approved". Creating packages this way to avoid that
        context = {'user': 'john'}
        data_dict = _create_dataset_dict(self.pkg_1, 'us-ed-1')
        call_action('package_create', context, **data_dict)

        # 1 datasets above "approveal_pending" and 1 below "approved"
        context = {'user': 'george'}
        data_dict = _create_dataset_dict(self.pkg_2, 'us-ed-1')
        call_action('package_create', context, **data_dict)


    @classmethod
    def tearDownClass(self):
        pass


    def test_dataset_not_appears_in_search_if_not_approved_admin(self):
        context = {'user': 'george'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_dataset_not_appears_in_search_if_not_approved_editor(self):
        context = {'user': 'john'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_dataset_not_appears_in_search_if_not_approved_reder(self):
        context = {'user': 'paul'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_dataset_not_appears_in_search_if_not_approved_aninimous(self):
        context = {'user': 'ringo'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_package_show_admin_can_see_both(self):
        context = {'user': 'george'}
        packages = call_action('package_show', context, **{'id': self.pkg_1})
        assert_equals(packages['name'], self.pkg_1)
        packages = call_action('package_show', context, **{'id': self.pkg_2})
        assert_equals(packages['name'], self.pkg_2)

    def test_package_show_editor_can_see_both(self):
        context = {'user': 'john'}
        packages = call_action('package_show', context, **{'id': self.pkg_1})
        assert_equals(packages['name'], self.pkg_1)
        packages = call_action('package_show', context, **{'id': self.pkg_2})
        assert_equals(packages['name'], self.pkg_2)

    def test_package_show_member_can_not_see_pending(self):
        context = {'user': 'paul', 'ignore_auth': False}
        assert_raises(toolkit.ObjectNotFound,
                      call_action, 'package_show', context, id=self.pkg_1)
        packages = call_action('package_show', context, **{'id': self.pkg_2})
        assert_equals(packages['name'], self.pkg_2)

    def test_package_show_anonimous_can_not_see_pending(self):
        context = {'user': 'ringo', 'ignore_auth': False}
        assert_raises(toolkit.ObjectNotFound,
                      call_action, 'package_show', context, id=self.pkg_1)
        packages = call_action('package_show', context, **{'id': self.pkg_2})
        assert_equals(packages['name'], self.pkg_2)


# Helpers


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
