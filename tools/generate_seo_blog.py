#!/usr/bin/env python3
"""Generate 50 SEO blog articles + blog.html + sitemap.xml for ekaterina-site."""
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

SITE = "https://xn----7sbanvcabqhfqljbckzlp0dn.xn--p1ai"
OG_IMAGE = f"{SITE}/img/ekaterina.jpg"
TODAY = "2026-07-06"
ROOT = Path(__file__).resolve().parent.parent

EXISTING = [
    {
        "slug": "trevoga-bez-prichiny",
        "title": "Тревога без причины — почему возникает и что делать",
        "desc": "Откуда берётся постоянное беспокойство, что помогает в моменте и когда пора к специалисту.",
        "category": "Тревога и стресс",
        "date": "2026-06-27",
    },
    {
        "slug": "emocionalnoe-vygoranie",
        "title": "Эмоциональное выгорание: признаки и как восстановиться",
        "desc": "Признаки выгорания, отличие от усталости и депрессии и что помогает восстановиться.",
        "category": "Работа и выгорание",
        "date": "2026-06-27",
    },
    {
        "slug": "kogda-obratitsya-k-psihologu",
        "title": "Когда стоит обратиться к психологу",
        "desc": "Признаки, по которым стоит обратиться, мифы о терапии и с чего начать.",
        "category": "О терапии",
        "date": "2026-06-27",
    },
    {
        "slug": "blog-pervaya-konsultaciya",
        "title": "Как проходит первая консультация у психолога",
        "desc": "Чего ждать, как подготовиться, что спросить на ознакомительной встрече.",
        "category": "О терапии",
        "date": "2026-06-05",
    },
]

LANDINGS = [
    ("", "weekly", "1.0"),
    ("psiholog-novosibirsk.html", "monthly", "0.9"),
    ("contacts.html", "yearly", "0.8"),
    ("blog.html", "weekly", "0.7"),
    ("gruppovoy-psihoanaliz.html", "monthly", "0.9"),
    ("psiholog-online.html", "monthly", "0.9"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def section_block(title: str, body_html: str) -> str:
    return f'          <div class="reveal">\n            <h2>{esc(title)}</h2>\n{body_html}\n          </div>'


def p(text: str) -> str:
    return f"            <p>{text}</p>"


def ul(items: list[str]) -> str:
    lines = "\n".join(f"<li>{esc(x)}</li>" for x in items)
    return f"            <ul>{lines}</ul>"


def build_sections(topic: str, kind: str) -> list[tuple[str, str]]:
    t = topic
    cta = (
        ' Можно начать с бесплатной <a href="/psiholog-online.html">ознакомительной встречи онлайн</a> '
        'или очной консультации в <a href="/psiholog-novosibirsk.html">Новосибирске</a>.'
    )
    if kind == "anxiety":
        return [
            (
                f"Что такое {t.lower()}",
                p(
                    f"{t} — это не «слабость характера» и не выдумка. Это сигнал нервной системы о перегрузке, "
                    f"неопределённости или накопившемся напряжении. Важно отличать разовую реакцию на событие "
                    f"и устойчивое состояние, которое мешает спать, работать и общаться."
                ),
            ),
            (
                "Как это может проявляться",
                ul(
                    [
                        "напряжение в теле, учащённое сердцебиение, ком в горле;",
                        "навязчивые мысли «а вдруг случится…»;",
                        "избегание ситуаций, мест или людей;",
                        "раздражительность, проблемы со сном и концентрацией.",
                    ]
                ),
            ),
            (
                "Почему это возникает",
                p(
                    "Причины обычно сочетаются: хронический стресс, непрожитые переживания, высокие требования к себе, "
                    "травматичный опыт, изменения в жизни. Психика пытается защититься — но способ защиты начинает мешать. "
                    "В терапии мы исследуем не только симптом, но и то, что за ним стоит."
                ),
            ),
            (
                "Что можно сделать самостоятельно",
                ul(
                    [
                        "Замечать триггеры: время суток, люди, мысли перед обострением.",
                        "Дыхание и заземление: медленный выдох, контакт стоп с полом, холодная вода для лица.",
                        "Снижать перегруз: сон, паузы, меньше новостей и doom-scrolling перед сном.",
                        "Не ругать себя за тревогу — это усиливает напряжение.",
                    ]
                ),
            ),
            (
                "Когда нужен психолог",
                p(
                    f"Если {t.lower()} длятся неделями, мешают работе, отношениям или сну — это повод обратиться. "
                    f"Не нужно ждать «дна»: чем раньше начата работа, тем легче восстановить опору."
                    + cta
                ),
            ),
        ]
    if kind == "work":
        return [
            (
                f"О чём этот запрос: {t.lower()}",
                p(
                    f"Тема «{t}» часто приходит на консультацию не как абстракция, а как ощущение: «я больше не вывожу», "
                    f"«всё бессмысленно» или «я застрял». Это не обязательно депрессия — иногда это сигнал о границах, "
                    f"ценностях и реальных условиях, которые пора пересмотреть."
                ),
            ),
            (
                "Типичные признаки",
                ul(
                    [
                        "усталость не проходит после отдыха;",
                        "цинизм, раздражение на коллег или близких;",
                        "ощущение, что вы «притворяетесь» на работе;",
                        "сложно принимать решения, прокрастинация;",
                        "физические симптомы: головные боли, напряжение, бессонница.",
                    ]
                ),
            ),
            (
                "Что часто стоит за этим",
                p(
                    "Перегруз, страх ошибки, перфекционизм, отсутствие признания, конфликт ценностей с компанией, "
                    "невозможность сказать «нет». В психоаналитическом подходе мы смотрим и на текущую ситуацию, "
                    "и на привычные сценарии — как вы обычно справляетесь с давлением."
                ),
            ),
            (
                "Что помогает в первую очередь",
                ul(
                    [
                        "Честно оценить нагрузку: что можно делегировать или убрать.",
                        "Вернуть базовые ресурсы: сон, еда, движение — не «когда будет время», а в календарь.",
                        "Поговорить с близким человеком или специалистом — изоляция усиливает выгорание.",
                        "Разделить «я плохой сотрудник» и «мне тяжело в этих условиях».",
                    ]
                ),
            ),
            (
                "Как помогает терапия",
                p(
                    f"На консультации можно разобрать именно ваш случай: {t.lower()} — это про обстоятельства, "
                    f"про внутренние установки или про оба слоя. Личная терапия и "
                    f'<a href="/gruppovoy-psihoanaliz.html">групповой психоанализ</a> — разные форматы; '
                    f"на ознакомительной встрече можно понять, что подходит вам."
                    + cta
                ),
            ),
        ]
    if kind == "relations":
        return [
            (
                f"Почему тема «{t}» так часто болит",
                p(
                    "Отношения — главная сфера, где мы проверяем свою ценность, безопасность и близость. "
                    "Когда что-то идёт не так, страдает не только пара — страдает самоощущение, сон, работоспособность. "
                    "Обращаться за помощью по этому поводу нормально и часто своевременно."
                ),
            ),
            (
                "Как это может выглядеть в жизни",
                ul(
                    [
                        "частые ссоры по одним и тем же темам;",
                        "ощущение одиночества рядом с партнёром;",
                        "ревность, контроль, страх потери;",
                        "сложность говорить о потребностях и границах;",
                        "мысли о расставании без ясности «что я хочу на самом деле».",
                    ]
                ),
            ),
            (
                "Что важно понимать",
                p(
                    f"Тема «{t}» редко решается только «правильными фразами». Часто в игру вступают старые сценарии: "
                    f"как в семье показывали любовь, можно ли злиться, что делать с обидой. Терапия — это пространство, "
                    f"где можно разложить переживания без стыда и давления «срочно всё починить»."
                ),
            ),
            (
                "Что можно попробовать до терапии",
                ul(
                    [
                        "Замечать, где вы автоматически нападаете или закрываетесь.",
                        "Договориться о паузе в ссоре, а не докричаться до победы.",
                        "Говорить о своих чувствах через «я-сообщения», без обвинений.",
                        "Не принимать решение о расставании в пике эмоций — дать себе время и опору.",
                    ]
                ),
            ),
            (
                "Когда идти к психологу",
                p(
                    "Если цикл повторяется месяцами, есть насилие, выгорание или депрессивные мысли — лучше не откладывать. "
                    "Можно прийти одному: это уже меняет динамику. Пара не обязана идти вместе."
                    + cta
                ),
            ),
        ]
    if kind == "therapy":
        return [
            (
                "Кратко о теме",
                p(
                    f"«{t}» — один из самых частых вопросов на первой консультации. Ответ зависит не только от теории, "
                    f"но и от вашего запроса, темпа жизни и того, насколько вам комфортно в формате разговора один на один "
                    f"или в группе."
                ),
            ),
            (
                "Что важно знать",
                ul(
                    [
                        "Психолог не ставит диагнозы как врач и не назначает лекарства.",
                        "Конфиденциальность — базовое правило (кроме ситуаций угрозы жизни).",
                        "Терапия — это процесс, а не одна «волшебная» сессия.",
                        "Вы можете задавать любые вопросы о формате, стоимости и частоте встреч.",
                    ]
                ),
            ),
            (
                "Как это работает на практике",
                p(
                    "На первой встрече вы формулируете запрос, задаёте вопросы, смотрите, насколько комфортен специалист. "
                    "В психоаналитическом подходе мы исследуем не только симптом, но и связи между мыслями, чувствами "
                    "и повторяющимися ситуациями. Это помогает не просто «пережить кризис», а понять, что вас к нему ведёт."
                ),
            ),
            (
                "Мифы, которые мешают начать",
                ul(
                    [
                        "«Нужно совсем плохо» — можно прийти с тревогой, усталостью, вопросом о себе.",
                        "«Психолог скажет, как жить» — скорее поможет услышать себя.",
                        "«Это слабость» — это забота о ресурсе, как визит к стоматологу.",
                        "«Онлайн не работает» — для многих форматов онлайн-терапия так же эффективна.",
                    ]
                ),
            ),
            (
                "Следующий шаг",
                p(
                    f"Если вас интересует тема «{t.lower()}», логичный шаг — "
                    f'<a href="/blog-pervaya-konsultaciya.html">узнать о первой консультации</a> '
                    f"и записаться на бесплатную ознакомительную встречу."
                    + cta
                ),
            ),
        ]
    if kind == "geo":
        return [
            (
                "Зачем искать психолога в своём городе",
                p(
                    f"{t} — запрос, с которым часто приходят жители Новосибирска и области. "
                    f"Очные встречи удобны, если важен личный контакт; онлайн подходит, если график плотный "
                    f"или вы живёте в другом районе. Оба формата можно совмещать."
                ),
            ),
            (
                "На что обратить внимание при выборе",
                ul(
                    [
                        "Образование и подход: психоанализ, КПТ, гуманистический — важно, чтобы вам откликалось.",
                        "Специализация по запросу: тревога, отношения, выгорание, групповая работа.",
                        "Прозрачность условий: стоимость, длительность, отмена сессии.",
                        "Ощущение безопасности на первой встрече — это главный критерий.",
                    ]
                ),
            ),
            (
                "Как проходит работа",
                p(
                    "Обычно личная терапия — раз в неделю, 50 минут. Групповой психоанализ — по расписанию группы. "
                    "Первая ознакомительная встреча онлайн у меня бесплатная: можно задать вопросы и понять, "
                    "подходит ли формат, не принимая долгосрочных обязательств."
                ),
            ),
            (
                "Частые запросы в Новосибирске",
                ul(
                    [
                        "тревога, панические состояния, бессонница;",
                        "выгорание и кризис на работе;",
                        "отношения, развод, одиночество;",
                        "поиск смысла, самооценка, перфекционизм;",
                        "поддержка в групповой терапии.",
                    ]
                ),
            ),
            (
                "Как записаться",
                p(
                    f"Если вы ищете {t.lower()}, напишите в Telegram или оставьте заявку на сайте. "
                    f"Подберём формат — очно, онлайн или группа."
                    + cta
                ),
            ),
        ]
    # self / default
    return [
        (
            f"Что такое {t.lower()}",
            p(
                f"{t} — состояние или паттерн, с которым люди нередко живут годами, считая его «просто характером». "
                f"На самом деле за этим часто стоят перегруз, старый опыт, неудовлетворённые потребности или "
                f"внутренние конфликты, которые можно исследовать в терапии."
            ),
        ),
        (
            "Признаки, что тема актуальна",
            ul(
                [
                    "повторяющиеся мысли или сценарии, которые сложно остановить;",
                    "сильная самокритика или стыд;",
                    "избегание важных разговоров, дел, отношений;",
                    "ощущение застоя, пустоты или «я не на своём месте»;",
                    "физическое напряжение без явной медицинской причины.",
                ]
            ),
        ),
        (
            "Откуда это берётся",
            p(
                "Редко бывает одна причина. Обычно сочетаются биография, текущий стресс, отношения и способ, "
                "которым вы привыкли справляться. Важно не искать виноватых — ни среди других, ни в себе — "
                "а понять, что сейчас можно изменить."
            ),
        ),
        (
            "Что помогает",
            ul(
                [
                    "Замечать моменты обострения без самообвинения.",
                    "Малые шаги вместо рывка «с понедельника всё изменю».",
                    "Поддержка: близкие, группа, специалист.",
                    "Регулярность заботы о теле: сон, еда, движение.",
                ]
            ),
        ),
        (
            "Когда обращаться к психологу",
            p(
                f"Если {t.lower()} мешает жить, работать, любить — это достаточный повод. "
                f"Не нужно ждать, пока «совсем накроет»."
                + cta
            ),
        ),
    ]


NEW_ARTICLES = [
    ("panicheskie-ataki", "Панические атаки: что делать во время и после", "Как распознать паническую атаку, что делать в моменте, чем отличается от сердечного приступа и когда нужен психолог.", "anxiety", "Тревога и стресс"),
    ("trevoga-pered-snom", "Тревога перед сном: почему мысли не отпускают", "Почему тревога усиливается вечером, как успокоить нервную систему перед сном и когда это повод к специалисту.", "anxiety", "Тревога и стресс"),
    ("sotsialnaya-trevoga", "Социальная тревога: страх оценки и людей", "Как проявляется социальная тревога, почему возникает страх осуждения и что помогает возвращаться в контакт.", "anxiety", "Тревога и стресс"),
    ("trevoga-za-detey", "Тревога за детей: когда это норма, а когда нет", "Родительская тревога: откуда берётся, как не передавать её ребёнку и когда нужна поддержка психолога.", "anxiety", "Тревога и стресс"),
    ("obsesivnye-mysli", "Навязчивые мысли: что это и как с ними жить", "Почему появляются навязчивые мысли, чем они отличаются от фантазий и когда нужна профессиональная помощь.", "anxiety", "Тревога и стресс"),
    ("generalizovannaya-trevoga", "Генерализованная тревога: постоянное беспокойство", "Что такое генерализованная тревога, как она влияет на тело и жизнь и как работает терапия.", "anxiety", "Тревога и стресс"),
    ("strah-budushchego", "Страх будущего и неопределённости", "Почему мы тревожимся о том, чего ещё нет, и как вернуть опору в настоящем.", "anxiety", "Тревога и стресс"),
    ("trevoga-posle-stressa", "Тревога после сильного стресса", "Как организм реагирует на перегруз, почему тревога остаётся после события и что помогает восстановиться.", "anxiety", "Тревога и стресс"),
    ("chronicheskiy-stress", "Хронический стресс: признаки и последствия", "Как распознать хронический стресс до выгорания и что делать, чтобы не довести до истощения.", "work", "Работа и выгорание"),
    ("stress-na-rabote", "Стресс на работе: как не довести до выгорания", "Причины рабочего стресса, телесные сигналы и шаги, которые реально помогают.", "work", "Работа и выгорание"),
    ("konflikt-s-kollegami", "Конфликт с коллегами: как прожить и что делать", "Почему рабочие конфликты так выбивают из колеи и как восстановить границы.", "work", "Работа и выгорание"),
    ("uvolnenie-i-perezhivanie", "Увольнение и переживание потери работы", "Как прожить увольнение, страх неопределённости и возвращение опоры.", "work", "Работа и выгорание"),
    ("ne-lyublyu-rabotu", "Не люблю работу: выгорание или не свой путь", "Как отличить временное истощение от системного несоответствия и что с этим делать.", "work", "Работа и выгорание"),
    ("karernyy-krizis", "Карьерный кризис: когда хочется всё бросить", "Признаки карьерного кризиса, страх изменений и как принимать решения из ясности.", "work", "Работа и выгорание"),
    ("delovoe-vygoranie", "Деловое выгорание у руководителей и предпринимателей", "Особенности выгорания у тех, кто «всё тянет на себе», и пути восстановления.", "work", "Работа и выгорание"),
    ("nizkaya-samootsenka", "Низкая самооценка: откуда берётся и как меняется", "Почему самооценка скачет, как работает внутренний критик и что даёт терапия.", "self", "Самооценка и личность"),
    ("perfektsionizm", "Перфекционизм: когда «хорошо» становится мало", "Как перфекционизм маскируется под ответственность и чем он опасен для жизни.", "self", "Самооценка и личность"),
    ("sindrom-samozvanca", "Синдром самозванца на работе", "Почему успешные люди чувствуют, что их «раскроют», и как с этим работать.", "self", "Самооценка и личность"),
    ("strah-osuzhdeniya", "Страх осуждения: как перестать жить для других", "Откуда берётся страх быть «не таким» и как возвращать опору на себя.", "self", "Самооценка и личность"),
    ("prokrastinaciya", "Прокрастинация: не лень, а сигнал", "Почему откладывание — часто про тревогу, перфекционизм или выгорание.", "self", "Самооценка и личность"),
    ("chuvstvo-viny", "Чувство вины: когда оно помогает, а когда разрушает", "Токсичная и здоровая вина, самонаказание и работа с этим в терапии.", "self", "Самооценка и личность"),
    ("agressiya-i-razdrazhenie", "Раздражительность и скрытая агрессия", "Почему «срываемся» на близких, что стоит за злостью и как её проживать безопасно.", "self", "Самооценка и личность"),
    ("apatiya-i-bessilie", "Апатия и чувство бессилия", "Когда пропадает интерес к жизни, чем апатия отличается от депрессии и что делать.", "self", "Самооценка и личность"),
    ("poterya-smysla", "Потеря смысла в жизни", "Экзистенциальный кризис, пустота и поиск направления — с чего начать.", "self", "Самооценка и личность"),
    ("konflikt-v-pare", "Конфликты в паре: повторяющиеся ссоры", "Почему ссоры ходят по кругу и как прервать цикл без «кто прав».", "relations", "Отношения"),
    ("krizis-v-brake", "Кризис в браке: можно ли сохранить отношения", "Признаки кризиса, когда стоит бороться за связь, а когда — отпустить.", "relations", "Отношения"),
    ("kak-perezhit-rasstavanie", "Как пережить расставание", "Этапы горевания после разрыва, ловушки «быстро забыть» и поддержка.", "relations", "Отношения"),
    ("sozavisimye-otnosheniya", "Созависимые отношения: признаки", "Как распознать созависимость, почему так сложно уйти и с чего начать изменения.", "relations", "Отношения"),
    ("granicy-v-otnosheniyah", "Границы в отношениях: как говорить «нет»", "Почему границы пугают, как их обозначать без агрессии и вины.", "relations", "Отношения"),
    ("revnost-v-otnosheniyah", "Ревность в отношениях: норма или проблема", "Откуда берётся ревность, когда она разрушает пару и как с ней работать.", "relations", "Отношения"),
    ("emotsionalnoe-nasilie", "Эмоциональное насилие: как распознать", "Признаки эмоционального насилия, почему сложно уйти и где искать опору.", "relations", "Отношения"),
    ("odinochestvo-v-pare", "Одиночество в паре", "Почему рядом с партнёром бывает так пусто и что с этим делать.", "relations", "Отношения"),
    ("roditelskoe-vygoranie", "Родительское выгорание", "Признаки выгорания у родителей, вина и восстановление ресурса.", "self", "Семья и дети"),
    ("konflikty-s-podrostkom", "Конфликты с подростком в семье", "Как сохранить контакт, когда «всё не так» и кто может помочь родителю.", "relations", "Семья и дети"),
    ("kak-podderzhat-rebenka", "Как поддержать ребёнка в тревоге", "Что говорить ребёнку при тревоге, чего избегать и когда нужен специалист.", "anxiety", "Семья и дети"),
    ("trevoga-pered-ekzamenami", "Тревога перед экзаменами у подростка и взрослого", "Как справляться с экзаменационной тревогой и не передавать панику.", "anxiety", "Семья и дети"),
    ("razvod-i-deti", "Развод и дети: как пройти период изменений", "Как говорить с ребёнком о разводе, снижать тревогу и беречь себя.", "relations", "Семья и дети"),
    ("chto-takoe-psihoanaliz", "Что такое психоанализ простыми словами", "Основы психоanалитического подхода, чем отличается от советов и самопомощи.", "therapy", "О терапии"),
    ("psihoanaliz-i-kbt", "Психоанализ и КПТ: в чём разница", "Сравнение подходов, кому что может подойти и как выбрать.", "therapy", "О терапии"),
    ("kak-vybrat-psihologa", "Как выбрать психолога в Новосибирске", "Критерии выбора, red flags и как понять «ваш» ли специалист на первой встрече.", "therapy", "О терапии"),
    ("skolko-stoit-psiholog", "Сколько стоит психолог и из чего складывается цена", "Почему цены различаются, что входит в сессию и как планировать бюджет.", "therapy", "О терапии"),
    ("kak-dolgo-hodit-k-psihologu", "Как долго ходят к психологу", "От чего зависит длительность терапии, когда ждать изменений и как не бросать рано.", "therapy", "О терапии"),
    ("konfidentsialnost-terapii", "Конфиденциальность в терапии", "Что остаётся между вами и психологом, исключения и как это обсуждается.", "therapy", "О терапии"),
    ("psiholog-i-psihiatr", "Психолог и психиатр: кому идти", "Разница специалистов, когда нужны лекарства и как они работают вместе.", "therapy", "О терапии"),
    ("gruppovaya-i-lichная-terapiya", "Групповая и личная терапия: что выбрать", "Плюсы и минусы форматов, кому подходит групповой психоанализ.", "therapy", "О терапии"),
    ("psiholog-novosibirsk-rayony", "Психолог в Новосибирске: очно и онлайн", "Как выбрать формат, частые запросы и запись к психологу в НСК.", "geo", "Новосибирск"),
    ("psiholog-akademgorodok", "Психолог для жителей Академгородка", "Онлайн и очные консультации для Академгородка и научного сообщества.", "geo", "Новосибирsk"),
    ("online-terapiya-kak-prohodit", "Онлайн-терапия: как проходит сессия", "Техника, конфиденциальность, эффективность и кому подходит формат.", "therapy", "О терапии"),
    ("psiholog-dlya-zhenshchin", "Психолог для женщин: частые запросы", "Выгорание, отношения, самооценка, материнство — с чем приходят и как помогает терапия.", "self", "Новосибирск"),
    ("psiholog-dlya-muzhchin", "Пsycholog для мужчин: стоит ли идти", "Сtereotipy, стресс, гнев, отношения — почему мужчинам тоже нужна поддержка.", "self", "Новосибирск"),
    ("gore-i-poterya-blizkogo", "Горе и потеря близкого", "Этапы проживания утраты, когда горе «застревает» и как поддерживает терапия.", "self", "Кризисы и потери"),
    ("adaptaciya-posle-pereezda", "Адаптация после переезда", "Одиночество, тревога, потеря опоры после смены города и как к этому адаптироваться.", "self", "Кризисы и потери"),
]

# fix typos in tuples
NEW_ARTICLES = [
    x if x[0] != "ne-lyublyu-rabotu" else (
        "ne-lyublyu-rabotu",
        "Не люблю работу: выгорание или не свой путь",
        "Как отличить временное истощение от системного несоответствия и что с этим делать.",
        "work",
        "Работа и выгорание",
    )
    for x in NEW_ARTICLES
]
NEW_ARTICLES = [
    x if x[0] != "gruppovaya-i-lichная-terapiya" else (
        "gruppovaya-i-lichная-terapiya",
        "Групповая и личная терапия: что выбрать",
        "Плюсы и минусы форматов, кому подходит групповой психоanализ.",
        "therapy",
        "О терапии",
    )
    for x in NEW_ARTICLES
]
NEW_ARTICLES = [
    x if x[0] != "psiholog-akademgorodok" else (
        "psiholog-akademgorodok",
        "Психolog для жителей Академгородка",
        "Онлайн и очные консультации для Академгородка и научного сообщества.",
        "geo",
        "Новосибирск",
    )
    for x in NEW_ARTICLES
]
NEW_ARTICLES = [
    x if x[0] != "psiholog-dlya-muzhchin" else (
        "psiholog-dlya-muzhchin",
        "Психolog для мужчин: стоит ли идти",
        "Сtereotipy, стресс, гнев, отношения — почему мужчинам тоже нужна поддержка.",
        "self",
        "Новосибирск",
    )
    for x in NEW_ARTICLES
]

assert len(NEW_ARTICLES) >= 50, len(NEW_ARTICLES)


def render_article(slug: str, title: str, desc: str, kind: str, pub_date: str) -> str:
    sections = build_sections(title.split(":")[0].split("—")[0].strip(), kind)
    body = "\n".join(section_block(h, b) for h, b in sections)
    url = f"{SITE}/{slug}.html"
    short = title if len(title) <= 60 else title[:57] + "…"
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script>document.documentElement.classList.add("js");</script>

    <title>{esc(title)} — Екатерина Фролова</title>
    <meta name="description" content="{esc(desc)}" />
    <meta name="robots" content="index, follow" />

    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="ru_RU" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{OG_IMAGE}" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />

    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@graph": [
          {{
            "@type": "BreadcrumbList",
            "itemListElement": [
              {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "{SITE}/" }},
              {{ "@type": "ListItem", "position": 2, "name": "Блог", "item": "{SITE}/blog.html" }},
              {{ "@type": "ListItem", "position": 3, "name": {json.dumps(title, ensure_ascii=False)}, "item": "{url}" }}
            ]
          }},
          {{
            "@type": "BlogPosting",
            "headline": {json.dumps(title, ensure_ascii=False)},
            "description": {json.dumps(desc, ensure_ascii=False)},
            "image": "{OG_IMAGE}",
            "datePublished": "{pub_date}",
            "dateModified": "{pub_date}",
            "inLanguage": "ru-RU",
            "mainEntityOfPage": "{url}",
            "author": {{ "@type": "Person", "name": "Екатерина Фролова", "jobTitle": "Психолог, психоanалитик" }},
            "publisher": {{ "@type": "Person", "name": "Екатерина Фролова" }}
          }}
        ]
      }}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#content">Перейти к содержимому</a>

    <header class="header">
      <div class="container header__inner">
        <a class="brand" href="/">
          <span class="brand__role">Психолог</span>
          <span class="brand__name">ЕКАТЕРИНА ФРОЛОВА</span>
        </a>
        <nav class="nav" aria-label="Навигация">
          <a class="nav__link" href="/">Главная</a>
          <a class="nav__link" href="/psiholog-novosibirsk.html">Психолог НСК</a>
          <a class="nav__link nav__link--active" aria-current="page" href="/blog.html">Блог</a>
          <a class="nav__link" href="/contacts.html">Контакты</a>
          <a class="nav__link nav__link--cta" href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Напишите в Telegram</a>
        </nav>
      </div>
    </header>

    <main id="content" class="page">
      <article class="section">
        <div class="container prose">
          <p class="page__kicker"><a href="/blog.html">Блог</a></p>
          <h1 class="page__title">{esc(title)}</h1>
          <p class="page__lead">{esc(desc)}</p>
{body}
          <div class="page__actions">
            <a class="btn btn--primary" href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Записаться на консультацию</a>
            <a class="btn btn--ghost" href="/blog.html">Все статьи</a>
          </div>
        </div>
      </article>
    </main>

    <footer class="footer">
      <div class="container footer__inner">
        <p class="footer__copy">© <span id="year"></span> Екатерина Фролова · психолог, Новосибирск</p>
        <nav class="footer__nav" aria-label="Подвал">
          <a href="/">Главная</a>
          <a href="/psiholog-novosibirsk.html">Психолог НСК</a>
          <a href="/blog.html">Блог</a>
          <a href="/contacts.html">Контакты</a>
          <a href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Telegram</a>
        </nav>
      </div>
    </footer>

    <script>
      document.getElementById("year").textContent = String(new Date().getFullYear());
    </script>

    <!-- Yandex.Metrika counter -->
    <script type="text/javascript">
      (function (m, e, t, r, i, k, a) {{
        m[i] =
          m[i] ||
          function () {{
            (m[i].a = m[i].a || []).push(arguments);
          }};
        m[i].l = 1 * new Date();
        for (var j = 0; j < document.scripts.length; j++) {{
          if (document.scripts[j].src === r) {{
            return;
          }}
        }}
        (k = e.createElement(t)), (a = e.getElementsByTagName(t)[0]), (k.async = 1), (k.src = r), a.parentNode.insertBefore(k, a);
      }})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js?id=109674855", "ym");

      ym(109674855, "init", {{
        ssr: true,
        webvisor: true,
        clickmap: true,
        ecommerce: "dataLayer",
        referrer: document.referrer,
        url: location.href,
        accurateTrackBounce: true,
        trackLinks: true,
      }});
    </script>
    <noscript
      ><div><img src="https://mc.yandex.ru/watch/109674855" style="position: absolute; left: -9999px" alt="" /></div
    ></noscript>
    <!-- /Yandex.Metrika counter -->
  </body>
</html>
"""


def render_blog(all_articles: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {}
    for a in all_articles:
        by_cat.setdefault(a["category"], []).append(a)
    order = [
        "Тревога и стресс",
        "Работа и выгорание",
        "Самооценка и личность",
        "Отношения",
        "Семья и дети",
        "О терапии",
        "Новосибирск",
        "Кризисы и потери",
    ]
    lists = []
    for cat in order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        items = sorted(items, key=lambda x: x["title"])
        lis = "\n".join(
            f"""            <li class="blog-list__item">
              <a class="blog-list__link" href="/{esc(a['slug'])}.html">
                <span class="blog-list__title">{esc(a['title'])}</span>
                <span class="blog-list__desc">{esc(a['desc'])}</span>
              </a>
            </li>"""
            for a in items
        )
        lists.append(f'          <h2 class="blog-category">{esc(cat)}</h2>\n          <ul class="blog-list">\n{lis}\n          </ul>')
    body = "\n".join(lists)
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>Блог психолога — Екатерина Фролова, Новосибирск</title>
    <meta
      name="description"
      content="Более 50 статей о тревоге, отношениях, выгорании, психоанализе и консультациях. Психолог Екатерина Фролова, Новосибирск."
    />
    <meta name="robots" content="index, follow" />

    <link rel="canonical" href="{SITE}/blog.html" />
    <meta property="og:image" content="{OG_IMAGE}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="ru_RU" />
    <meta property="og:title" content="Блог — Екатерина Фролова" />
    <meta property="og:description" content="Статьи о психоanализе, тревоге, отношениях и терапии." />
    <meta property="og:url" content="{SITE}/blog.html" />
    <meta name="twitter:card" content="summary" />

    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <a class="skip-link" href="#content">Перейти к содержимому</a>

    <header class="header">
      <div class="container header__inner">
        <a class="brand" href="/">
          <span class="brand__role">Пsycholog</span>
          <span class="brand__name">ЕКАТЕРИНА ФРОЛОВА</span>
        </a>
        <nav class="nav" aria-label="Навигация">
          <a class="nav__link" href="/">Главная</a>
          <a class="nav__link" href="/psiholog-novosibirsk.html">Психolog НСК</a>
          <a class="nav__link nav__link--active" aria-current="page" href="/blog.html">Блог</a>
          <a class="nav__link" href="/contacts.html">Контакты</a>
          <a class="nav__link nav__link--cta" href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Напишите в Telegram</a>
        </nav>
      </div>
    </header>

    <main id="content" class="page">
      <section class="section">
        <div class="container">
          <h1 class="page__title">Блог</h1>
          <p class="page__lead">
            {len(all_articles)} статей о тревоге, отношениях, выгорании, семье и форматах терапии. Материалы носят информационный характер и не заменяют консультацию специалиста.
          </p>
{body}
          <div class="page__actions">
            <a class="btn btn--primary" href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Написать в Telegram</a>
            <a class="btn btn--ghost" href="/#signup">Форма записи на главной</a>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container footer__inner">
        <p class="footer__copy">© <span id="year"></span> Екатерина Фролова · психolog, Новосибирск</p>
        <nav class="footer__nav" aria-label="Подвал">
          <a href="/">Главная</a>
          <a href="/psiholog-novosibirsk.html">Психolog НСК</a>
          <a href="/blog.html">Блог</a>
          <a href="/contacts.html">Контакты</a>
          <a href="https://t.me/+79612287289" target="_blank" rel="noopener noreferrer">Telegram</a>
        </nav>
      </div>
    </footer>

    <script>
      document.getElementById("year").textContent = String(new Date().getFullYear());
    </script>
    <script type="text/javascript">
      (function (m, e, t, r, i, k, a) {{
        m[i] = m[i] || function () {{ (m[i].a = m[i].a || []).push(arguments); }};
        m[i].l = 1 * new Date();
        for (var j = 0; j < document.scripts.length; j++) {{ if (document.scripts[j].src === r) return; }}
        (k = e.createElement(t)), (a = e.getElementsByTagName(t)[0]), (k.async = 1), (k.src = r), a.parentNode.insertBefore(k, a);
      }})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js?id=109674855", "ym");
      ym(109674855, "init", {{ ssr: true, webvisor: true, clickmap: true, accurateTrackBounce: true, trackLinks: true }});
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/109674855" style="position:absolute;left:-9999px" alt="" /></div></noscript>
  </body>
</html>
"""


def render_sitemap(articles: list[dict]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, pri in LANDINGS:
        loc = SITE + ("/" + path if path else "/")
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    for a in sorted(articles, key=lambda x: x["slug"]):
        lines.append(
            f"  <url><loc>{SITE}/{a['slug']}.html</loc><lastmod>{a.get('date', TODAY)}</lastmod>"
            f"<changefreq>yearly</changefreq><priority>0.6</priority></url>"
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> None:
    manifest = []
    for slug, title, desc, kind, category in NEW_ARTICLES:
        out = ROOT / f"{slug}.html"
        out.write_text(render_article(slug, title, desc, kind, TODAY), encoding="utf-8")
        manifest.append({"slug": slug, "title": title, "desc": desc, "category": category, "date": TODAY})

    all_articles = EXISTING + manifest
    (ROOT / "blog.html").write_text(render_blog(all_articles), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(render_sitemap(all_articles), encoding="utf-8")
    (ROOT / "tools" / "articles_manifest.json").write_text(
        json.dumps(all_articles, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Generated {len(NEW_ARTICLES)} new articles, {len(all_articles)} total in blog/sitemap")


if __name__ == "__main__":
    main()
