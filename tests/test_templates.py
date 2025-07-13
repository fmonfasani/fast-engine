from pathlib import Path
from fast_engine.templates import TemplateEngine

def test_list_templates(tmp_path):
    base = tmp_path / "templates"
    base.mkdir()

    valid1 = base / "t1"
    valid1.mkdir()
    (valid1 / "template.yml").write_text("name: t1")

    valid2 = base / "t2"
    valid2.mkdir()
    (valid2 / "template.yml").write_text("name: t2")

    invalid = base / "nope"
    invalid.mkdir()

    engine = TemplateEngine(str(base))
    names = engine.list_templates()
    assert set(names) == {"t1", "t2"}
