"""仙佛紀念日
"""

class SpecialDay:
    """仙佛紀念日
    """
    def __init__(self, name, etiquette, lunar, note) -> None:
        self.name = name
        self.etiquette = etiquette
        self.lunar = lunar
        self.note = note

SpecialDays = [
    SpecialDay("彌勒祖師聖誕", "三跪九叩首", "01-01", ""),
    SpecialDay("天官大帝聖誕", "五叩首", "01-15", "堯帝"),
    SpecialDay("金公祖師成道", "三跪九叩首", "02-02", ""),
    SpecialDay("太上老君聖誕", "五叩首", "02-15", ""),
    SpecialDay("南海古佛聖誕", "五叩首", "02-19", ""),
    SpecialDay("中華聖母成道", "五叩首", "02-23", ""),
    SpecialDay("院長大人聖誕", "三叩首", "03-07", ""),
    SpecialDay("明明上帝　春季大典", "大典禮", "03-15", "春季"),
    SpecialDay("釋迦牟尼佛聖誕", "五叩首","04-08", ""),
    SpecialDay("張老前人成道", "三叩首", "04-11", ""),
    SpecialDay("呂法律主聖誕", "五叩首", "04-14", ""),
    SpecialDay("張老前人聖誕", "三叩首", "04-14", ""),
    SpecialDay("金公祖師聖誕", "三跪九叩首", "04-24", ""),
    SpecialDay("潘道長成道", "三叩首", "05-01", ""),
    SpecialDay("明明上帝　夏季大典", "大典禮", "06-15", "夏季"),
    SpecialDay("南海古佛成道", "五叩首", "06-19", ""),
    SpecialDay("活佛師尊聖誕", "五叩首", "06-24", ""),
    SpecialDay("關法律主聖誕", "五叩首", "06-24", ""),
    SpecialDay("林老前人聖誕", "三叩首", "06-28", ""),
    SpecialDay("地官大帝聖誕", "五叩首", "07-15", "舜帝"),
    SpecialDay("天然古佛聖誕", "五叩首", "07-19", ""),
    SpecialDay("灶君聖誕", "三叩首", "08-03", ""),
    SpecialDay("林老前人成道", "三叩首", "08-09", ""),
    SpecialDay("天然古佛成道", "五叩首", "08-15", ""),
    SpecialDay("至聖先師聖誕", "五叩首", "08-27", ""),
    SpecialDay("中華聖母聖誕", "五叩首", "08-28", ""),
    SpecialDay("周老前人成道", "三叩首", "09-11", ""),
    SpecialDay("明明上帝　秋季大典", "大典禮", "09-15", "秋季"),
    SpecialDay("南海古佛得道", "五叩首", "09-19", ""),
    SpecialDay("水官大帝聖誕", "五叩首", "10-15", "禹帝"),
    SpecialDay("明明上帝　冬季大典", "大典禮", "11-15", "冬季"),
    SpecialDay("周老前人聖誔", "三叩首", "11-18", ""),
]