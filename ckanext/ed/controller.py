import logging
import os

from ckan import model
from ckan.common import response
from ckan.lib import base
from ckan.logic.action import delete as delete_core
from ckan.logic.action import get as get_core
from ckan.logic.action import patch as patch_core
from ckan.plugins import toolkit
from ckanext.ed.helpers import get_storage_path_for
from ckanext.ed.mailer import mail_package_publish_update_to_user


class DownloadController(base.BaseController):
    def download_zip(self, zip_id):
        if not zip_id:
            abort(404, toolkit._('Resource data not found'))
        file_name, package_name = zip_id.split('::')
        file_path = get_storage_path_for('temp-ed/' + file_name)

        if not os.path.isfile(file_path):
            abort(404, toolkit._('Resource data not found'))

        if not package_name:
            package_name = 'resources'
        package_name += '.zip'

        with open(file_path, 'r') as f:
            response.write(f.read())

        response.headers['Content-Type'] = 'application/octet-stream'
        response.content_disposition = 'attachment; filename=' + package_name
        os.remove(file_path)


class PublishControler(base.BaseController):
    def approve(self, id):
        # check access and state
        _raise_not_authz_or_not_pending(id)
        data_dict = patch_core.package_patch({}, {'id': id, 'state': 'active'})
        mail_package_publish_update_to_user({}, data_dict, event='approval')

        # show flash message and redirect
        toolkit.h.flash_success('Dataset "{}" approved'.format(data_dict['title']))
        toolkit.redirect_to(controller='package', action='read', id=data_dict['name'])

    def reject(self, id, *args, **kwargs):
        # check access and state
        _raise_not_authz_or_not_pending(id)
        data_dict = get_core.package_show({'model': model}, {'id': id})
        mail_package_publish_update_to_user({}, data_dict, event='rejection')
        delete_core.dataset_purge({'model': model}, {'id': id})

        # show flash message and redirect
        toolkit.h.flash_error('Dataset "{}" rejected'.format(data_dict['title']))
        toolkit.redirect_to('/dataset')


def _raise_not_authz_or_not_pending(id):
    # check auth with toolkit.check_access
    toolkit.check_access('sysadmin', {'model': model})

    # check org exists and it's pending with organization_show
    data_dict = toolkit.get_action('package_show')({}, {'id': id})
    if data_dict.get('state') != 'approval_needed':
        raise toolkit.ObjectNotFound('Dataset "{}" not found'.format(id))
