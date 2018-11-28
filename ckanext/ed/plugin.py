from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.ed import actions, helpers, validators


class EDPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IValidators)

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'ed_get_groups': helpers.get_groups,
            'ed_get_recently_updated_datasets': helpers.get_recently_updated_datasets,
            'ed_get_most_popular_datasets': helpers.get_most_popular_datasets,
            'ed_get_total_views_for_dataset': helpers.get_total_views_for_dataset,
        }

    # IActions
    def get_actions(self):
        return {
            'ed_prepare_zip_resources': actions.prepare_zip_resources,
        }

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'ed')

    # IRoutes
    def before_map(self, map):
        map.connect(
            'download_zip',
            '/download/zip/{zip_id}',
            controller='ckanext.ed.controller:DownloadController',
            action='download_zip'
        )

        return map

    # IValidators
    def get_validators(self):
        return {
            'state_validator': validators.state_validator
        }
