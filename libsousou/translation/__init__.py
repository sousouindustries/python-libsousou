# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Django nor the names of its contributors may be used
#        to endorse or promote products derived from this software without
#        specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import collections
import contextlib
import gettext as gnu
import os
import threading
import re


LOCALE_PATTERN = re.compile('^(?P<lang>[a-z]{2})_[A-Z]{2}$')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE')
_active = threading.local()
_translations = collections.defaultdict(dict)
_default = None
_domain = None


def load(domain, localedir, **kwargs):
    global _default
    global DEFAULT_LANGUAGE

    is_default = kwargs.pop('is_default', False)
    languages = kwargs.pop('languages', [])
    t = gnu.translation(domain, localedir, languages=languages)
    for lang in languages:
        _translations[domain][lang] = t

    if is_default:
        _default = t
        DEFAULT_LANGUAGE = t.info()['language']


@contextlib.contextmanager
def language(language_code, fatal=False):
    """Return a context guard that activates a certain language
    and deactivates it when exiting.
    """
    current = activate(language_code)
    yield
    activate(current)


def activate(lang):
    """Sets the current active language to `lang`."""
    current = getattr(_active, 'value', None)
    _active.value = lang
    return current


def get_language():
    """Return a string indicating the currently activated
    language.
    """
    return getattr(_active, 'value', DEFAULT_LANGUAGE)


def dgettext(domain, *args, **kwargs):
    """Like :func:`gettext()`, but look the message up in specified
    `domain`.
    """
    lang = get_language()
    try:
        t = _get_translation(domain, lang)
        return t.gettext(*args, **kwargs)
    except KeyError:
        if _default is None:
            raise

        return _default.gettext(*args, **kwargs)


def _get_translation(domain, lang):
    # If the language code is not in the translations dictionary,
    # try to do some parsing.
    if lang not in _translations[domain]:
        m = LOCALE_PATTERN.match(lang)
        if m is None:
            raise KeyError(lang)
        lang = m.groupdict()['lang']
        return _get_translation(domain, lang)

    return _translations[domain][lang]
