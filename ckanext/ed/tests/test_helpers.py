from ckan.tests import helpers as test_helpers
from ckan.tests import factories as core_factories

from ckanext.ed import helpers
from ckanext.ed.tests import factories


class TestHelpers(test_helpers.FunctionalTestBase):
    def test_get_recently_updated_datasets(self):
        user = core_factories.User()
        org = core_factories.Organization(
            users=[{'name': user['name'], 'capacity': 'admin'}]
        )
        factories.Dataset(owner_org=org['id'])
        factories.Dataset(owner_org=org['id'])
        factories.Dataset(owner_org=org['id'])
        dataset = factories.Dataset(owner_org=org['id'])

        result = helpers.get_recently_updated_datasets(user=user['name'])
        assert len(result) == 4, 'Epextec 4 but got %s' % len(result)
        assert result[0]['id'] == dataset['id']

        result = helpers.get_recently_updated_datasets(limit=2, user=user['name'])
        assert len(result) == 2
        assert result[0]['id'] == dataset['id']

    def test_get_recently_updated_datasets_lists_only_approved(self):
        user = core_factories.User()
        org = core_factories.Organization(
            users=[{'name': user['name'], 'capacity': 'admin'}]
        )
        factories.Dataset()
        factories.Dataset()
        factories.Dataset(owner_org=org['id'])
        dataset = factories.Dataset(owner_org=org['id'])

        result = helpers.get_recently_updated_datasets(user=user['name'])
        assert len(result) == 2, 'Epextec 2 but got %s' % len(result)
        assert result[0]['id'] == dataset['id']

    def test_get_groups(self):
        group1 = core_factories.Group()

        result = helpers.get_groups()
        assert len(result) == 1
        core_factories.Group()
        core_factories.Group()
        core_factories.Group()
        result = helpers.get_groups()
        assert result[0]['id'] == group1['id']
        assert len(result) == 4
