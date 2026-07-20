from __future__ import annotations

from typing import Literal

Lang = Literal["ru", "en", "de", "kz", "uk", "by"]

LANGS: tuple[Lang, ...] = ("de", "en", "by", "uk", "ru", "kz")

LANG_META: dict[Lang, dict[str, str]] = {
    "de": {"flag": "🇩🇪", "label": "Deutsch"},
    "en": {"flag": "🇬🇧", "label": "English"},
    "by": {"flag": "🇧🇾", "label": "Беларуская"},
    "uk": {"flag": "🇺🇦", "label": "Українська"},
    "ru": {"flag": "🇷🇺", "label": "Русский"},
    "kz": {"flag": "🇰🇿", "label": "Қазақша"},
}

STATUS_LABEL: dict[Lang, dict[str, str]] = {
    "ru": {
        "scheduled": "запланирован",
        "completed": "проведён",
        "missed": "пропущен",
        "canceled": "отменён",
    },
    "en": {
        "scheduled": "scheduled",
        "completed": "completed",
        "missed": "missed",
        "canceled": "canceled",
    },
    "de": {
        "scheduled": "geplant",
        "completed": "durchgeführt",
        "missed": "verpasst",
        "canceled": "abgesagt",
    },
    "kz": {
        "scheduled": "жоспарланған",
        "completed": "өткізілді",
        "missed": "өткізілмеді",
        "canceled": "болдырылмады",
    },
    "uk": {
        "scheduled": "заплановано",
        "completed": "проведено",
        "missed": "пропущено",
        "canceled": "скасовано",
    },
    "by": {
        "scheduled": "запланаваны",
        "completed": "праведзены",
        "missed": "прапушчаны",
        "canceled": "скасаваны",
    },
}

TEXTS: dict[Lang, dict[str, str]] = {
    "ru": {
        "btn_lessons": "📚 Занятия",
        "btn_payment": "💳 Оплата",
        "btn_profile": "👤 Профиль",
        "btn_language": "🌐 Язык",
        "btn_unlink": "🔕 Отключить бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Да, отключить",
        "btn_cancel": "Отмена",
        "welcome": "Привет{name}! Меню ниже — занятия, оплата и профиль.",
        "tutor_line": "Репетитор: {name}",
        "need_link": "Открой персональную ссылку от репетитора, чтобы подключить бота.",
        "not_linked": "Сначала подключись по ссылке от репетитора.",
        "lessons_empty": "Пока нет прошедших занятий.",
        "lessons_title": "Последние занятия:",
        "payment_title": "Оплата",
        "payment_package": (
            "Оплачено (пополнено): {topped} {balance_unit}\n"
            "Проведено: {completed} занятий\n"
            "Осталось: {balance} {balance_unit}\n"
            "Ставка: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Проведено: {completed} занятий\n"
            "К оплате (долг): {unpaid} {balance_unit}\n"
            "Лимит долга: {credit} {balance_unit}\n"
            "Ставка: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/час",
        "rate_unit_lesson": "/занятие",
        "balance_unit_hour": "ч",
        "balance_unit_lesson": "занятий",
        "profile_title": "Профиль",
        "profile_lang": "Язык: {flag} {label}",
        "pick_lang": "Выбери язык интерфейса:",
        "lang_set": "Язык сохранён: {flag} {label}",
        "unlink_confirm": "Отключить бота? Репетитор получит уведомление, что ты отвязал Telegram.",
        "unlinked": "Бот отключён. Чтобы снова получать уведомления — открой новую ссылку от репетитора.",
        "error": "Не удалось загрузить данные. Попробуй позже.",
        "menu_hint": "Выбери раздел в меню ниже.",
    },
    "en": {
        "btn_lessons": "📚 Lessons",
        "btn_payment": "💳 Payments",
        "btn_profile": "👤 Profile",
        "btn_language": "🌐 Language",
        "btn_unlink": "🔕 Disable bot",
        "btn_back": "⬅️ Back",
        "btn_confirm_unlink": "Yes, disable",
        "btn_cancel": "Cancel",
        "welcome": "Hi{name}! Use the menu for lessons, payments and profile.",
        "tutor_line": "Tutor: {name}",
        "need_link": "Open your personal invite link from your tutor to connect.",
        "not_linked": "Connect via your tutor’s invite link first.",
        "lessons_empty": "No past lessons yet.",
        "lessons_title": "Recent lessons:",
        "payment_title": "Payments",
        "payment_package": (
            "Topped up: {topped} {balance_unit}\n"
            "Completed: {completed} lessons\n"
            "Remaining: {balance} {balance_unit}\n"
            "Rate: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Completed: {completed} lessons\n"
            "Due: {unpaid} {balance_unit}\n"
            "Debt limit: {credit} {balance_unit}\n"
            "Rate: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/hour",
        "rate_unit_lesson": "/lesson",
        "balance_unit_hour": "h",
        "balance_unit_lesson": "lessons",
        "profile_title": "Profile",
        "profile_lang": "Language: {flag} {label}",
        "pick_lang": "Choose interface language:",
        "lang_set": "Language saved: {flag} {label}",
        "unlink_confirm": "Disable the bot? Your tutor will be notified that you unlinked Telegram.",
        "unlinked": "Bot disabled. To reconnect, open a new invite link from your tutor.",
        "error": "Could not load data. Try again later.",
        "menu_hint": "Pick a section from the menu below.",
    },
    "de": {
        "btn_lessons": "📚 Unterricht",
        "btn_payment": "💳 Zahlung",
        "btn_profile": "👤 Profil",
        "btn_language": "🌐 Sprache",
        "btn_unlink": "🔕 Bot deaktivieren",
        "btn_back": "⬅️ Zurück",
        "btn_confirm_unlink": "Ja, deaktivieren",
        "btn_cancel": "Abbrechen",
        "welcome": "Hallo{name}! Menü: Unterricht, Zahlung und Profil.",
        "tutor_line": "Tutor: {name}",
        "need_link": "Öffne den persönlichen Link deines Tutors, um den Bot zu verbinden.",
        "not_linked": "Bitte zuerst über den Einladungslink verbinden.",
        "lessons_empty": "Noch keine vergangenen Stunden.",
        "lessons_title": "Letzte Stunden:",
        "payment_title": "Zahlung",
        "payment_package": (
            "Aufgeladen: {topped} {balance_unit}\n"
            "Durchgeführt: {completed} Stunden\n"
            "Übrig: {balance} {balance_unit}\n"
            "Satz: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Durchgeführt: {completed} Stunden\n"
            "Offen: {unpaid} {balance_unit}\n"
            "Limit: {credit} {balance_unit}\n"
            "Satz: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/Std.",
        "rate_unit_lesson": "/Unterricht",
        "balance_unit_hour": "Std.",
        "balance_unit_lesson": "Unterricht",
        "profile_title": "Profil",
        "profile_lang": "Sprache: {flag} {label}",
        "pick_lang": "Sprache wählen:",
        "lang_set": "Sprache gespeichert: {flag} {label}",
        "unlink_confirm": "Bot deaktivieren? Dein Tutor wird benachrichtigt.",
        "unlinked": "Bot deaktiviert. Für neue Nachrichten brauchst du einen neuen Link.",
        "error": "Daten konnten nicht geladen werden.",
        "menu_hint": "Wähle einen Bereich im Menü.",
    },
    "kz": {
        "btn_lessons": "📚 Сабақтар",
        "btn_payment": "💳 Төлем",
        "btn_profile": "👤 Профиль",
        "btn_language": "🌐 Тіл",
        "btn_unlink": "🔕 Ботты өшіру",
        "btn_back": "⬅️ Артқа",
        "btn_confirm_unlink": "Иә, өшіру",
        "btn_cancel": "Болдырмау",
        "welcome": "Сәлем{name}! Мәзір: сабақтар, төлем және профиль.",
        "tutor_line": "Репетитор: {name}",
        "need_link": "Репетитор сілтемесі арқылы ботты қосыңыз.",
        "not_linked": "Алдымен сілтеме арқылы қосылыңыз.",
        "lessons_empty": "Өткен сабақтар жоқ.",
        "lessons_title": "Соңғы сабақтар:",
        "payment_title": "Төлем",
        "payment_package": (
            "Толтырылған: {topped} {balance_unit}\n"
            "Өткізілген: {completed} сабақ\n"
            "Қалды: {balance} {balance_unit}\n"
            "Баға: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Өткізілген: {completed} сабақ\n"
            "Қарыз: {unpaid} {balance_unit}\n"
            "Шек: {credit} {balance_unit}\n"
            "Баға: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/сағат",
        "rate_unit_lesson": "/сабақ",
        "balance_unit_hour": "сағ",
        "balance_unit_lesson": "сабақ",
        "profile_title": "Профиль",
        "profile_lang": "Тіл: {flag} {label}",
        "pick_lang": "Тілді таңдаңыз:",
        "lang_set": "Тіл сақталды: {flag} {label}",
        "unlink_confirm": "Ботты өшіру? Репетиторға хабарлама барады.",
        "unlinked": "Бот өшірілді. Қайта қосу үшін жаңа сілтеме керек.",
        "error": "Деректер жүктелмеді.",
        "menu_hint": "Мәзірден бөлімді таңдаңыз.",
    },
    "uk": {
        "btn_lessons": "📚 Заняття",
        "btn_payment": "💳 Оплата",
        "btn_profile": "👤 Профіль",
        "btn_language": "🌐 Мова",
        "btn_unlink": "🔕 Вимкнути бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Так, вимкнути",
        "btn_cancel": "Скасувати",
        "welcome": "Привіт{name}! Меню — заняття, оплата та профіль.",
        "tutor_line": "Репетитор: {name}",
        "need_link": "Відкрий персональне посилання від репетитора.",
        "not_linked": "Спочатку підключися за посиланням.",
        "lessons_empty": "Поки немає минулих занять.",
        "lessons_title": "Останні заняття:",
        "payment_title": "Оплата",
        "payment_package": (
            "Поповнено: {topped} {balance_unit}\n"
            "Проведено: {completed} занять\n"
            "Залишилось: {balance} {balance_unit}\n"
            "Ставка: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Проведено: {completed} занять\n"
            "Борг: {unpaid} {balance_unit}\n"
            "Ліміт: {credit} {balance_unit}\n"
            "Ставка: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/год",
        "rate_unit_lesson": "/заняття",
        "balance_unit_hour": "год",
        "balance_unit_lesson": "занять",
        "profile_title": "Профіль",
        "profile_lang": "Мова: {flag} {label}",
        "pick_lang": "Обери мову:",
        "lang_set": "Мову збережено: {flag} {label}",
        "unlink_confirm": "Вимкнути бота? Репетитор отримає сповіщення.",
        "unlinked": "Бота вимкнено. Для повторного підключення потрібне нове посилання.",
        "error": "Не вдалося завантажити дані.",
        "menu_hint": "Обери розділ у меню.",
    },
    "by": {
        "btn_lessons": "📚 Заняткі",
        "btn_payment": "💳 Аплата",
        "btn_profile": "👤 Профіль",
        "btn_language": "🌐 Мова",
        "btn_unlink": "🔕 Адключыць бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Так, адключыць",
        "btn_cancel": "Адмена",
        "welcome": "Прывітанне{name}! Меню — заняткі, аплата і профіль.",
        "tutor_line": "Рэпетытар: {name}",
        "need_link": "Адкрый персанальную спасылку ад рэпетытара.",
        "not_linked": "Спачатку падключыся па спасылцы.",
        "lessons_empty": "Пакуль няма мінулых заняткаў.",
        "lessons_title": "Апошнія заняткі:",
        "payment_title": "Аплата",
        "payment_package": (
            "Папоўнена: {topped} {balance_unit}\n"
            "Праведзена: {completed} заняткаў\n"
            "Засталося: {balance} {balance_unit}\n"
            "Стаўка: {rate} {currency}{rate_unit}"
        ),
        "payment_postpaid": (
            "Праведзена: {completed} заняткаў\n"
            "Доўг: {unpaid} {balance_unit}\n"
            "Ліміт: {credit} {balance_unit}\n"
            "Стаўка: {rate} {currency}{rate_unit}"
        ),
        "rate_unit_hour": "/гадзіну",
        "rate_unit_lesson": "/занятак",
        "balance_unit_hour": "гадз",
        "balance_unit_lesson": "заняткаў",
        "profile_title": "Профіль",
        "profile_lang": "Мова: {flag} {label}",
        "pick_lang": "Абяры мову:",
        "lang_set": "Мову захавана: {flag} {label}",
        "unlink_confirm": "Адключыць бота? Рэпетытар атрымае апавяшчэнне.",
        "unlinked": "Бот адключаны. Для паўторнага падключэння патрэбна новая спасылка.",
        "error": "Не атрымалася загрузіць даныя.",
        "menu_hint": "Абяры раздзел у меню.",
    },
}


def normalize_lang(raw: str | None) -> Lang:
    value = (raw or "ru").strip().lower()
    if value in LANG_META:
        return value  # type: ignore[return-value]
    return "ru"


def t(lang: str | None, key: str) -> str:
    code = normalize_lang(lang)
    return TEXTS[code].get(key) or TEXTS["ru"].get(key) or key


def status_label(lang: str | None, status: str) -> str:
    code = normalize_lang(lang)
    return STATUS_LABEL[code].get(status) or status
