import ckan.logic as logic
from ckan import model
from ckan.plugins import toolkit
from ckan.common import config
import os
import logging

from datetime import datetime

log = logging.getLogger()

def _get_action(action, context_dict, data_dict):
    return toolkit.get_action(action)(context_dict, data_dict)


def get_groups():
    # Helper used on the homepage for showing groups

    data_dict = {
        'all_fields': True
    }
    groups = _get_action('group_list', {}, data_dict)

    return groups


def get_recently_updated_datasets(limit=5, user=None):
    '''
     Returns recent created or updated datasets.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :param user: user name
    :type user: string

    :returns: a list of recently created or updated datasets
    :rtype: list
    '''
    try:
        pkg_search_results = toolkit.get_action('package_search')(
            context={'user': user},
            data_dict={
                'sort': 'metadata_modified desc',
                'rows': limit
            })['results']

    except toolkit.ValidationError, search.SearchError:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(context={'user': user},
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = ((datetime.now() - modified).days)
            pkgs.append(package)
        return pkgs


def get_most_popular_datasets(limit=5, user=None):
    '''
     Returns most popular datasets based on total views.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :param user: user name
    :type user: string

    :returns: a list of most popular datasets
    :rtype: list
    '''
    data = pkg_search_results = toolkit.get_action('package_search')(
        context={'user': user},
        data_dict={
            'sort': 'views_total desc',
            'rows': limit,
        })['results']

    return data


def get_storage_path_for(dirname):
    """Returns the full path for the specified directory name within
    CKAN's storage path. If the target directory does not exists, it
    gets created.

    :param dirname: the directory name
    :type dirname: string

    :returns: a full path for the specified directory name within CKAN's storage path
    :rtype: string
    """
    storage_path = config.get('ckan.storage_path')
    target_path = os.path.join(storage_path, 'storage', dirname)
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except OSError, exc:
            log.error('Storage directory creation failed. Error: %s' % exc)
            target_path = os.path.join(storage_path, 'storage')
            if not os.path.exists(target_path):
                log.info('CKAN storage directory not found also')
                raise

    return target_path


def get_total_views_for_dataset(id):
    data_dict = {
        'id': id,
        'include_tracking': True
    }

    try:
        dataset = _get_action('package_show', {}, data_dict)
        return dataset.get('tracking_summary').get('total')
    except Exception:
        return 0


def is_admin(user):
    """
    Returns True if user is admin of any organisation

    :param user: user name
    :type user: string

    :returns: True/False
    :rtype: boolean
    """
    user_orgs = _get_action('organization_list_for_user', {'user': user}, {'user': user})
    return any([i.get('capacity') == 'admin' for i in user_orgs])
