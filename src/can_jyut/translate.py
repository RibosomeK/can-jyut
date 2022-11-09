import warnings, locale, gettext

warnings.simplefilter("ignore")

lang: list[str] | None
if locate := locale.getdefaultlocale()[0]:
    lang = [locate]
else:
    lang = None
translator = gettext.translation(
    "base", localedir="./locales", languages=lang, fallback=True
)
translator.install()
tr = translator.gettext
