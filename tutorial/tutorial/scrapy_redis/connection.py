import six

from scrapy.utils.misc import load_object

from . import defaults


# Shortcut maps 'setting name' -> 'parmater name'.
SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url','REDIS_HOST': 'host','REDIS_PORT': 'port','REDIS_ENCODING': 'encoding'}


def get_redis_from_settings(settings):
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
	if val:
	    params[dest] = val

	# Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


# Backwards compatible alias.
from_settings = get_redis_from_settings


def get_redis(**kwargs):
    redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)

FILTER_URL=None
FILTER_HOST='192.168.163.128'
FILTER_PORT=6379
FILTER_DB=0
def from_setting_filter(settings):
    url=settings.get('FILTER_URL',FILTER_URL)
    host=settings.get('FILTER_HOST',FILTER_HOST)
    port=settings.get('FILTER_PORT',FILTER_PORT)
    db=settings.get('FILTER_DB',FILTER_DB)
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(host=host,port=port,db=db)

