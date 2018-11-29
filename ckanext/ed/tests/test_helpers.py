from ckan.tests import helpers as test_helpers
from ckan.tests import factories as core_factories

from ckanext.ed import helpers
from ckanext.ed.tests import factories


class TestHelpers(test_helpers.FunctionalTestBase):
    def test_get_recently_updated_datasets(self):
        factories.Dataset()
        factories.Dataset()
        factories.Dataset()
        dataset = factories.Dataset()

        result = helpers.get_recently_updated_datasets()
        assert len(result) == 4
        assert result[0]['id'] == dataset['id']

        result = helpers.get_recently_updated_datasets(limit=2)
        assert len(result) == 2
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
