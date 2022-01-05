from django.db import connection

class TenantContextFilter(object):
    """Adds the current tenant's ``schema_name`` and ``domain_url`` properties to all log messages."""
    def filter(self, record):
        record.schema_name = connection.schema_name
        record.domain_url = getattr(connection.tenant, 'domain_url', None)
        return True