API_KEY_AVI = '1f67d5c737a3b09f7850f67574c3112c'
API_KEY_TRN = 'b553ddc4-f6db-4d6e-bc3a-cde7801110c2'
city_to_iata = {
    'Москва': 'mow',
    'Санкт-Петербург': 'led',
    'Казань': 'kzn',
    'Екатеринбург': 'svx',
    'Москва (Внуково)': 'vko',
    'Анапа': 'aae',
    'Абакан': 'aba',
    'Ачинск': 'acs',
    'Алдан': 'adh',
    'Сочи': 'aer',
    'Амдерма': 'amv',
    'Архангельск': 'arh',
    'Астрахань': 'asf',
    'Барнаул': 'bax',
    'Белурек': 'bcx',
    'Белая Гора': 'bgn',
    'Богучаны': 'bgs',
    'Баджкит': 'bka',
    'Богородское': 'bqg',
    'Батагай': 'bqj',
    'Благовещенск': 'bqs',
    'Братск': 'btk',
    'Бованенково': 'bvj',
    'Буревестник': 'bvv',
    'Балаково': 'bwo',
    'Брянск': 'bzk',
    'Череповец': 'cee',
    'Челябинск': 'cek',
    'Чокурдах': 'ckh',
    'Чкаловский': 'ckl',
    'Соловки': 'csh',
    'Чебоксары': 'csy',
    'Черский': 'cyx',
    'Чара': 'czr',
    'Менделеево': 'dee',
    'Дальнегорск': 'dhg',
    'Диксон': 'dks',
    'Дальнереченск': 'dlr',
    'Депутатский': 'dpt',
    'Анадырь': 'dyr',
    'Белгород': 'ego',
    'Енисейск': 'eie',
    'Ейск': 'eik',
    'Шахтёрск': 'eks',
    'Ербогачён': 'erg',
    'Элиста': 'esl',
    'Светлая': 'etl',
    'Белоярский': 'eyk',
    'Берёзово': 'ezv',
    'Магдагачи': 'gdg',
    'Магадан': 'gdx',
    'Геленджик': 'gdz',
    'Нижний Новгород': 'goj',
    'Туру': 'goy',
    'Грозный': 'grv',
    'Май-Гатка': 'gvn',
    'Маган': 'gyg',
    'Ханты-Мансийск': 'hma',
    'Чита': 'hta',
    'Хатанга': 'htg',
    'Игарка': 'iaa',
    'Ярославль': 'iar',
    'Магас': 'igt',
    'Ижевск': 'ijk',
    'Тикси': 'iks',
    'Иркутск': 'ikt',
    'Инта': 'ina',
    'Игра': 'irm',
    'Итуруп': 'itu',
    'Иваново': 'iwa',
    'Йошкар-Ола': 'jok',
    'Киренск': 'kck',
    'Кемерово': 'kej',
    'Калининград': 'kgd',
    'Когалым': 'kgp',
    'Хабаровск': 'khv',
    'Красноярск': 'kja',
    'Красноселькуп': 'kkq',
    'Тверь': 'kld',
    'Калуга': 'klf',
    'Кодинск': 'kny',
    'Кепервеем': 'kpw',
    'Курган': 'kro',
    'Краснодар': 'krr',
    'Котлас': 'ksz',
    'Самара': 'kuf',
    'Кировск': 'kvk',
    'Марково': 'kvm',
    'Кавалерово': 'kvr',
    'Киров': 'kvx',
    'Комсомольск-на-Амуре': 'kxk',
    'Кызыл': 'kyz',
    'Лешуконское': 'ldg',
    'Смоленск': 'lnx',
    'Липецк': 'lpk',
    'Махачкала': 'mcx',
    'Мотыгино': 'mjy',
    'Мирный': 'mjz',
    'Мурманск': 'mmk',
    'Магнитогорск': 'mqf',
    'Мама': 'mqj',
    'Минеральные Воды': 'mrv',
    'Нальчик': 'nal',
    'Бегишево': 'nbc',
    'Нефтекамск': 'nef',
    'Терней': 'nei',
    'Нерюнгри': 'ner',
    'Ноглики': 'ngk',
    'Нижневартовск': 'njc',
    'Николаевск-на-Амуре': 'nli',
    'Нарьян-Мар': 'nnm',
    'Новороссийск': 'noi',
    'Ноябрьск': 'noj',
    'Новокузнецк': 'noz',
    'Норильск': 'nsk',
    'Новый Уренгой': 'nux',
    'Новгород': 'nvr',
    'Нягань': 'nya',
    'Надым': 'nym',
    'Нюрба': 'nyr',
    'Нижнеангарск': 'nzg',
    'Бодайбо': 'odo',
    'Орёл': 'oel',
    'Владикавказ': 'ogz',
    'Новостройка': 'ohh',
    'Охотск': 'oho',
    'Октябрьский': 'okt',
    'Олёкминск': 'olz',
    'Омск': 'oms',
    'Оленёк': 'onk',
    'Орск': 'osw',
    'Новосибирск': 'ovb',
    'Советский': 'ovs',
    'Пермь': 'pee',
    'Петрозаводск': 'pes',
    'Печора': 'pex',
    'Пенза': 'pez',
    'Петропавловск-Камчатский': 'pkc',
    'Псков': 'pkv',
    'Провидения': 'pvs',
    'Певек': 'pwe',
    'Полярный': 'pyj',
    'Радужный': 'rat',
    'Оренбург': 'ren',
    'Горно-Алтайск': 'rgk',
    'Тобольск': 'rmz',
    'Ростов-на-Дону': 'rov',
    'Саратов': 'rtw',
    'Рыбинск': 'ryb',
    'Преображение': 'rzh',
    'Рязань': 'rzn',
    'Сабетта': 'sbt',
    'Сыктывкар': 'scw',
    'Среднеколымск': 'sek',
    'Светлогорск': 'ses',
    'Сургут': 'sgc',
    'Саранск': 'skx',
    'Ставрополь': 'stw',
    'Сахалин': 'suk',
    'Сангар': 'suy',
    'Стрежевой': 'swt',
    'Северо-Эвенск': 'swv',
    'Саскылах': 'sys',
    'Тамбов': 'tbw',
    'Таганрог': 'tgk',
    'Подкаменная Тунгуска': 'tgp',
    'Туруханск': 'thx',
    'Тюмень': 'tjm',
    'Тиксимо': 'tkm',
    'Талакан': 'tlk',
    'Пластун': 'tly',
    'Томск': 'tof',
    'Тарко-Сале': 'tql',
    'Тула': 'tya',
    'Тында': 'tyd',
    'Ухта': 'uct',
    'Уренгой': 'uen',
    'Уфа': 'ufa',
    'Усть-Илимск': 'uik',
    'Усть-Куйга': 'ukg',
    'Усть-Кут': 'ukx',
    'Ленск': 'ulk',
    'Ульяновск': 'uly',
    'Усть-Мая': 'ums',
    'Урай': 'urj',
    'Курск': 'urs',
    'Усинск': 'usk',
    'Усть-Рена': 'usr',
    'Усть-Цильма': 'uts',
    'Бугульма': 'uua',
    'Улан-Удэ': 'uud',
    'Южно-Сахалинск': 'uus',
    'Ванавара': 'vaq',
    'Северо-Энисейск': 'veo',
    'Вологда': 'vgd',
    'Верхневилюйск': 'vhv',
    'Воркута': 'vkt',
    'Волгодонск': 'vlk',
    'Великие Луки': 'vlu',
    'Волгоград': 'vog',
    'Воронеж': 'voz',
    'Варандей': 'vri',
    'Великий Устюг': 'vus',
    'Владивосток': 'vvo',
    'Вилюйск': 'vyi',
    'Ярцево': 'yae',
    'Якутск': 'yks',
    'Мыс Каменный': 'ymk',
    'Чиганка': 'zix',
    'Зырянка': 'zkp',
    'Зональное': 'zzo',
    'Адамовка': 'adm',
    'Агзу': 'azu',
    'Амгу': 'amu',
    'Апука': 'apu',
    'Архыз': 'ahz',
    'Ахайваям': 'ach',
    'Аянка': 'ayk',
    'Аян': 'ayn',
    'Главный': 'bgg',
    'Белокуриха': 'bih',
    'Беринговский': 'bng',
    'Большой Ларджак': 'bok',
    'Бурный': 'buy',
    'Байлино': 'byl',
    'Спайск': 'vag',
    'Вершинский': 'ves',
    'Владимир': 'vlm',
    'Вампугольск': 'vmp',
    'Вуктыл': 'vtl',
    'Домбай': 'dmy',
    'Эдинка': 'edi',
    'Эссей': 'esi',
    'Ессентуки': 'esn',
    'Железногорск': 'zhez',
    'Зея': 'zeya',
    'Лаврентия': 'zla',
    'Крабозаводское': 'kbz',
    'Кускургун': 'kgy',
    'Кедровый': 'kdd',
    'Каменское': 'kdu',
    'Кузьмовка': 'kzv',
    'Казачинское': 'kzch',
    'Корлики': 'kiu',
    'Колекеган': 'klk',
    'Краснокаменск': 'knk',
    'Кослан': 'kos',
    'Красный Чикой': 'ksch',
    'Красный Кут': 'ksy',
    'Кислоканы': 'ksyu',
    'Куджумба': 'kyum',
    'Лайтамак': 'lay',
    'Ларджак': 'lry',
    'Мама': 'mam',
    'Мириуга': 'mga',
    'Мезень': 'mzn',
    'Манилы': 'mil',
    'Максимовка': 'mki',
    'Никольское': 'nik',
    'Нелькан': 'nln',
    'Новокуровка': 'nuv',
    'Озерная': 'ozr',
    'Омолон': 'ool',
    'Оссора': 'oso',
    'Омсукчан': 'osu',
    'Ошарово': 'osha',
    'Поронайск': 'pay',
    'Палана': 'pan',
    'Пахачи': 'pach',
    'Победа': 'pbe',
    'Полигус': 'pgu',
    'Подволочное': 'pdv',
    'Полынья Осипенко': 'pos',
    'Мопный Курт': 'pug',
    'Покур': 'pur',
    'Сангар': 'sag',
    'Суломай': 'sai',
    'Соболево': 'sbo',
    'Сосновый Бор': 'sbr',
    'Суринда': 'sdr',
    'Северо-Курильск': 'skr',
    'Светлый': 'sly',
    'Слаутное': 'slu',
    'Самарга': 'smg',
    'Смирных': 'smh',
    'Сеймчан': 'smch',
    'Синегорье': 'sng',
    'Старый Оскол': 'sol',
    'Средние Пахачи': 'sph',
    'Сусуман': 'ssm',
    'Срелка-Чуня': 'schu',
    'Тигиль': 'tig',
    'Тиличики': 'til',
    'Таловка': 'tlo',
    'Тутончаны': 'tnch',
    'Тугур': 'tuu',
    'Троицко-Печорск': 'tcp',
    'Толка': 'tyk',
    'Удское': 'uds',
    'Усть-Кокса': 'uko',
    'Усть-Камчатск': 'ukch',
    'Учами': 'umi',
    'Усть-Омчуг': 'uom',
    'Усть-Коликиджиган': 'ute',
    'Усть-Хайрюзово': 'uhy',
    'Хайлино': 'hai',
    'Харута': 'hau',
    'Хужир': 'hzhr',
    'Керпучи': 'hrp',
    'Чегдомын': 'chd',
    'Химдалск': 'chem',
    'Чехломей': 'chekh',
    'Чиринда': 'chir',
    'Чумикан': 'chmi',
    'Шерегеш': 'shgsh',
    'Шушенское': 'shush',
    'Залив Креста': 'egt',
    'Эконда': 'eko',
    'Джукта': 'ykt',
    'Ягодное': 'yago',
    'Ямбург': 'yamb',
}
city_name_to_code_train = {
    'Москва': "c213",
    'Санкт-Петербург': 'c54',
    'Казань': 'c43',
    'Екатеринбург': 'c62',
    'Новосибирск': 'c14',
    'Нижний Новгород': 'c107',
    'Самара': 'c123',
    'Омск': 'c143',
    'Ростов-на-Дону': 'c152',
    'Уфа': 'c184',
    'Красноярск': 'c221',
    'Воронеж': 'c232',
    'Пермь': 'c239',
    'Волгоград': 'c259',
    'Краснодар': 'c272',
    'Сочи': 'c289',
    'Челябинск': 'c294',
    'Иркутск': 'c308',
    'Владивосток': 'c328',
    'Хабаровск': 'c341',
    'Ярославль': 'c350',
    'Тюмень': 'c369',
    'Ижевск': 'c382',
    'Барнаул': 'c397',
    'Томск': 'c408',
    'Кемерово': 'c417',
    'Новокузнецк': 'c426',
    'Тула': 'c437',
    'Калининград': 'c446',
    'Брянск': 'c459',
    'Курск': 'c468',
    'Липецк': 'c477',
    'Орёл': 'c486',
    'Смоленск': 'c495',
    'Тверь': 'c504',
    'Владимир': 'c513',
    'Чита': 'c522',
    'Ставрополь': 'c531',
    'Махачкала': 'c540',
    'Петрозаводск': 'c549',
    'Сыктывкар': 'c558',
    'Йошкар-Ола': 'c567',
    'Саранск': 'c576',
    'Улан-Удэ': 'c585',
    'Магнитогорск': 'c594',
    'Норильск': 'c603',
    'Мурманск': 'c612',
    'Архангельск': 'c621',
    'Сургут': 'c630',
    'Нижневартовск': 'c639',
    'Новый Уренгой': 'c648',
    'Тобольск': 'c657',
    'Ноябрьск': 'c666',
    'Ханты-Мансийск': 'c675',
    'Южно-Сахалинск': 'c684',
    'Петропавловск-Камчатский': 'c693',
    'Анадырь': 'c702',
    'Благовещенск': 'c711',
    'Биробиджан': 'c720',
    'Якутск': 'c729',
    'Абакан': 'c738',
    'Грозный': 'c747',
    'Нальчик': 'c756',
    'Черкесск': 'c765',
    'Элиста': 'c774',
    'Симферополь': 'c783',
    'Севастополь': 'c792',
    'Керчь': 'c801',
    'Феодосия': 'c810',
    'Евпатория': 'c819',
    'Ялта': 'c828',
    'Алушта': 'c837',
    'Судак': 'c846',
    'Бахчисарай': 'c855',
    'Саки': 'c864',
    'Джанкой': 'c873',
    'Красноперекопск': 'c882',
    'Армянск': 'c891',
    'Щёлкино': 'c900',
    'Старый Крым': 'c909',
    'Белогорск': 'c918',
    'Раздольное': 'c927',
    'Нижнегорск': 'c936',
    'Советский': 'c945',
    'Черноморское': 'c954',
    'Кировское': 'c963',
    'Ленино': 'c972',
    'Первомайское': 'c981',
    'Красногвардейское': 'c990',
}