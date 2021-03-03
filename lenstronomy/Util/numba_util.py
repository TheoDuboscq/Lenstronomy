import numba
import lenstronomy
import os
import yaml


"""
From pyautolens:
Depending on if we're using a super computer, we want two different numba decorators:
If on laptop:
@numba.jit(nopython=True, cache=True, parallel=False)
If on super computer:
@numba.jit(nopython=True, cache=False, parallel=True)
"""


from xdg.BaseDirectory import xdg_config_home

user_config_file = os.path.join(xdg_config_home, "lenstronomy", "config.yaml")

module_path = os.path.dirname(lenstronomy.__file__)
default_config_file = os.path.join(module_path, 'Conf', 'conf_default.yaml')

if os.path.exists(user_config_file ):
    conf_file = user_config_file
else:
    conf_file = default_config_file

with open(conf_file) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    conf = yaml.load(file, Loader=yaml.FullLoader)
    numba_conf = conf['numba']
    nopython = numba_conf['nopython']
    cache = numba_conf['cache']
    parallel = numba_conf['parallel']
    numba_enabled = numba_conf['enable']
    fastmath = numba_conf['fastmath']
    error_model = numba_conf['error_model']

#nopython = True
#cache = True
#parallel = False

__all__ = ['jit']


def jit(nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath, error_model=error_model):
    if numba_enabled:
        def wrapper(func):
            return numba.jit(func, nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath,
                             error_model=error_model)
    else:
        def wrapper(func):
            return func
    return wrapper

