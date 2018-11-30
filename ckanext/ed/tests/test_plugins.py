from nose.tools import assert_raises, assert_equals

from ckan.tests import factories as core_factories
from ckan.tests.helpers import call_action, FunctionalTestBase
import ckan.plugins.toolkit as toolkit

from ckanext.ed.tests import factories


class TestPlugins(FunctionalTestBase):
    def test_dataset_appears_in_search_if_approved(self):
        core_factories.User(name='george')
        core_factories.User(name='john')
        core_factories.User(name='paul')
        core_factories.Organization(
            users=[
                {'name': 'george', 'capacity': 'admin'},
                {'name': 'john', 'capacity': 'editor'},
                {'name': 'paul', 'capacity': 'member'}
            ],
            name='us-ed-1',
            id='us-ed-1'
        )
        factories.Dataset(approval_state='approved', owner_org='us-ed-1')

        # Admin
        context = {'user': 'george'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Editor
        context = {'user': 'john'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Member
        context = {'user': 'paul'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Anonimous
        context = {'user': 'ringo'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_dataset_not_appears_in_search_if_not_approved(self):
        core_factories.User(name='george')
        core_factories.User(name='john')
        core_factories.User(name='paul')
        core_factories.Organization(
            users=[
                {'name': 'george', 'capacity': 'admin'},
                {'name': 'john', 'capacity': 'editor'},
                {'name': 'paul', 'capacity': 'member'}
            ],
            name='us-ed-2',
            id='us-ed-2'
        )

        # Dataset created by factories seem to use sysadmin so approval_state
        # forced to be "approved". Creating packages this way to avoid that
        context = {'user': 'john'}
        data_dict = _create_dataset_dict('test-dataset-1', 'us-ed-2')
        call_action('package_create', context, **data_dict)

        context = {'user': 'john'}
        data_dict = _create_dataset_dict('test-dataset-2', 'us-ed-2')
        call_action('package_create', context, **data_dict)

        # 2 datasets above "approveal_pending" and 1 below "approved"
        context = {'user': 'george'}
        data_dict = _create_dataset_dict('test-dataset-3', 'us-ed-2')
        call_action('package_create', context, **data_dict)

        # Admin
        context = {'user': 'george'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Editor
        context = {'user': 'john'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Member
        context = {'user': 'paul'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

        # Anonimous
        context = {'user': 'ringo'}
        packages = call_action('package_search', context, **{})
        assert_equals(packages['count'], 1)

    def test_package_show(self):
        core_factories.User(name='george')
        core_factories.User(name='john')
        core_factories.User(name='paul')
        core_factories.Organization(
            users=[
                {'name': 'george', 'capacity': 'admin'},
                {'name': 'john', 'capacity': 'editor'},
                {'name': 'paul', 'capacity': 'member'}
            ],
            name='us-ed-3',
            id='us-ed-3'
        )

        pkg_1 = 'test-dataset-1'
        pkg_2 = 'test-dataset-2'

        # Dataset created by factories seem to use sysadmin so approval_state
        # forced to be "approved". Creating packages this way to avoid that
        context = {'user': 'john'}
        data_dict = _create_dataset_dict(pkg_1, 'us-ed-3')
        call_action('package_create', context, **data_dict)

        # 1 datasets above "approveal_pending" and 1 below "approved"
        context = {'user': 'george'}
        data_dict = _create_dataset_dict(pkg_2, 'us-ed-3')
        call_action('package_create', context, **data_dict)

        # Admin
        context = {'user': 'george'}
        packages = call_action('package_show', context, **{'id': pkg_1})
        assert_equals(packages['name'], pkg_1)
        packages = call_action('package_show', context, **{'id': pkg_2})
        assert_equals(packages['name'], pkg_2)

        # Editor
        context = {'user': 'john'}
        packages = call_action('package_show', context, **{'id': pkg_1})
        assert_equals(packages['name'], pkg_1)
        packages = call_action('package_show', context, **{'id': pkg_2})
        assert_equals(packages['name'], pkg_2)

        # 2 checks bellow not passing due to context issue
        # Member
        context = {'user': 'paul', 'ignore_auth': False}
        assert_raises(toolkit.ObjectNotFound,
                      call_action, 'package_show', context, id=pkg_1)
        packages = call_action('package_show', context, **{'id': pkg_2})
        assert_equals(packages['name'], pkg_2)

        # Anonymous
        context = {'user': 'ringo', 'ignore_auth': False}
        assert_raises(toolkit.ObjectNotFound,
                      call_action, 'package_show', context, id=pkg_1)
        packages = call_action('package_show', context, **{'id': pkg_2})
        assert_equals(packages['name'], pkg_2)

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
