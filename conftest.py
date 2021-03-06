# Licensed under a 3-clause BSD style license - see LICENSE.rst

# This file is the main file used when running tests with pytest directly,
# in particular if running e.g. ``pytest docs/``.

import os
import tempfile

import hypothesis

try:
    from pytest_astropy_header.display import PYTEST_HEADER_MODULES
    PYTEST_HEADER_MODULES['PyERFA'] = 'erfa'
except ImportError:
    PYTEST_HEADER_MODULES = {}

# Tell Hypothesis that we might be running slow tests, to print the seed blob
# so we can easily reproduce failures from CI, and derive a fuzzing profile
# to try many more inputs.  Select profiles with the HYPOTHESIS_PROFILE
# environment variable, defaulting to automatic CI detection.

hypothesis.settings.register_profile('normal', deadline=None)
hypothesis.settings.register_profile('ci', deadline=None, print_blob=True)
hypothesis.settings.register_profile(
    'fuzzing', parent=hypothesis.settings.get_profile('ci'), max_examples=10**4
)
default = 'ci' if os.environ.get('CI') == 'true' else 'normal'
hypothesis.settings.load_profile(os.environ.get('HYPOTHESIS_PROFILE', default))

# Make sure we use temporary directories for the config and cache
# so that the tests are insensitive to local configuration.

os.environ['XDG_CONFIG_HOME'] = tempfile.mkdtemp('astropy_config')
os.environ['XDG_CACHE_HOME'] = tempfile.mkdtemp('astropy_cache')

os.mkdir(os.path.join(os.environ['XDG_CONFIG_HOME'], 'astropy'))
os.mkdir(os.path.join(os.environ['XDG_CACHE_HOME'], 'astropy'))

# Note that we don't need to change the environment variables back or remove
# them after testing, because they are only changed for the duration of the
# Python process, and this configuration only matters if running pytest
# directly, not from e.g. an IPython session.
