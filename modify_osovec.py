from pathlib import Path

path = Path("ocovec/osovec.html")
text = path.read_text(encoding="cp866")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise SystemExit(label + " pattern not found")
    text = text.replace(old, new, 1)


def replace_card(heading: str, new_block: str) -> None:
    global text
    start_marker = "        <div class=\"card\">\n          <div class=\"body\">\n            <h2>" + heading + "</h2>"
    start = text.find(start_marker)
    if start == -1:
        raise SystemExit("card heading '" + heading + "' not found")
    close_marker = "\n          </div>\n        </div>"
    end = text.find(close_marker, start)
    if end == -1:
        raise SystemExit("closing marker for '" + heading + "' not found")
    end += len(close_marker)
    text = text[:start] + new_block + text[end:]
# Step 1: add indent variable
replace_once(
    "      --radius: 16px;\n      --maxw: 1080px;\n    }\n",
    "      --radius: 16px;\n      --maxw: 1080px;\n      --indent: 2.2em;\n    }\n",
    "root block"
)

# Step 2: extend layout styles
css_snippet = (
    "    .text-flow{\n"
    "      display:grid;\n"
    "      gap: clamp(14px, 2.8vw, 24px);\n"
    "      line-height: 1.7;\n"
    "    }\n"
    "    .text-flow > *{ margin:0; }\n"
    "    .text-flow > * + *{ margin-top: clamp(10px, 2.2vw, 18px); }\n"
    "    .text-flow > p{\n"
    "      text-indent: var(--indent);\n"
    "      text-align: justify;\n"
    "      text-wrap: pretty;\n"
    "    }\n"
    "    .text-flow > p.no-indent, .text-flow > .no-indent{ text-indent: 0; }\n"
    "    .text-flow > p.muted{ text-indent: 0; }\n"
    "    .text-flow > blockquote{\n"
    "      text-indent: 0;\n"
    "      padding: clamp(14px, 3vw, 24px);\n"
    "      border-radius: 14px;\n"
    "      background: rgba(255,255,255,.05);\n"
    "      border-left: 4px solid var(--accent);\n"
    "      box-shadow: 0 16px 40px rgba(0,0,0,.18);\n"
    "    }\n"
    "    .text-flow > blockquote p{\n"
    "      margin:0;\n"
    "      text-indent: 0;\n"
    "      color: var(--ink);\n"
    "      font-style: italic;\n"
    "    }\n"
    "    .text-flow > ul, .text-flow > ol{\n"
    "      margin:0;\n"
    "      padding-left: clamp(18px, 3vw, 28px);\n"
    "    }\n"
    "    .text-flow > .aside{ margin-top: clamp(8px, 2vw, 16px); }\n"
    "    .aside{\n"
    "      background: rgba(24,28,36,.72);\n"
    "      border: 1px solid rgba(255,255,255,.08);\n"
    "      border-radius: 14px;\n"
    "      padding: clamp(12px, 3vw, 20px);\n"
    "      color: var(--muted);\n"
    "      text-indent: 0 !important;\n"
    "      box-shadow: var(--shadow);\n"
    "    }\n"
    "    .aside strong{ color: var(--ink); }\n"
    "    .tag{\n"
    "      display:inline-flex;\n"
    "      align-items:center;\n"
    "      gap:6px;\n"
    "      padding:4px 12px;\n"
    "      border-radius:999px;\n"
    "      background:rgba(136,198,255,.12);\n"
    "      color:var(--accent);\n"
    "      text-transform:uppercase;\n"
    "      font-weight:700;\n"
    "      letter-spacing:.08em;\n"
    "      font-size:11px;\n"
    "    }\n"
    "    .feature{ margin: clamp(32px, 6vw, 68px) 0; }\n"
    "    .feature .card{\n"
    "      background: linear-gradient(180deg, rgba(28,32,40,.92), rgba(16,20,28,.92));\n"
    "      border:1px solid rgba(255,255,255,.12);\n"
    "    }\n"
    "    .feature .card .body{ max-width: 74ch; margin: 0 auto; }\n"
    "    .stat-badges{\n"
    "      display:flex; flex-wrap:wrap;\n"
    "      gap: clamp(10px, 2vw, 18px);\n"
    "      margin: clamp(4px, 1.6vw, 12px) 0 clamp(12px, 3vw, 22px);\n"
    "    }\n"
    "    .stat-badge{\n"
    "      background: rgba(255,255,255,.04);\n"
    "      border: 1px solid rgba(255,255,255,.08);\n"
    "      border-radius: 12px;\n"
    "      padding: 12px 16px;\n"
    "      min-width: 160px;\n"
    "      box-shadow: 0 14px 24px rgba(0,0,0,.18);\n"
    "    }\n"
    "    .stat-badge .label{\n"
    "      font-size: 11px;\n"
    "      letter-spacing:.1em;\n"
    "      text-transform: uppercase;\n"
    "      color: rgba(136,198,255,.75);\n"
    "      margin-bottom: 6px;\n"
    "      display:block;\n"
    "    }\n"
    "    .stat-badge .value{\n"
    "      font-size: clamp(16px, 2.2vw, 20px);\n"
    "      font-weight: 600;\n"
    "      color: var(--ink);\n"
    "    }\n"
    "    .photo-grid{\n"
    "      display:grid;\n"
    "      gap: clamp(16px, 3vw, 28px);\n"
    "      margin: clamp(20px, 5vw, 36px) auto 0;\n"
    "      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));\n"
    "      width: 100%;\n"
    "    }\n"
    "    .photo-grid figure{ width: 100%; margin:0; }\n"
    "    .photo-grid figure.wide{ grid-column: 1 / -1; }\n"
    "    .photo-grid figure img{ height: clamp(220px, 38vh, 420px); }\n"
    "    .photo-grid figcaption{ text-align:left; }\n"
    "    .photo-grid .photo-slot.portrait img{ object-position: 50% 35%; }\n"
    "    .mini-timeline{\n"
    "      margin: clamp(26px, 6vw, 44px) auto 0;\n"
    "      padding: clamp(18px, 4vw, 26px);\n"
    "      border-radius: var(--radius);\n"
    "      background: rgba(24,28,36,.62);\n"
    "      border:1px solid rgba(255,255,255,.08);\n"
    "      display:grid;\n"
    "      gap: clamp(12px, 2.4vw, 22px);\n"
    "      max-width: 760px;\n"
    "    }\n"
    "    .mini-timeline .moment{ position:relative; padding-left: 82px; }\n"
    "    .mini-timeline .moment::before{\n"
    "      content:\"\"; position:absolute; left:36px; top:14px; bottom:-12px;\n"
    "      width:2px; background: linear-gradient(180deg, rgba(136,198,255,.65), rgba(136,198,255,0));\n"
    "    }\n"
    "    .mini-timeline .moment:last-child::before{ bottom:14px; }\n"
    "    .mini-timeline .moment-time{\n"
    "      position:absolute; left:0; top:0;\n"
    "      font-weight:700; color:var(--accent); letter-spacing:.08em;\n"
    "    }\n"
    "    .mini-timeline .moment p{ margin:0; text-indent:0; color:var(--muted); }\n"
    "    @media (max-width: 640px){\n"
    "      .mini-timeline .moment{ padding-left: 64px; }\n"
    "      .mini-timeline .moment::before{ left:28px; }\n"
    "    }\n"
)

replace_once(
    "    .grid{ display:grid; gap: clamp(12px, 2.5vw, 20px); grid-template-columns: 1fr; }\n    @media (min-width: 920px){\n      .grid.cols-2{grid-template-columns: 1.05fr .95fr}\n      .grid.cols-3{grid-template-columns: 1fr 1fr 1fr}\n    }\n",
    "    .grid{ display:grid; gap: clamp(12px, 2.5vw, 20px); grid-template-columns: 1fr; }\n    @media (min-width: 920px){\n      .grid.cols-2{grid-template-columns: 1.05fr .95fr}\n      .grid.cols-3{grid-template-columns: 1fr 1fr 1fr}\n    }\n" + css_snippet,
    "grid block"
)

# Step 3: adjust hero paragraph style
replace_once(
    '    .center-text p{ font-size:18px; line-height:1.6; color:#d0d6e2; max-width:70ch; margin:0 auto; }\n',
    '    .center-text p{ font-size:18px; line-height:1.65; color:#d0d6e2; max-width:70ch; margin:0 auto 1.1em; text-align:justify; text-indent: var(--indent); }\n',
    'center-text CSS'
)

# Step 4: hero paragraphs
replace_once(
    """  <section class=\"center-text\">\n    <h2>Первая мировая война — Восточный фронт</h2>\n    <h1>«Атака мёртвецов»: контратака защитников крепости Осовец</h1>\n    <p>Утро 6 августа 1915 (24 июля по старому стилю). После массированного выпуска хлора (местами — со смесью брома) на передовые позиции крепости Осовец немецкая пехота пошла в штурм. \n      Навстречу ей поднялись отравленные газом защитники. Этот эпизод получит известность как «Атака мёртвецов» — и обрастёт легендами.</p>\n  </section>\n""",
    """  <section class=\"center-text\">\n    <h2>Первая мировая война — Восточный фронт</h2>\n    <h1>«Атака мёртвецов»: контратака защитников крепости Осовец</h1>\n    <p>Утро 6 августа 1915 (24 июля по старому стилю). После массированного выпуска хлора — местами с примесью брома — по вынесенной Сосненской позиции крепости Осовец немецкая пехота пошла в штурм.</p>\n    <p>Навстречу ей поднялись отравленные газом защитники. Эпизод получил название «Атака мёртвецов» и десятилетиями обрастал легендами; собрали проверенные факты, свидетельства и цифры.</p>\n  </section>\n""",
    'center-text block'
)

new_brief = """        <div class=\"card\">\n          <div class=\"body text-flow\">\n            <h2>В двух словах</h2>\n            <p>Крепость Осовец на реке Бобр (ныне Подляское воеводство, Польша) с осени 1914 года сдерживала продвижение германских войск к Белостоку.</p>\n            <p>На рассвете 6&nbsp;августа 1915 года германцы открыли газовую атаку хлором (в ряде источников упоминается примесь брома) по вынесенной Сосненской позиции.</p>\n            <p>Часть гарнизона погибла и была выдавлена с передового рубежа, но контратака рот <strong>226-го Землянского пехотного полка</strong> и соседних подразделений сорвала штурм.</p>\n            <p>Через двенадцать дней, под угрозой окружения, гарнизон организованно эвакуировал крепость, предварительно разрушив ключевые укрепления и склады.</p>\n            <div class=\"aside\">\n              <span class=\"tag\">Дата</span> 6 августа 1915 (24 июля ст. ст.) &middot;\n              <span class=\"tag\">Место</span> Крепость Осовец\n            </div>\n          </div>\n        </div>\n"""

new_where = """        <div class=\"card\">\n          <div class=\"body text-flow\">\n            <h2>Где находится крепость Осовец</h2>\n            <p>Осовец (пол. Osowiec-Twierdza) — узел укреплений в излучине реки Бобр, в коридоре между Неманом и линией Висла–Нарев–Буг.</p>\n            <p>Крепость построена Российской империей в 1882–1892 годах и постоянно модернизировалась: болотистая местность осложняла подступы, а железная дорога Белосток—Лык—Кёнигсберг и шоссе через крепость придавали ей стратегическое значение.</p>\n            <ul>\n              <li><strong>Форты:</strong> система из четырёх фортов и вынесенных позиций, связанных траншеями;</li>\n              <li><strong>Сосненская позиция:</strong> передовой рубеж на западном берегу, в 2–2,5 км от цитадели;</li>\n              <li><strong>Гарнизон:</strong> к лету 1915 года — многотысячная группировка с крепостной артиллерией, аэростатом и 3 самолётами-разведчиками.</li>\n            </ul>\n          </div>\n        </div>\n"""

new_background = """        <div class=\"card\">\n          <div class=\"body text-flow\">\n            <h2>Предыстория: осада 1914–1915</h2>\n            <p>Лето 1915 года стало «чёрным временем» русских крепостей: Новогеоргиевская и Ковенская были сданы, а Ивангородская и Осовецкая по решению командования готовились к эвакуации. Осовец перекрывал железнодорожный и шоссейный пути на Белосток.</p>\n            <p>Первые две попытки штурма — в сентябре 1914 года и в феврале–марте 1915-го — закончились неудачей для немцев: атаки обошлись им серьёзными потерями, и противник временно отказался от прямого приступа.</p>\n            <p>После провала наступления германская армия перешла к позиционной войне, накапливая силы, подтягивая тяжёлую артиллерию и готовя новый штурм, в котором ключевую роль должны были сыграть химические средства.</p>\n          </div>\n        </div>\n"""

new_gas = """        <div class=\"card\">\n          <div class=\"body text-flow\">\n            <h2>Газовая атака 6&nbsp;августа&nbsp;1915</h2>\n            <p>На рассвете около 4:00, при благоприятном ветре, германцы начали выпускать <strong>хлор</strong> (в ряде источников — с примесью <em>брома</em>) по фронту Сосненской позиции.</p>\n            <p>Газ шёл плотной волной, поражая людей и технику; передний край понёс тяжёлые потери, часть окопов противник занял.</p>\n            <ul>\n              <li>Отмечают до <em>30 газобаллонных батарей</em> и глубокое проникновение облака;</li>\n              <li>Эффект газа был неравномерен по участкам;</li>\n              <li>Часть резервов в крепости избежала полного поражения.</li>\n            </ul>\n          </div>\n        </div>\n"""

replace_card('В двух словах', new_brief)
replace_card('Где находится крепость Осовец', new_where)
replace_card('Предыстория: осада 1914–1915', new_background)
replace_card('Газовая атака 6&nbsp;августа&nbsp;1915', new_gas)

anchor = "</section>\n\n    <!-- Предыстория -->\n"
new_gallery = """</section>\n\n    <!-- Подборка фото -->\n    <section id=\"visuals\" class=\"card photo-essay\">\n      <div class=\"body text-flow\">\n        <h2>Идеи для иллюстраций</h2>\n        <p>Здесь можно разместить собственные фотографии крепости, реконструкций или карт. Сейчас стоят заглушки — замените их на нужные изображения.</p>\n      </div>\n      <div class=\"photo-grid\">\n        <figure class=\"photo-slot wide\">\n          <img src=\"https://images.unsplash.com/photo-1500051638674-ff996a0ec29e?auto=format&fit=crop&w=1400&q=80\" alt=\"Панорама крепостных валов на закате\" loading=\"lazy\" />\n          <figcaption>Заглушка: общий вид крепости или карта расположения фортов.</figcaption>\n        </figure>\n        <figure class=\"photo-slot\">\n          <img src=\"https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=900&q=80\" alt=\"Деталь старой кирпичной кладки\" loading=\"lazy\" />\n          <figcaption>Заглушка: фактура стен, детали капониров и брустверов.</figcaption>\n        </figure>\n        <figure class=\"photo-slot\">\n          <img src=\"https://images.unsplash.com/photo-1520256862855-398228c41684?auto=format&fit=crop&w=900&q=80\" alt=\"Экспонаты военно-исторического музея\" loading=\"lazy\" />\n          <figcaption>Заглушка: музейные артефакты или предметы экипировки защитников.</figcaption>\n        </figure>\n      </div>\n    </section>\n\n    <!-- Предыстория -->\n"""
replace_once(anchor, new_gallery, 'gallery anchor')
new_counter = """    <!-- Контратака -->\n    <section id=\"counter\" class=\"feature\">\n      <div class=\"card feature-card\">\n        <div class=\"body text-flow\">\n          <h2>Контратака, которую назовут «Атакой мёртвецов»</h2>\n          <div class=\"stat-badges\">\n            <div class=\"stat-badge\">\n              <span class=\"label\">Газовые батареи</span>\n              <span class=\"value\">30 установок</span>\n            </div>\n            <div class=\"stat-badge\">\n              <span class=\"label\">Глубина заражения</span>\n              <span class=\"value\">до 20&nbsp;км</span>\n            </div>\n            <div class=\"stat-badge\">\n              <span class=\"label\">Потери защитников</span>\n              <span class=\"value\">≈600–650 человек</span>\n            </div>\n          </div>\n          <p>Отравляющие вещества — в данном случае хлор — оставались новинкой, поэтому средства защиты у русских войск были несовершенны. Газ доставлялся в баллонах, и немцы более десяти дней ждали попутного ветра, чтобы облако не накрыло собственные цепи.</p>\n          <p>Для атаки на четырёх участках сосредоточили 30 газобаллонных батарей, каждая — с 10–12 баллонами и компрессорами. Жидкий хлор выбрасывался в течение 1,5–3 минут, создавая сплошную завесу перед позициями.</p>\n          <p>Рано утром 24 июля (6 августа) 1915 года при попутном ветре начался выпуск хлора и брома по всему фронту. Газ проник на глубину до 20&nbsp;км и сохранял поражающее действие до 12&nbsp;км при высоте облака около 12&nbsp;м. Журнал боевых действий 443-го полка отмечал, что немецкая артиллерия открыла огонь уже в 3:20 — перед массированным выпуском газа.</p>\n          <p>Дневник 226-го Землянского полка фиксировал, что в 4:00 противник выпустил «целое облако удушливых газов» и под их прикрытием повёл наступление на 1-й, 2-й и 4-й участки Сосненской позиции. Одновременно немцы вели ураганный огонь по Заречному форту и коммуникациям.</p>\n          <p>У защитников были импровизированные меры противодействия: жгли паклю и солому перед окопами, поливали брустверы известковым раствором, надевали противогазовые маски и повязки. Эффективность оставалась невысокой — многие использовали мокрые тряпки или бинты.</p>\n          <p>Роты в низинах пострадали особенно сильно: 9-я, 10-я и 11-я почти перестали существовать; в 12-й на Центральном редуте в строю осталось около сорока человек, у Бялогронды — порядка шестидесяти. Обстрел снарядами с ОВ лишил русскую артиллерию возможности быстро ответить.</p>\n          <p>Германская артиллерия создала огневой вал, и части 18-го и 76-го ландверных полков заняли первую и вторую линии, ожидая встретить лишь мёртвые тела. Но выжившие роты — опираясь на остатки резервов — поднялись в контратаку.</p>\n          <blockquote>\n            <p>«Я не могу описать озлобления и бешенства, с которым шли наши солдаты на отравителей-немцев. Сильный ружейный и пулемётный огонь, густо рвавшаяся шрапнель не могли остановить натиска. Здесь не было отдельных героев — роты шли как один человек: погибнуть, но отомстить».</p>\n          </blockquote>\n          <p>Русская артиллерия вновь вступила в бой и помогла выбить противника. К 11 часам Сосненская позиция была очищена; повторять атаку немцы не решились. Боевая группа потеряла убитыми, ранеными и пострадавшими от газов около 600–650 человек, противник понёс сопоставимые или большие потери.</p>\n          <div class=\"aside\"><strong>Важно про цифры.</strong> Публицистика даёт образ «60–100 полуживых бойцов против тысяч», тогда как архивные реконструкции говорят о <em>нескольких ротах</em> с нашей стороны и ограниченных штурмовых группах противника.</div>\n        </div>\n      </div>\n      <div class=\"photo-grid\">\n        <figure class=\"photo-slot wide\">\n          <img src=\"https://images.unsplash.com/photo-1524492530021-3c5aa8adad59?auto=format&fit=crop&w=1400&q=80\" alt=\"Газовые маски времён Первой мировой войны\" loading=\"lazy\" />\n          <figcaption>Заглушка: маски и защитные костюмы — замените на своё фото сцены подготовки к бою.</figcaption>\n        </figure>\n        <figure class=\"photo-slot\">\n          <img src=\"https://images.unsplash.com/photo-1517686469429-8bdb88b9fffa?auto=format&fit=crop&w=900&q=80\" alt=\"Рубеж обороны в тумане\" loading=\"lazy\" />\n          <figcaption>Заглушка: атмосферный кадр укреплений или ландшафта вокруг Осовца.</figcaption>\n        </figure>\n        <figure class=\"photo-slot portrait\">\n          <img src=\"https://images.unsplash.com/photo-1542367597-31e9961317a3?auto=format&fit=crop&w=900&q=80\" alt=\"Силуэт солдата на фоне восхода\" loading=\"lazy\" />\n          <figcaption>Заглушка: место под портреты командиров или реконструкторов.</figcaption>\n        </figure>\n      </div>\n      <div class=\"mini-timeline\" aria-label=\"Хроника контратаки\">\n        <div class=\"moment\">\n          <span class=\"moment-time\">03:20</span>\n          <p>Немецкая артиллерия открывает обстрел Заречного форта и коммуникаций, готовя почву для газовой атаки.</p>\n        </div>\n        <div class=\"moment\">\n          <span class=\"moment-time\">04:00</span>\n          <p>Газовые батареи выпускают хлор с примесью брома по всей Сосненской позиции; облако накрывает траншеи.</p>\n        </div>\n        <div class=\"moment\">\n          <span class=\"moment-time\">04:30</span>\n          <p>18-й и 76-й ландверные полки продвигаются через поражённые участки, занимая первую и вторую линии обороны.</p>\n        </div>\n        <div class=\"moment\">\n          <span class=\"moment-time\">≈05:00</span>\n          <p>Роты 226-го Землянского и соседние части переходят в контратаку, поддержанные крепостной артиллерией.</p>\n        </div>\n        <div class=\"moment\">\n          <span class=\"moment-time\">11:00</span>\n          <p>Сосненская позиция зачищена; противник отходит и штурм более не возобновляет.</p>\n        </div>\n      </div>\n    </section>\n"""

start = text.find('    <!-- Контратака -->')
if start == -1:
    raise SystemExit("counter section start not found")
end = text.find('    </section>', start)
if end == -1:
    raise SystemExit("counter section end not found")
end += len('    </section>')
text = text[:start] + new_counter + text[end:]

new_aftermath = """        <div class=\"card\">\n          <div class=\"body text-flow\">\n            <h2>Итоги боя и эвакуация крепости</h2>\n            <p>Штурм 6&nbsp;августа сорвали, но оперативная обстановка ухудшалась: падение Ковно и угрозы от Новогеоргиевска делали удержание Осовца бессмысленным.</p>\n            <p><strong>18&nbsp;августа&nbsp;1915</strong> гарнизон организованно оставил крепость, предварительно приведя в негодность укрепления и имущество.</p>\n          </div>\n        </div>\n"""
replace_card('Итоги боя и эвакуация крепости', new_aftermath)

path.write_text(text, encoding='cp866')
