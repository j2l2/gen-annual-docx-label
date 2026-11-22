#!/usr/bin/env python3

"""_summary_
"""

from argparse import Namespace, ArgumentParser, SUPPRESS, ArgumentTypeError
from mailmerge import MailMerge     # type: ignore # pip install docx-mailmerge
from lunarcalendar import Converter, Lunar # type: ignore # pip install lunarcalendar
from special_days import SpecialDays


mon = ['','正','二','三','四','五','六','七','八','九','十','十一','十二']
day = ['',
    '初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
    '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
    '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十'
]
zodiac = '鼠牛虎兔龍蛇馬羊猴鷄狗猪'
gan = '甲乙丙丁戊己庚辛壬癸'
zhi = '子丑寅卯辰巳午未申酉戌亥'

def main() -> None:
    """_summary_
    """

    def validate_year(value: str) -> int:
        """_summary_

        Args:
            value (str): _description_

        Raises:
            ArgumentTypeError: _description_

        Returns:
            int: _description_
        """
        try:
            ivalue = int(value)
            if ivalue < 1900 or ivalue > 2100:
                raise ValueError
            return ivalue
        except ValueError:
            raise ArgumentTypeError(f"{value} 不是有效的年份，請輸入 1900 到 2100 之間的數字。")

    argparser = ArgumentParser(
        description="產生一貫道仙佛紀念日表",
        epilog="Copyright 2024，一貫道寶光紹興崇華聖道院，版權所有"
    )
    
    argparser.add_argument("year", type=validate_year, help="產生西元年份，介於(1900-2100)之間")
    args = argparser.parse_args()
    template = "仙佛紀念日.docx"
  
    
    document = MailMerge(template)
    
    # print(document.get_merge_fields())

    xiao = (int(args.year) -3 -1) % 12
    sx = zodiac[xiao]
    g = (int(args.year) -3 -1) % 10
    z = (int(args.year) -3 -1) % 12
    gz = gan[g] + zhi[z]
    year = f"{args.year} {gz}年（{sx}年）"
    document.merge(year=year)
    
    data = []
    for s_day in SpecialDays:
        (l_mo, l_day) = s_day.lunar.split("-")
        # print (f"{s_day.name}: {mon[int(l_mo)]}月{day[int(l_day)]}日")
        lunar_day = f"{mon[int(l_mo)]}月{day[int(l_day)]}日"
        solar = Converter.Lunar2Solar(Lunar(int(args.year), int(l_mo), int(l_day)))
        solar_day = f"{solar.month}月{solar.day}日"
        # print(solar_day)
        data.append({
            'name': s_day.name,
            'etiquette': s_day.etiquette,
            'lunar_day': lunar_day,
            'solar_day': solar_day,
            'note': s_day.note
        })
    document.merge_rows('name', data)
    document.write(f'{year}.docx')
if __name__ == "__main__":
    main()