"""
This module provide class to control domain data.
"""


class SlamDomainController:
    """
    SlamDomainController provide CLI wrapper to manage a SLAM domain
    """
    def __init__(self, api):
        """
        :param self: object itself
        :param api: generic api for SLAM REST api
        """
        self.api = api

    def create(self, options):
        """
        Create a new domain on SLAM. By default, we only need domain name and DNS master entry

        :param self: object itself
        :param options: arguments pass throught CLI
        """
        domain = {
            'name': options.domain,
            'description': options.description,
            'contact': options.contact,
            'master': options.dns_master
        }
        result = self.api.create('domains', options.domain, domain)
        if result['status'] == 'done':
            print('Domain {} as been created.'.format(result['domain']))
        else:
            print('Domain {} creation failed with status {}'.format(result['domain'],
                                                                    result['status']))

    def add(self, options):
        """
        Add a new entry into a domain. A entry is a fqdn (ie www.example.com)

        :param self: object itself
        :param options: arguments pass throught CLI
        """
        fqdn = options.fqdn.split('.', 1)
        name = fqdn[0]
        domain = fqdn[1]
        entry = dict()
        if options.description is not None:
            entry['description'] = options.description
        if options.type is not None:
            entry['type'] = options.type
        result = self.api.create('domains', domain, entry, field=name)
        if result['status'] == 'done':
            print('Name resolution {} as been added to domain {}'.format(name, domain))
        else:
            print('Name resolution {}.{} addition has failed with status {}'.format(
                result['name'],
                result['domain'],
                result['status']
            ))

    def update(self, options):
        """
        Modify a domain. This allow to change contact email, description and dns-master

        :param self: object itself
        :param options: arguments pass throught CLI
        """
        modification = {}
        if options.contact is not None:
            modification['contact'] = options.contact
        if options.description is not None:
            modification['description'] = options.description
        if options.dns_master is not None:
            modification['master'] = options.dns_master
        result = self.api.update('domains', options.domain, modification)
        if result['status'] == 'done':
            print('Domain {} has been modified'.format(options.domain))
        else:
            print('Domain {} modification failed with status {}'.format(options.domain,
                                                                        result['status']))
