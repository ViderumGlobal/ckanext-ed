import os
import logging

from ckan import model
from ckan.common import response
from ckan.lib import base
from ckan.plugins import toolkit

from ckanext.ed.helpers import get_storage_path_for

log = logging.getLogger()


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


class ApproveRejectControler(base.BaseController):
    def approve(self, id):
        _make_action(id, 'approve')

    def reject(self, id):
        _make_action(id, 'reject')


def _raise_not_authz_or_not_pending(id):
    toolkit.check_access(
        'package_delete', {'model': model, 'user': toolkit.c.user}, {'id': id})
    # check approval_state is pending
    data_dict = toolkit.get_action('package_show')({}, {'id': id})
    if data_dict.get('approval_state') != 'approval_pending':
        raise toolkit.ObjectNotFound('Dataset "{}" not found'.format(id))


def _make_action(package_id, action='reject'):
    states = {
        'reject': 'rejected',
        'approve': 'approved'
    }
    # check access and state
    _raise_not_authz_or_not_pending(package_id)
    data_dict = toolkit.get_action('package_patch')(
        {'model': model, 'user': toolkit.c.user},
        {'id': package_id, 'approval_state': states[action]}
    )
    msg = 'Dataset "{0}" {1}'.format(data_dict['title'], states[action])
    if action == 'approve':
        toolkit.h.flash_success(msg)
    else:
        toolkit.h.flash_error(msg)
    toolkit.redirect_to(controller='package', action='read', id=data_dict['name'])
