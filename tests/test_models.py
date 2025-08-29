import pytest
from engagement.models import TextbookSection

@pytest.mark.django_db
def test_section_str():
    s = TextbookSection.objects.create(section_title="Intro")
    assert str(s) == "Intro"
