from simple4u_bot.services.translate import translate_target


def test_translate_target_mapping() -> None:
    assert translate_target("en") == "en"
    assert translate_target("de") == "de"
    assert translate_target("by") == "be"
    assert translate_target("kz") == "kk"
    assert translate_target(None) is None
