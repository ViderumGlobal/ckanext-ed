from ckan.tests import factories


class Dataset(factories.Dataset):
    contact_name = 'Example User'
    contact_email = 'contact@example.com'
    access_level = 'public'
    bureau_code = '015:11'
    program_code = '0001:17'
    identifier =  'abcd1234'
