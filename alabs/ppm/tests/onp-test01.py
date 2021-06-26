from alabs.common.util.vvnet import is_svc_opeded

host = 'oauth-rpa.argos-labs.com'
print('%s opened? %s' % (host, is_svc_opeded(host, 443)))

host = 'oauth-rpa-hcl.argos-labs.com'
print('%s opened? %s' % (host, is_svc_opeded(host, 443)))

host = 'api-chief.argos-labs.com'
print('%s opened? %s' % (host, is_svc_opeded(host, 443)))

host = 'api-chief-hcl.argos-labs.com'
print('%s opened? %s' % (host, is_svc_opeded(host, 443)))

host = 's3-us-west-2.amazonaws.com'
print('%s opened? %s' % (host, is_svc_opeded(host, 443)))

