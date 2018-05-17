import pytest

import wurfdocs
from wurfdocs.build_info import BuildInfo


def test_build_info():

    build_info = BuildInfo()

    build_info.slug = 'slug'

    with pytest.raises(AttributeError):
        build_info.slug = 'slug2'

    assert build_info.slug == 'slug'
