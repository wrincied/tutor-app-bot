from __future__ import annotations

from typing import Literal

Lang = Literal["ru", "en", "de", "kz", "uk", "by"]

LANGS: tuple[Lang, ...] = ("de", "en", "ru")

_LEGACY_LANG: dict[str, Lang] = {
    "kz": "ru",
    "uk": "ru",
    "by": "ru",
}

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
        "btn_home": "🏠 Главная",
        "btn_profile": "👤 Профиль",
        "btn_language": "🌐 Язык",
        "btn_unlink": "🔕 Отключить бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Да, отключить",
        "btn_cancel": "Отмена",
        "welcome": "Привет{name}! Меню ниже — занятия, оплата и главная.",
        "tutor_line": "Репетитор: {name}",
        "need_link": "Открой персональную ссылку от репетитора, чтобы подключить бота.",
        "not_linked": "Сначала подключись по ссылке от репетитора.",
        "lessons_empty": "Пока нет прошедших занятий.",
        "lessons_title": "Последние занятия:",
        "lessons_screen_title": "Занятия",
        "payment_title": "Оплата",
        "payment_screen_title": "Оплата",
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
        "home_title": "Главная",
        "home_greeting": "Привет, {name}!",
        "home_greeting_anon": "Привет!",
        "home_subject": "Предмет: {subject}",
        "home_rate": "Ставка: {rate}",
        "home_balance": "Баланс: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Репетитор: {name}",
        "home_announcement_vacation": "Отпуск: {text}",
        "pick_lang": "Выбери язык интерфейса:",
        "lang_set": "Язык сохранён: {flag} {label}",
        "unlink_confirm": "Отключить бота? Репетитор получит уведомление, что ты отвязал Telegram.",
        "unlinked": "Бот отключён. Чтобы снова получать уведомления — открой новую ссылку от репетитора.",
        "error": "Не удалось загрузить данные. Попробуй позже.",
        "menu_hint": "Выбери раздел в меню ниже.",
        "vacation_title": "Отпуск",
        "vacation_default": "Репетитор в отпуске до {end_date}. Ответит после возвращения.",
        "vacation_default_no_date": "Репетитор сейчас в отпуске. Ответит после возвращения.",
        "brand_title": "Simple4U",
        "footer_brand": "© Simple4U",
        "notify_unit_lesson_one": "занятие",
        "notify_balance_changed_title": "Баланс изменён",
        "notify_balance_changed_delta": "{before} → {after} {unit}.",
        "notify_balance_remaining": "Осталось {count} {unit}.",
        "notify_balance_reason": "Причина: {reason}.",
        "notify_balance_package_title": "Баланс пакета",
        "notify_balance_package_body": "В пакете осталось {count} {unit}.",
        "balance_reason_no_show": "неявка на урок",
        "balance_reason_bonus": "бонусное занятие",
        "balance_reason_typo": "исправление",
        "notify_payment_title": "Оплата получена",
        "notify_payment_body": "{amount} · {delta}. {thanks}",
        "notify_payment_thanks": "Спасибо!",
        "notify_lesson_start_title": "Скоро урок",
        "notify_lesson_start_body": "Через {minutes} минут начинается урок{with_tutor} · {time}",
        "notify_lesson_start_with_tutor": " с {name}",
        "notify_meeting_link": "Ссылка на звонок",
        "notify_homework_title": "Домашнее задание",
        "notify_lesson_moved_title": "Урок перенесён",
        "notify_lesson_moved_body": "Новое время{who}: {time}",
        "notify_lesson_moved_who": " ({name})",
        "welcome_linked_hello": "Привет, {name}!",
        "welcome_linked_hello_anon": "Привет!",
        "welcome_linked_subtitle": "{hello} Уведомления подключены.",
        "welcome_linked_tutor": "Твой репетитор: {name}.",
        "welcome_linked_body": "Сюда будут приходить баланс, оплата, старт урока и домашка.",
        "welcome_need_link_hello": "Привет! Я бот Simple4U.",
        "welcome_need_link_body": "Открой персональную ссылку от репетитора, чтобы получать уведомления.",
    },
    "en": {
        "btn_lessons": "📚 Lessons",
        "btn_payment": "💳 Payments",
        "btn_home": "🏠 Home",
        "btn_profile": "👤 Profile",
        "btn_language": "🌐 Language",
        "btn_unlink": "🔕 Disable bot",
        "btn_back": "⬅️ Back",
        "btn_confirm_unlink": "Yes, disable",
        "btn_cancel": "Cancel",
        "welcome": "Hi{name}! Use the menu for lessons, payments and home.",
        "tutor_line": "Tutor: {name}",
        "need_link": "Open your personal invite link from your tutor to connect.",
        "not_linked": "Connect via your tutor’s invite link first.",
        "lessons_empty": "No past lessons yet.",
        "lessons_title": "Recent lessons:",
        "lessons_screen_title": "Lessons",
        "payment_title": "Payments",
        "payment_screen_title": "Payments",
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
        "home_title": "Home",
        "home_greeting": "Hi, {name}!",
        "home_greeting_anon": "Hi!",
        "home_subject": "Subject: {subject}",
        "home_rate": "Rate: {rate}",
        "home_balance": "Balance: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Tutor: {name}",
        "home_announcement_vacation": "Away: {text}",
        "pick_lang": "Choose interface language:",
        "lang_set": "Language saved: {flag} {label}",
        "unlink_confirm": "Disable the bot? Your tutor will be notified that you unlinked Telegram.",
        "unlinked": "Bot disabled. To reconnect, open a new invite link from your tutor.",
        "error": "Could not load data. Try again later.",
        "menu_hint": "Pick a section from the menu below.",
        "vacation_title": "Away",
        "vacation_default": "Your tutor is away until {end_date} and will reply when back.",
        "vacation_default_no_date": "Your tutor is away and will reply when back.",
        "brand_title": "Simple4U",
        "footer_brand": "© Simple4U",
        "notify_unit_lesson_one": "lesson",
        "notify_balance_changed_title": "Balance updated",
        "notify_balance_changed_delta": "{before} → {after} {unit}.",
        "notify_balance_remaining": "{count} {unit} remaining.",
        "notify_balance_reason": "Reason: {reason}.",
        "notify_balance_package_title": "Package balance",
        "notify_balance_package_body": "{count} {unit} left in your package.",
        "balance_reason_no_show": "no-show",
        "balance_reason_bonus": "bonus lesson",
        "balance_reason_typo": "correction",
        "notify_payment_title": "Payment received",
        "notify_payment_body": "{amount} · {delta}. {thanks}",
        "notify_payment_thanks": "Thank you!",
        "notify_lesson_start_title": "Lesson soon",
        "notify_lesson_start_body": "Lesson{with_tutor} starts in {minutes} min · {time}",
        "notify_lesson_start_with_tutor": " with {name}",
        "notify_meeting_link": "Call link",
        "notify_homework_title": "Homework",
        "notify_lesson_moved_title": "Lesson rescheduled",
        "notify_lesson_moved_body": "New time{who}: {time}",
        "notify_lesson_moved_who": " ({name})",
        "welcome_linked_hello": "Hi, {name}!",
        "welcome_linked_hello_anon": "Hi!",
        "welcome_linked_subtitle": "{hello} Notifications are on.",
        "welcome_linked_tutor": "Your tutor: {name}.",
        "welcome_linked_body": "Balance, payments, lesson start and homework will appear here.",
        "welcome_need_link_hello": "Hi! I'm the Simple4U bot.",
        "welcome_need_link_body": "Open your personal invite link from your tutor to get notifications.",
    },
    "de": {
        "btn_lessons": "📚 Unterricht",
        "btn_payment": "💳 Zahlung",
        "btn_home": "🏠 Start",
        "btn_profile": "👤 Profil",
        "btn_language": "🌐 Sprache",
        "btn_unlink": "🔕 Bot deaktivieren",
        "btn_back": "⬅️ Zurück",
        "btn_confirm_unlink": "Ja, deaktivieren",
        "btn_cancel": "Abbrechen",
        "welcome": "Hallo{name}! Menü: Unterricht, Zahlung und Start.",
        "tutor_line": "Tutor: {name}",
        "need_link": "Öffne den persönlichen Link deines Tutors, um den Bot zu verbinden.",
        "not_linked": "Bitte zuerst über den Einladungslink verbinden.",
        "lessons_empty": "Noch keine vergangenen Stunden.",
        "lessons_title": "Letzte Stunden:",
        "lessons_screen_title": "Unterricht",
        "payment_title": "Zahlung",
        "payment_screen_title": "Zahlung",
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
        "home_title": "Start",
        "home_greeting": "Hallo, {name}!",
        "home_greeting_anon": "Hallo!",
        "home_subject": "Fach: {subject}",
        "home_rate": "Satz: {rate}",
        "home_balance": "Saldo: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Tutor: {name}",
        "home_announcement_vacation": "Abwesenheit: {text}",
        "pick_lang": "Sprache wählen:",
        "lang_set": "Sprache gespeichert: {flag} {label}",
        "unlink_confirm": "Bot deaktivieren? Dein Tutor wird benachrichtigt.",
        "unlinked": "Bot deaktiviert. Für neue Nachrichten brauchst du einen neuen Link.",
        "error": "Daten konnten nicht geladen werden.",
        "menu_hint": "Wähle einen Bereich im Menü.",
        "vacation_title": "Abwesenheit",
        "vacation_default": "Dein Tutor ist bis {end_date} abwesend und meldet sich danach.",
        "vacation_default_no_date": "Dein Tutor ist derzeit abwesend und meldet sich danach.",
        "brand_title": "Simple4U",
        "footer_brand": "© Simple4U",
        "notify_unit_lesson_one": "Unterricht",
        "notify_balance_changed_title": "Saldo geändert",
        "notify_balance_changed_delta": "{before} → {after} {unit}.",
        "notify_balance_remaining": "Noch {count} {unit}.",
        "notify_balance_reason": "Grund: {reason}.",
        "notify_balance_package_title": "Paket-Saldo",
        "notify_balance_package_body": "Noch {count} {unit} im Paket.",
        "balance_reason_no_show": "Nichterscheinen",
        "balance_reason_bonus": "Bonus-Stunde",
        "balance_reason_typo": "Korrektur",
        "notify_payment_title": "Zahlung erhalten",
        "notify_payment_body": "{amount} · {delta}. {thanks}",
        "notify_payment_thanks": "Danke!",
        "notify_lesson_start_title": "Bald Unterricht",
        "notify_lesson_start_body": "In {minutes} Min. beginnt der Unterricht{with_tutor} · {time}",
        "notify_lesson_start_with_tutor": " mit {name}",
        "notify_meeting_link": "Link zum Anruf",
        "notify_homework_title": "Hausaufgabe",
        "notify_lesson_moved_title": "Unterricht verschoben",
        "notify_lesson_moved_body": "Neue Zeit{who}: {time}",
        "notify_lesson_moved_who": " ({name})",
        "welcome_linked_hello": "Hallo, {name}!",
        "welcome_linked_hello_anon": "Hallo!",
        "welcome_linked_subtitle": "{hello} Benachrichtigungen sind aktiv.",
        "welcome_linked_tutor": "Dein Tutor: {name}.",
        "welcome_linked_body": "Hier erscheinen Saldo, Zahlung, Unterrichtsstart und Hausaufgaben.",
        "welcome_need_link_hello": "Hallo! Ich bin der Simple4U-Bot.",
        "welcome_need_link_body": "Öffne den persönlichen Link deines Tutors, um Benachrichtigungen zu erhalten.",
    },
    "kz": {
        "btn_lessons": "📚 Сабақтар",
        "btn_payment": "💳 Төлем",
        "btn_home": "🏠 Басты",
        "btn_profile": "👤 Профиль",
        "btn_language": "🌐 Тіл",
        "btn_unlink": "🔕 Ботты өшіру",
        "btn_back": "⬅️ Артқа",
        "btn_confirm_unlink": "Иә, өшіру",
        "btn_cancel": "Болдырмау",
        "welcome": "Сәлем{name}! Мәзір: сабақтар, төлем және басты.",
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
        "home_title": "Басты",
        "home_greeting": "Сәлем, {name}!",
        "home_greeting_anon": "Сәлем!",
        "home_subject": "Пән: {subject}",
        "home_rate": "Баға: {rate}",
        "home_balance": "Баланс: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Репетитор: {name}",
        "home_announcement_vacation": "Демалыс: {text}",
        "pick_lang": "Тілді таңдаңыз:",
        "lang_set": "Тіл сақталды: {flag} {label}",
        "unlink_confirm": "Ботты өшіру? Репетиторға хабарлама барады.",
        "unlinked": "Бот өшірілді. Қайта қосу үшін жаңа сілтеме керек.",
        "error": "Деректер жүктелмеді.",
        "menu_hint": "Мәзірден бөлімді таңдаңыз.",
        "vacation_title": "Демалыс",
        "vacation_default": "Тьютор {end_date} дейін демалыста. Оралған соң жауап береді.",
        "vacation_default_no_date": "Тьютор қазір демалыста. Оралған соң жауап береді.",
    },
    "uk": {
        "btn_lessons": "📚 Заняття",
        "btn_payment": "💳 Оплата",
        "btn_home": "🏠 Головна",
        "btn_profile": "👤 Профіль",
        "btn_language": "🌐 Мова",
        "btn_unlink": "🔕 Вимкнути бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Так, вимкнути",
        "btn_cancel": "Скасувати",
        "welcome": "Привіт{name}! Меню — заняття, оплата та головна.",
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
        "home_title": "Головна",
        "home_greeting": "Привіт, {name}!",
        "home_greeting_anon": "Привіт!",
        "home_subject": "Предмет: {subject}",
        "home_rate": "Ставка: {rate}",
        "home_balance": "Баланс: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Репетитор: {name}",
        "home_announcement_vacation": "Відпустка: {text}",
        "pick_lang": "Обери мову:",
        "lang_set": "Мову збережено: {flag} {label}",
        "unlink_confirm": "Вимкнути бота? Репетитор отримає сповіщення.",
        "unlinked": "Бота вимкнено. Для повторного підключення потрібне нове посилання.",
        "error": "Не вдалося завантажити дані.",
        "menu_hint": "Обери розділ у меню.",
        "vacation_title": "Відпустка",
        "vacation_default": "Репетитор у відпустці до {end_date}. Відповість після повернення.",
        "vacation_default_no_date": "Репетитор зараз у відпустці. Відповість після повернення.",
    },
    "by": {
        "btn_lessons": "📚 Заняткі",
        "btn_payment": "💳 Аплата",
        "btn_home": "🏠 Галоўная",
        "btn_profile": "👤 Профіль",
        "btn_language": "🌐 Мова",
        "btn_unlink": "🔕 Адключыць бота",
        "btn_back": "⬅️ Назад",
        "btn_confirm_unlink": "Так, адключыць",
        "btn_cancel": "Адмена",
        "welcome": "Прывітанне{name}! Меню — заняткі, аплата і галоўная.",
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
        "home_title": "Галоўная",
        "home_greeting": "Прывітанне, {name}!",
        "home_greeting_anon": "Прывітанне!",
        "home_subject": "Прадмет: {subject}",
        "home_rate": "Стаўка: {rate}",
        "home_balance": "Баланс: {balance}",
        "home_balance_package": "{money} ({count} {unit})",
        "home_balance_postpaid": "{money} ({count} {unit})",
        "home_tutor": "Рэпетытар: {name}",
        "home_announcement_vacation": "Адпачынак: {text}",
        "pick_lang": "Абяры мову:",
        "lang_set": "Мову захавана: {flag} {label}",
        "unlink_confirm": "Адключыць бота? Рэпетытар атрымае апавяшчэнне.",
        "unlinked": "Бот адключаны. Для паўторнага падключэння патрэбна новая спасылка.",
        "error": "Не атрымалася загрузіць даныя.",
        "menu_hint": "Абяры раздзел у меню.",
        "vacation_title": "Адпачынак",
        "vacation_default": "Рэпетитор у адпачынку да {end_date}. Адкажэ пасля вяртання.",
        "vacation_default_no_date": "Рэпетитор зараз у адпачынку. Адкажэ пасля вяртання.",
    },
}


def normalize_lang(raw: str | None) -> Lang:
    value = (raw or "ru").strip().lower()
    if value in _LEGACY_LANG:
        return _LEGACY_LANG[value]
    if value in LANG_META:
        return value  # type: ignore[return-value]
    return "ru"


def t(lang: str | None, key: str) -> str:
    code = normalize_lang(lang)
    return TEXTS[code].get(key) or TEXTS["ru"].get(key) or key


def unit_word(lang: str | None, rate_unit: str | None, *, plural: bool = True) -> str:
    if (rate_unit or "").strip().lower() == "lesson":
        key = "balance_unit_lesson" if plural else "notify_unit_lesson_one"
        return t(lang, key)
    return t(lang, "balance_unit_hour")


def balance_reason_label(lang: str | None, reason: str | None) -> str | None:
    key = f"balance_reason_{(reason or '').strip().lower()}"
    label = t(lang, key)
    if label == key:
        return None
    return label


def status_label(lang: str | None, status: str) -> str:
    code = normalize_lang(lang)
    return STATUS_LABEL[code].get(status) or status
