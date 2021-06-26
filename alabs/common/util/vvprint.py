################################################################################
import pprint


################################################################################
class PrettyPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):
        if isinstance(_object, str):
            # return "%s" % _object.encode('utf8'), True, False
            return '"%s"' % _object, True, False
        return pprint.PrettyPrinter.format(self, _object, context,
                                           maxlevels, level)


################################################################################
def readable_bytes(n):
    if n >= 1024 * 1024 * 1024:
        return '%0.2fG' % (n / (1024 * 1024 * 1024))
    if n >= 1024 * 1024:
        return '%0.2fM' % (n / (1024 * 1024))
    if n >= 1024:
        return '%0.2fk' % (n / 1024)
    return '%d' % n


################################################################################
if __name__ == '__main__':
    # d = {'_id': '12345', 'kind': 'abc',
    #      'name': '\xea\xb0\x80\xeb\x82\x98\xeb\x8b\xa4'}
    d = {'age': 9, 'id': 30,
         'title': '안녕? 세계야?'}

    pprint.pprint(d)
    # PrettyPrinter().pprint(d)
    print(PrettyPrinter().pformat(d))
