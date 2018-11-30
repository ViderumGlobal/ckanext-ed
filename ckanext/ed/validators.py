from logging import getLogger

import ckan.logic.action.get as get_core

from ckanext.ed import helpers


log = getLogger(__name__)


def state_validator(key, data, errors, context):
    user_orgs = get_core.organization_list_for_user(context, {'id': context['user']})
    office_id = data.get(('owner_org',))
    state = 'approval_pending'
    # user is member of the org and admin remove pending
    for org in user_orgs:
        if org.get('id') == office_id and org.get('capacity') == 'admin':
            state = None
    data[key] = state
