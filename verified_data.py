"""Published Yemen indicators with exact reporting windows and source URLs.

No synthetic time series, estimates masquerading as observations, or random numbers.
Cross-sector categories overlap and must not be summed.
"""
SOURCES = {
    "ocha": {
        "name": "OCHA – Yemen Humanitarian Needs and Response Plan 2026",
        "date": "2026-03-18",
        "url": "https://yemen.un.org/sites/default/files/2026-03/Yemen_2026_HNRP_EN_final.pdf",
    },
    "unfpa": {
        "name": "UNFPA – Yemen Humanitarian Action Overview",
        "date": "2026-03-30",
        "url": "https://yemen.unfpa.org/sites/default/files/pub-pdf/2date26-date4/2026%20humanitarian%20overview%20and%202025%20results%20-%20Snapshot%20%20-%2030%20March%202026.pdf",
    },
    "who": {
        "name": "WHO / United Nations – Yemen Health Response 2026",
        "date": "2026-10",
        "url": "https://yemen.un.org/en/323279-who-scales-health-response-escalating-conflict-deepens-health-needs-yemen",
    },
    "unicef": {
        "name": "UNICEF – Yemen Humanitarian Action for Children 2026",
        "date": "2026",
        "url": "https://www.unicef.org/appeals/yemen",
    },
    "stc": {
        "name": "Save the Children – Barriers to Education Assessment",
        "date": "2026",
        "url": "https://resourcecentre.savethechildren.net/document/vulnerabilities-assessment-barriers-to-education-in-conflict-affected-communities-yemen-2026",
    },
    "imf": {
        "name": "IMF – Staff-Monitored Program with Yemen",
        "date": "2026-10-07",
        "url": "https://www.imf.org/en/news/articles/2026/10/07/pr26324-imf-management-approves-a-staff-monitored-program-with-yemen",
    },
    "fao": {
        "name": "FAO GIEWS – Yemen Country Brief",
        "date": "2026-10-13",
        "url": "https://www.fao.org/giews/countrybrief/country.jsp?code=YEM&lang=ar",
    },
    "un": {
        "name": "UN – Yemen Country Results Report 2025",
        "date": "2026-06-15",
        "url": "https://yemen.un.org/en/317368-un-yemen-country-results-report-2025",
    },
}

def metric(value, unit, ar, en, source, scope_ar, scope_en):
    return dict(value=value, unit=unit, label_ar=ar, label_en=en,
                source=source, scope_ar=scope_ar, scope_en=scope_en)

SECTORS = {
    "health": {
        "title_ar": "الصحة والاحتياجات الإنسانية",
        "title_en": "Health & Humanitarian Needs",
        "intro_ar": "مؤشرات وطنية منشورة عن الاستجابة الصحية والتغذية وعمل المنشآت؛ وليست بيانات مراقبة لحظية للمستشفيات.",
        "intro_en": "Published national indicators on health, nutrition and facility functionality; not live hospital surveillance.",
        "as_of": "2026", "sources": ["ocha", "unfpa", "who"],
        "metrics": [
            metric(19.3, "M", "أشخاص بحاجة إلى خدمات صحية", "People needing health services", "unfpa", "اليمن • تقديرات 2026", "Yemen • 2026 estimate"),
            metric(2.2, "M", "أطفال دون الخامسة يعانون من سوء تغذية حاد", "Under-five children with acute malnutrition", "ocha", "اليمن • خطة 2026", "Yemen • 2026 HNRP"),
            metric(516157, "count", "حالات سوء تغذية حاد وخيم لدى الأطفال", "Children with severe acute malnutrition", "ocha", "ضمن إجمالي 2.2 مليون • 2026", "Subset of 2.2M • 2026"),
            metric(5415, "count", "وحدات تقديم خدمات صحية قُيّمت", "Health service delivery units assessed", "who", "التقييم المذكور في تقرير 2026", "WHO-reported 2026 assessment"),
        ],
        "charts": [
            {"type": "doughnut", "title_ar": "حالة عمل المنشآت الصحية المقيّمة", "title_en": "Functionality of assessed health service units",
             "labels_ar": ["تعمل بالكامل", "تعمل جزئيًا", "لا تعمل", "فرق تقريب"],
             "labels_en": ["Fully functional", "Partly functional", "Non-functional", "Rounding remainder"],
             "values": [60, 35, 4, 1], "source": "who",
             "note_ar": "النسب 60% و35% و4% مقربة في مصدر WHO؛ أضيف 1% لإكمال الرسم فقط ولا يمثل فئة مثبتة.",
             "note_en": "WHO shares of 60%, 35% and 4% are rounded; 1% is only a rounding remainder, not a measured category."},
            {"type": "bar", "title_ar": "سوء التغذية الحاد لدى الأطفال دون الخامسة", "title_en": "Acute malnutrition in children under five",
             "labels_ar": ["حالات وخيمة", "بقية الحالات"],
             "labels_en": ["Severe cases", "Other acute cases"],
             "values": [516157, 1683843], "source": "ocha",
             "note_ar": "عدد بقية الحالات = 2.2 مليون ناقص 516,157؛ حساب توضيحي بناءً على تقديرات 2026، وليس تقديرًا مستقلًا.",
             "note_en": "Other acute cases = 2.2M less 516,157; arithmetic derived from 2026 estimates, not a separate reported figure."},
        ],
        "insights": [
            {"ar": "خطة الاستجابة الإنسانية تستهدف 12 مليون شخص من أصل 22.3 مليون بحاجة إلى المساعدة على مستوى البلاد، عبر قطاعات متداخلة.", 
             "en": "The 2026 response targets 12M out of 22.3M people needing aid nationally; sector needs overlap.", "source": "ocha"},
            {"ar": "الحالات الصحية وأرقام سوء التغذية تقديرات لفترة الخطة، وليست بلاغات آنية أو أعداد حالات مسجلة اليوم.",
             "en": "Health and nutrition caseloads are planning estimates, not live case reports or today's notifications.", "source": "ocha"},
        ],
    },
    "education": {
        "title_ar": "التعليم والأطفال في اليمن",
        "title_en": "Education & Children in Yemen",
        "intro_ar": "مؤشرات اليونيسف لعام 2026 مع نتائج دراسة ميدانية محددة في عدن ولحج وتعز؛ لا تُعرض نتائج العينة بوصفها ممثلة لليمن كله.",
        "intro_en": "2026 UNICEF national indicators alongside a localized Aden/Lahj/Taiz assessment; survey results are not national estimates.",
        "as_of": "2026", "sources": ["unicef", "stc"],
        "metrics": [
            metric(4.5, "M", "طفل خارج المدرسة", "Children out of school", "unicef", "تقدير اليمن الوطني • 2026", "National estimate • 2026"),
            metric(7, "M+", "طفل يواجه مخاطر حماية", "Children facing protection risks", "unicef", "أكثر من 7 ملايين • 2026", "More than 7M • 2026"),
            metric(4933, "count", "طفل شملتهم الدراسة", "Children in the surveyed sample", "stc", "عينة في عدن ولحج وتعز • 2026", "Sample in Aden, Lahj and Taiz • 2026"),
            metric(63, "%", "من أطفال العينة خارج المدرسة", "Out-of-school rate in the sample", "stc", "العينة فقط؛ لا تمثل النسبة الوطنية", "Survey only; not the national rate"),
        ],
        "charts": [
            {"type": "bar", "title_ar": "تفاصيل الاستبعاد من التعليم في العينة", "title_en": "Education exclusion in the assessment sample",
             "labels_ar": ["لم يلتحقوا مطلقًا", "انقطعوا عن الدراسة"],
             "labels_en": ["Never enrolled", "Dropped out"],
             "values": [1583, 1287], "source": "stc",
             "note_ar": "حالات مذكورة في الدراسة ضمن عينة تشمل 4,933 طفلًا؛ لا يُفترض أنها تستوعب كل أسباب الغياب.",
             "note_en": "Categories explicitly reported among 4,933 surveyed children; they are not an exhaustive breakdown of non-attendance."},
            {"type": "doughnut", "title_ar": "الالتحاق بالتعليم في عينة الدراسة", "title_en": "School participation in the study sample",
             "labels_ar": ["خارج المدرسة", "ليسوا ضمن هذه الفئة"],
             "labels_en": ["Out of school", "Not in that group"],
             "values": [63, 37], "source": "stc",
             "note_ar": "نسبة 63% تخص الأطفال المشاركين في مسح عدن ولحج وتعز، ولا يجوز تعميمها على جميع أطفال اليمن.",
             "note_en": "63% refers only to children assessed in Aden, Lahj and Taiz, not all children in Yemen."},
        ],
        "insights": [
            {"ar": "شملت الدراسة 2,225 أسرة و4,933 طفلًا في مناطق متأثرة بالنزاع؛ لذلك يجب فصل نتائجها عن المؤشر الوطني.",
             "en": "The assessment covers 2,225 households and 4,933 children in conflict-affected communities, not a representative national sample.", "source": "stc"},
            {"ar": "تداخل مخاطر الحماية مع عدم الالتحاق بالمدارس لا يعني أن مجموع الفئتين يمثل عددًا مختلفًا من الأطفال.",
             "en": "Protection-risk and out-of-school figures overlap; they must not be added as distinct child counts.", "source": "unicef"},
        ],
    },
    "economy": {
        "title_ar": "الاقتصاد والأمن الغذائي",
        "title_en": "Economy & Food Security",
        "intro_ar": "توقع اقتصادي من صندوق النقد وتغيرات أسعار منشورة من الفاو وتحليل IPC للفترة أكتوبر–ديسمبر 2026، دون اختراع أسعار صرف لحظية.",
        "intro_en": "An IMF economic projection, FAO food-price indicators and an IPC forecast for Oct–Dec 2026, without fabricated live FX quotes.",
        "as_of": "2026-10", "sources": ["imf", "fao", "ocha", "un"],
        "metrics": [
            metric(-1.5, "%", "النمو الحقيقي المتوقع للناتج 2026", "Projected real GDP growth in 2026", "imf", "توقع صندوق النقد • أكتوبر 2026", "IMF forecast • Oct 2026"),
            metric(5.4, "M", "أشخاص في IPC 3+ بمناطق الحكومة", "People in IPC 3+ in GoY areas", "fao", "توقع أكتوبر–ديسمبر 2026 • تغطية جزئية", "Oct–Dec 2026 projection • partial coverage"),
            metric(1.8, "M", "في مرحلة الطوارئ IPC 4", "People in IPC Phase 4 emergency", "fao", "ضمن 5.4 مليون بمناطق الحكومة", "Subset of 5.4M in GoY areas"),
            metric(90, "%~", "نسبة اعتماد اليمن على استيراد الغذاء", "Approx. food import dependence", "un", "نحو 90% بحسب تقرير الأمم المتحدة", "Approximately 90% in UN report"),
        ],
        "charts": [
            {"type": "bar", "title_ar": "تغير أسعار بعض السلع الغذائية سنويًا", "title_en": "Year-on-year food retail price changes",
             "labels_ar": ["دقيق القمح المستورد", "أرز بسمتي", "السلة الغذائية الدنيا"],
             "labels_en": ["Imported wheat flour", "Basmati rice", "Minimum food basket"],
             "values": [-1, -5, -2], "source": "fao",
             "note_ar": "نسب انخفاض سنوية تقريبية وردت في موجز الفاو 13 أكتوبر 2026؛ لا تمثل أسعارًا لحظية في جميع الأسواق.",
             "note_en": "Approximate year-on-year decreases in FAO's 13 Oct 2026 brief; not live prices for every market."},
            {"type": "doughnut", "title_ar": "انعدام الأمن الغذائي الحاد بمناطق الحكومة", "title_en": "Acute food insecurity in GoY-controlled areas",
             "labels_ar": ["مرحلة الطوارئ IPC 4", "بقية المرحلة 3 فأعلى"],
             "labels_en": ["IPC Phase 4 emergency", "Other IPC Phase 3+"],
             "values": [1.8, 3.6], "source": "fao",
             "note_ar": "مليون شخص: 1.8 ضمن مرحلة الطوارئ من إجمالي 5.4 مليون بمرحلة الأزمة فأعلى؛ توقع أكتوبر–ديسمبر 2026 للمناطق المحللة فقط.",
             "note_en": "Million people: 1.8M emergency among 5.4M facing crisis or worse; Oct–Dec 2026 projection for analyzed areas only."},
        ],
        "insights": [
            {"ar": "أشار صندوق النقد في 7 أكتوبر 2026 إلى احتمال انكماش الناتج الحقيقي للسنة الخامسة على التوالي؛ رقم -1.5% توقع وليس نتيجة نهائية.",
             "en": "The IMF projected a fifth consecutive contraction in October 2026; -1.5% is a forecast, not an observed annual result.", "source": "imf"},
            {"ar": "تقدير 18.3 مليون يواجهون انعدام الأمن الغذائي الحاد في خطة اليمن 2026 وبيانات 5.4 مليون بمناطق الحكومة يختلفان في نطاق التغطية، ولا تتم مقارنتهما كاتجاه زمني.",
             "en": "The nationwide 18.3M food-insecure estimate and the 5.4M GoY-area IPC projection cover different scopes and are not a time series.", "source": "ocha"},
        ],
    },
}

for sector in SECTORS.values():
    sector["source_details"] = {key: SOURCES[key] for key in sector["sources"]}
