import logging
from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
from ckan.lib.mailer import mail_user
from ckan.lib.base import render_jinja2
import ckan.logic.action.get as get_core
log = logging.getLogger(__name__)


def mail_package_publish_request_to_sysadmins(context, data_dict):
    context.setdefault('model', model)
    # Mail all sysadmins
    for user in _get_sysadmins(context):
        if user.email:
            subj = _compose_email_subj(data_dict, event='request')
            body = _compose_email_body(data_dict, user, event='request')
            mail_user(user, subj, body)
            log.debug('[email] Pakcage publishing request email sent to {0}'.format(user.name))


def mail_package_publish_update_to_user(context, pkg_dict, event='approval'):
    context.setdefault('model', model)
    user = model.User.get(pkg_dict['creator_user_id'])
    if user and user.email:
        subj = _compose_email_subj(pkg_dict, event=event)
        body = _compose_email_body(pkg_dict, user, event=event)
        mail_user(user, subj, body)
        log.debug('[email] Data container update email sent to {0}'.format(user.name))


def _get_sysadmins(context):
    model = context['model']
    return model.Session.query(model.User).filter(model.User.sysadmin==True).all()


def _compose_email_subj(data_dict, event='request'):
    return '[US ED] Package Publishing {0}: {1}'.format(event.capitalize(), data_dict['title'])


def _compose_email_body(data_dict, user, event='request'):
    pkg_link = toolkit.url_for('dataset_read', id=data_dict['name'], qualified=True)
    return render_jinja2('emails/package_publish_{0}.txt'.format(event), {
        'user_name': user.fullname or user.name,
        'site_title': config.get('ckan.site_title'),
        'site_url': config.get('ckan.site_url'),
        'package_title': data_dict['title'],
        'package_link': pkg_link,
        'publisher_name': data_dict.get('contact_name')
    })
