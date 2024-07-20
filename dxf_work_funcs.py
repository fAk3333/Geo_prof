import ezdxf
import re
from ezdxf.math import ConstructionArc
from ary_funcs import scaling_otmetok, scaling_piketov

def ugod_drawer(ugod, piketi, msp):
    dots_of_ugod = []
    for i in range(len(ugod)):
        if i == 0:
            continue
        if ugod[i] != ugod[i - 1]:
            # Линии - границы угодий
            msp.add_line([piketi[i], -25], [piketi[i], -34])
            dots_of_ugod.append(piketi[i])
            # Подпишем точки
            if piketi[i] > 200:
                num = piketi[i]
                num = num / 2
                num = str(num)
                drobnoe = float(num[1:])

                if drobnoe < 10.0:

                    msp.add_text("+0{0}".format(drobnoe.__round__(2)), height=1.8, rotation=90,
                                 dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, - 33))
                else:
                    msp.add_text("+{0}".format(drobnoe.__round__(2)), height=1.8, rotation=90,
                                 dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, -33))
            elif piketi[i] == 200:
                msp.add_text("+00.0", height=1.8, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, -33))
            else:
                drobnoe = piketi[i] / 2
                if drobnoe < 10.0:
                    msp.add_text("+0{0}".format(drobnoe.__round__(2)), height=1.8, rotation=90,
                                dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, - 33))
                else:
                    msp.add_text("+{0}".format(drobnoe.__round__(2)), height=1.8, rotation=90,
                                 dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, -33))

    # Подпишем угодья
    # отчистим лишнее
    ugod_without_duplicates = []
    for i in range(len(ugod)):
        if i == 0:
            ugod_without_duplicates.append(ugod[i])
        else:
            if ugod[i] != ugod_without_duplicates[-1]:
                ugod_without_duplicates.append(ugod[i])
    # подпишем
    dots_of_ugod.append(piketi[0])
    dots_of_ugod.append(piketi[-1])
    dots_of_ugod.sort()
    for i in range(len(ugod_without_duplicates)):
        msp.add_text("{0}".format(ugod_without_duplicates[i]), height=2, rotation=0,
                     dxfattribs={"style": "PK"}).set_placement(
            (dots_of_ugod[i] - 3 + (dots_of_ugod[i + 1] - dots_of_ugod[i]) / 2, - 30))

def communication_drawer(nazvaniya, piketi, otmetki, otmetki_old, msp):
    # print(nazvaniya)
    # print(piketi)
    # print(otmetki)
    piket_otmetka_nazvanie = []
    for i in range(len(nazvaniya)):
        if ('водд' in nazvaniya[i] or 'газ' in nazvaniya[i] or 'канал' in nazvaniya[i] or 'тепло' in nazvaniya[i]) \
                and '+' not in nazvaniya[i]:
            piket_otmetka_nazvanie.append([piketi[i], otmetki[i], nazvaniya[i]])
    # print(piket_otmetka_nazvanie)

    nums_of_communictaion = []
    # Выделим цифры
    for i in range(len(piket_otmetka_nazvanie)):
        nums_of_communictaion.append(re.findall(r'\d+', piket_otmetka_nazvanie[i][2]))
    for i in range(len(nums_of_communictaion)):
        for j in range(len(nums_of_communictaion[i])):
            nums_of_communictaion[i][j] = int(nums_of_communictaion[i][j])
    # print(nums_of_communictaion)
    new_nums = []
    tmp = 0
    for i in range(len(nums_of_communictaion)):
        for j in range(len(nums_of_communictaion[i])):
            if j == 0:
                tmp1 = (nums_of_communictaion[i][j] / 100)
            elif j == 1:
                if nums_of_communictaion[i][j] == 0:
                    tmp = 0
                else:
                    tmp += nums_of_communictaion[i][j]
            elif j == 2:
                tmp += float(nums_of_communictaion[i][j]) / 10
        new_nums.append([tmp1, tmp * 10])
        tmp = 0

    start_points_for_label = []
    # Рисуем трубу
    for i in range(len(piket_otmetka_nazvanie)):
        verh = piket_otmetka_nazvanie[i][1] - new_nums[i][1]
        niz = piket_otmetka_nazvanie[i][1] - new_nums[i][1] - new_nums[i][0]
        if verh - niz <= 0.25:
            otstup = 0.08
        elif verh - niz > 0.25 and verh - niz < 1:
            otstup = 0.12
        elif verh - niz >= 1 and verh - niz <= 250:
            otstup = 0.25
        else:
            otstup = 0.5

        start_point = [piket_otmetka_nazvanie[i][0], verh]
        end_point = [piket_otmetka_nazvanie[i][0], niz]
        def_point = [piket_otmetka_nazvanie[i][0] - otstup, verh - (verh - niz) / 2]
        start_points_for_label.append(start_point)

        arc = ConstructionArc.from_3p(
            start_point=start_point,
            end_point=end_point,
            def_point=def_point
        )
        arc.add_to_layout(msp)

        def_point = (piket_otmetka_nazvanie[i][0] + otstup, verh - (verh - niz) / 2)
        start_point, end_point = end_point, start_point
        arc = ConstructionArc.from_3p(
            start_point=start_point,
            end_point=end_point,
            def_point=def_point
        )
        arc.add_to_layout(msp)

    # Подготовим данные об отметках
    otmetki_labels_comm = []
    for i in range(len(nazvaniya)):
        if ('водд' in nazvaniya[i] or 'газ' in nazvaniya[i] or 'канал' in nazvaniya[i] or 'тепло' in nazvaniya[i]) \
                and '+' not in nazvaniya[i]:
            otmetki_labels_comm.append(otmetki_old[i])
    # print(new_nums)
    # print(otmetki_labels_comm)

    # Добавим сноски
    for i in range(len(start_points_for_label)):
        msp.add_line(start_points_for_label[i], [start_points_for_label[i][0] + 4,
                                                 start_points_for_label[i][1] + 25])

        # Triangle +0.06, +1.87 -> +1.26 + 1.87 -> +0.65 + 0.54 -> +0.06, +1.87
        msp.add_polyline2d([[start_points_for_label[i][0] + 4 + 0.06, start_points_for_label[i][1] + 25 + 1.87],
                            [start_points_for_label[i][0] + 4 + 1.26, start_points_for_label[i][1] + 25 + 1.87],
                            [start_points_for_label[i][0] + 4 + 0.65, start_points_for_label[i][1] + 25 + 0.54],
                            [start_points_for_label[i][0] + 4 + 0.06, start_points_for_label[i][1] + 25 + 1.87]])
        # Подпишем + 2.05, + 1.3
        msp.add_text("{:.2f}".format(float(otmetki_labels_comm[i]) - (new_nums[i][1] / 10)),
                     height=2.5, rotation=0,
                     dxfattribs={"style": "PK"}).set_placement([start_points_for_label[i][0] + 4 + 2.05,
                                                                start_points_for_label[i][1] + 25 + 0.5])
        #horiz lines
        if len(str("{:.2f}".format(float(otmetki_labels_comm[i]) - (new_nums[i][1] / 10)))) == 6:
            msp.add_line([start_points_for_label[i][0] + 4, start_points_for_label[i][1] + 25],
                         [start_points_for_label[i][0] + 16.2, start_points_for_label[i][1] + 25])
        else:
            msp.add_line([start_points_for_label[i][0] + 4, start_points_for_label[i][1] + 25],
                         [start_points_for_label[i][0] + 14, start_points_for_label[i][1] + 25])
    # кабели
    piket_otmetka_nazvanie_kab = []
    nums_of_kabels = []
    for i in range(len(nazvaniya)):
        if 'кабель' in nazvaniya[i]:
            piket_otmetka_nazvanie_kab.append([piketi[i], otmetki[i], nazvaniya[i]])
    for i in range(len(piket_otmetka_nazvanie_kab)):
        nums_of_kabels.append(re.findall(r'\d+', piket_otmetka_nazvanie_kab[i][2]))
    for i in range(len(nums_of_kabels)):
        for j in range(len(nums_of_kabels[i])):
            nums_of_kabels[i][j] = int(nums_of_kabels[i][j])

    # Убираем лишние
    new_nums_for_kabels = []
    for i in range(len(nums_of_kabels)):
        new_nums_for_kabels.append([nums_of_kabels[i][-2], nums_of_kabels[i][-1]])

    # Получаем цифры
    extra_new_nums_for_kabels = []
    tmp = 0
    for i in range(len(new_nums_for_kabels)):
        for j in range(len(new_nums_for_kabels[i])):
            if j == 0:
                tmp = new_nums_for_kabels[i][j]
            elif j == 1:
                tmp += new_nums_for_kabels[i][j] / 10
        extra_new_nums_for_kabels.append(tmp * 10)
        tmp = 0

    # Находим точки
    start_points_for_kabel_labels = []
    for i in range(len(piket_otmetka_nazvanie_kab)):
        start_points_for_kabel_labels.append([piket_otmetka_nazvanie_kab[i][0],
                                              piket_otmetka_nazvanie_kab[i][1] - extra_new_nums_for_kabels[i]])

    # Рисуем кабель r = 0.025,
    for i in range(len(start_points_for_kabel_labels)):
        msp.add_circle(start_points_for_kabel_labels[i], 0.025)
        msp.add_circle(start_points_for_kabel_labels[i], 0.05)
        msp.add_circle(start_points_for_kabel_labels[i], 0.075)
        msp.add_circle(start_points_for_kabel_labels[i], 0.1)
        msp.add_circle(start_points_for_kabel_labels[i], 0.125)
        msp.add_circle(start_points_for_kabel_labels[i], 0.150)
    # Подготовим данные
    # print(extra_new_nums_for_kabels)
    otmetki_labels_kab = []
    for i in range(len(nazvaniya)):
        if 'кабель' in nazvaniya[i]:
            otmetki_labels_kab.append(otmetki_old[i])
    # print(otmetki_labels_kab)
    # добавим отметку
    for i in range(len(start_points_for_kabel_labels)):
        msp.add_line(start_points_for_kabel_labels[i], [start_points_for_kabel_labels[i][0] + 4,
                                                        start_points_for_kabel_labels[i][1] + 25])
        # horiz lines
        msp.add_line([start_points_for_kabel_labels[i][0] + 4, start_points_for_kabel_labels[i][1] + 25],
                     [start_points_for_kabel_labels[i][0] + 14, start_points_for_kabel_labels[i][1] + 25])

        #horizline
        if len(str("{:.2f}".format(float(otmetki_labels_kab[i]) - (extra_new_nums_for_kabels[i] / 10)))) == 6:
            msp.add_line([start_points_for_kabel_labels[i][0] + 4, start_points_for_kabel_labels[i][1] + 25],
                         [start_points_for_kabel_labels[i][0] + 16.2, start_points_for_kabel_labels[i][1] + 25])
        else:
            msp.add_line([start_points_for_kabel_labels[i][0] + 4, start_points_for_kabel_labels[i][1] + 25],
                         [start_points_for_kabel_labels[i][0] + 14, start_points_for_kabel_labels[i][1] + 25])
        # Triangle +0.06, +1.87 -> +1.26 + 1.87 -> +0.65 + 0.54 -> +0.06, +1.87
        msp.add_polyline2d(
            [[start_points_for_kabel_labels[i][0] + 4 + 0.06, start_points_for_kabel_labels[i][1] + 25 + 1.87],
             [start_points_for_kabel_labels[i][0] + 4 + 1.26, start_points_for_kabel_labels[i][1] + 25 + 1.87],
             [start_points_for_kabel_labels[i][0] + 4 + 0.65, start_points_for_kabel_labels[i][1] + 25 + 0.54],
             [start_points_for_kabel_labels[i][0] + 4 + 0.06, start_points_for_kabel_labels[i][1] + 25 + 1.87]])
        # Подпишем + 2.05, + 1.3
        msp.add_text("{:.2f}".format(float(otmetki_labels_kab[i]) - (extra_new_nums_for_kabels[i] / 10)),
                     height=2.5, rotation=0,
                     dxfattribs={"style": "PK"}).set_placement([start_points_for_kabel_labels[i][0] + 4 + 2.05,
                                                                start_points_for_kabel_labels[i][1] + 25 + 0.5])

def last_pk_drawer(piketi, msp):
    if piketi[-1] < 200:
        msp.add_text("ПК 0+{0}".format((piketi[-1] / 2).__round__(3)), height=2.5, rotation=90,
                     dxfattribs={"style": "PK"}).set_placement((piketi[-1] + 3.5, 30.5))
    else:
        num = piketi[-1]
        num = num / 2
        num = str(num)
        celoe = int(num[0])
        drobnoe = float(num[1:])

        if float(num[1:]) < 10.0:
            msp.add_text("ПК {0}+0{1}".format(celoe, drobnoe), height=2.5, rotation=90,
                     dxfattribs={"style": "PK"}).set_placement((piketi[-1] + 3.5, 30.5))
        else:
            msp.add_text("ПК {0}+{1}".format(celoe, drobnoe), height=2.5, rotation=90,
                         dxfattribs={"style": "PK"}).set_placement((piketi[-1] + 3.5, 30.5))
def lower_table_drawer(piketi, msp):
    lower_table_dots = [[0, 0], [0, -173], [piketi[-1], -173], [piketi[-1], 0], [0, 0]]
    lower_table_border_dots = [[0, -15], [piketi[-1], -15], [piketi[-1], -25], [0, -25], [0, -34], [piketi[-1], -34], [piketi[-1], -48], [0, -48],
                  [0, -63], [piketi[-1], -63], [piketi[-1], -78], [0, -78], [0, -93], [piketi[-1], -93], [piketi[-1], -109], [0, -109],
                  [0, -119], [piketi[-1], -119], [piketi[-1], -129], [0, -129], [0, -139], [piketi[-1], -139], [piketi[-1], -154], [0, -154],
                  [0, -173], [piketi[-1], -173]]
    msp.add_line([-5, -119], [-65, -129])
    msp.add_polyline2d(lower_table_dots)
    msp.add_polyline2d(lower_table_border_dots)
def left_table_drawer(msp):
    left_table_dots = [[- 5, 0], [-65, 0], [-65, -173], [-5, -173], [-5, 0]]
    left_table_border_dots = [[-65, -15], [-5, -15], [-5, -25], [-65, -25], [-65, -34], [-5, -34], [-5, -48], [-65, -48],
                  [-65, -63], [-5, -63], [-5, -78], [-65, -78], [-65, -93], [-5, -93], [-5, -109], [-65, -109],
                  [-65, -119], [-5, -119], [-5, -129], [-65, -129], [-65, -139], [-5, -139], [-5, -154], [-65, -154],
                  [-65, -173], [-5, -173]]
    msp.add_line([-5, -119], [-65, -129])
    msp.add_polyline2d(left_table_dots)
    msp.add_polyline2d(left_table_border_dots)
    #Заполним ячейки левой таблицы
    text_dots_for_left_table = [[-65 + 6, -6.5], [-65 + 14.7, -12], [-65 + 5.2, -15-3.5], [-65 + 6.3, -15-8.93],
                                [-65+22.14, -25-5.8],
                 [-65 + 14.44, -34 - 5.66], [-65 + 14.85, -34 - 10.92], [-65 + 6.68, -48 - 8.62] , [-65 + 7.2, -63 - 9.1],
                 [-65 + 10.55, -78 - 9], [-65 + 11.31, -93 - 7], [-65 + 14.5, -93 - 12.5], [-65 + 19.43,
                                                                                                   -109 - 6.6],
                 [-65 + 3.23, -119 - 4.4], [-65 + 39.91, -119 - 8], [-65 + 17, -129 - 6.2], [-65 + 23.52,
                                                                                                  -139 - 8.9],
                 [-65 + 12.06, -154 - 11]]
    text_for_left_table = ['Инженерно-геологическая', 'характеристика', 'Удельное электросопро-',
                            'тивление грунтов Ом.м',
                           'Угодья', 'Отметка земли', 'фактическая, м', 'Отметка дна траншеи, м',
                           'Отметка верха трубы,  м', 'Глубина траншеи , м', 'Обозначение трубы', 'и тип изоляции',
                           'Основание', 'Уклон  %', 'Длина, м', 'Расстояние,  м', 'Пикет', 'Развернутый план']
    for i in range(len(text_dots_for_left_table)):
        msp.add_text("{0}".format(text_for_left_table[i]), height=3, rotation=0,
                     dxfattribs={"style": "PK"}).set_placement(text_dots_for_left_table[i])
def pk_drawer(piketi, msp):
    #Первый пикет
    msp.add_text("0", height=3, rotation=0,
                dxfattribs={"style": "PK"}).set_placement((piketi[0] + 0.5, -148))
    #следующие пикеты
    tmp_rass = 200
    tmp_pk = 1
    while True:
        if tmp_rass < piketi[-1]:
            msp.add_text(f"{tmp_pk}", height=3, rotation=0,
                         dxfattribs={"style": "PK"}).set_placement((tmp_rass, -148))
            tmp_rass += 200
            tmp_pk += 1
        else:
            break

def rails_drawer(piketi, otmetki, nazvaniya, otmetki_old, msp):
    pk_with_rails = []
    otmetki_with_rails = []
    otmetki_for_rails = []
    for i in range(len(nazvaniya)):
        if 'рельс' in nazvaniya[i]:
            pk_with_rails.append(piketi[i])
            otmetki_with_rails.append(otmetki[i])
            otmetki_for_rails.append(otmetki_old[i])
    dots_for_rails = []
    for i in range(len(pk_with_rails)):
        dots_for_rails.append([pk_with_rails[i], otmetki_with_rails[i]])
        dots_for_rails.append([pk_with_rails[i], otmetki_with_rails[i] - 1])
        dots_for_rails.append([pk_with_rails[i], otmetki_with_rails[i]])
        dots_for_rails.append([pk_with_rails[i]-0.5, otmetki_with_rails[i]])
        dots_for_rails.append([pk_with_rails[i]+0.5, otmetki_with_rails[i]])
        msp.add_polyline2d(dots_for_rails, dxfattribs={"layer": "rails"})
        dots_for_rails = []
    for i in range(len(pk_with_rails)):
        msp.add_line([pk_with_rails[i], otmetki_with_rails[i]], [pk_with_rails[i] + 4, otmetki_with_rails[i] + 25])
        msp.add_line([pk_with_rails[i]+4, otmetki_with_rails[i]+25], [pk_with_rails[i]+22, otmetki_with_rails[i] + 25])
        msp.add_text('г.р. {0}'.format(otmetki_for_rails[i]), height=2.5, rotation=0,
                     dxfattribs={"style": "PK"}).set_placement([pk_with_rails[i] + 4 + 2.05,
                                                                otmetki_with_rails[i] + 25 + 0.5])


def distance_drawer(piketi, msp):
    #Построим отрезки точек
    for i in range(len(piketi)):
        if piketi[i] == 0.0 or piketi[i] == piketi[-1]:
            continue
        else:
            if piketi[i] % 100 == 0:
                msp.add_line([piketi[i], -139], [piketi[i], -132])
            else:
                msp.add_line([piketi[i], -139], [piketi[i], -137])
    #Добавим подписи расстояний
    tmp = 0
    for i in range(len(piketi)):
        if piketi[i] == piketi[0]:
            continue
        else:
            tmp = (piketi[i] - piketi[i-1]) / 2
            msp.add_text(f"{tmp.__round__(2)}", height=2.2, rotation=90,
                         dxfattribs={"style": "PK"}).set_placement((piketi[i] - tmp + 1, -136))


def profile_drawer(piketi, otmetki, msp):
    msp.add_line((piketi[0], 0), (piketi[-1], 0)) #горизонтальная линия всего профа
    for i in range(len(piketi)): #Вертикальные линии
        msp.add_line((piketi[i], 0), (piketi[i], otmetki[i]))
    dots_for_polyline = []
    for i in range(len(piketi)):
        dots_for_polyline.append([piketi[i], otmetki[i]])
    msp.add_polyline2d(dots_for_polyline)

def otmetki_drawer(otmetki_old, piketi, msp):
    for i in range(len(otmetki_old)):
        #4x значные
        if len(otmetki_old[i]) == 4:
            if otmetki_old[i] != otmetki_old[-1] and otmetki_old[i] != otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] + 1, -44))
            elif otmetki_old[i] == otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] + 2.4, -44))
            else:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.2, -44))
        #5 значные
        elif len(otmetki_old[i]) == 5:
            if otmetki_old[i] != otmetki_old[-1] and otmetki_old[i] != otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] + 1, -45))
            elif otmetki_old[i] == otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] + 2.4, -45))
            else:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.2, -45))
        #6значные
        elif len(otmetki_old[i]) == 6:
            if otmetki_old[i] != otmetki_old[-1] and otmetki_old[i] != otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] + 1, -46))
            elif otmetki_old[i] == otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] + 2.4, -46))
            else:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.2, -46))
        #7значные
        elif len(otmetki_old[i]) == 7:
            if otmetki_old[i] != otmetki_old[-1] and otmetki_old[i] != otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] + 1, -47))
            elif otmetki_old[i] == otmetki_old[0]:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] + 2.4, -47))
            else:
                msp.add_text(f"{otmetki_old[i]}", height=2.2, rotation=90,
                            dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.2, -47))

def ordinata_naming(nazvaniya, piketi, msp):
    new_nazvaniya = []
    for i in nazvaniya:
        new_nazvaniya.append(i)
    for i in range(len(new_nazvaniya)):
        if 'рельс' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('рельс', 'рельс ж. д.')
        if 'тепло' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('тепло', 'теплотрасса ')
        if 'гл.' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('гл.', ' гл. ')
        if 'ЛЭП' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('ЛЭП', 'ЛЭП ')
        if 'канал' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('канал', 'канализация ')
        if 'газ' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('газ', 'газопровод ')
        if 'водд' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('водд', 'водопровод ')
        if 'кабель' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('кабель', 'кабель ')
        if 'отвод' in new_nazvaniya[i]:
            new_nazvaniya[i] = new_nazvaniya[i].replace('отвод', 'проектируемый газопровод отвод')

        if new_nazvaniya[i] == 'р' or new_nazvaniya[i] == 'н.тр' or new_nazvaniya[i] == 'к.тр' or i == 0 or i == len(new_nazvaniya) - 1\
                or new_nazvaniya[i] == 'угод':
            continue
        else:
            if piketi[i] < 200:
                msp.add_text("+{0} {1}".format((piketi[i] / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 400 and piketi[i] > 200:
                msp.add_text("+{0} {1}".format(((piketi[i] - 200) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 600 and piketi[i] > 400:
                msp.add_text("+{0} {1}".format(((piketi[i] - 400) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 800 and piketi[i] > 600:
                msp.add_text("+{0} {1}".format(((piketi[i] - 600) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 1000 and piketi[i] > 800:
                msp.add_text("+{0} {1}".format(((piketi[i] - 800) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 1200 and piketi[i] > 1000:
                msp.add_text("+{0} {1}".format(((piketi[i] - 1000) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 1400 and piketi[i] > 1200:
                msp.add_text("+{0} {1}".format(((piketi[i] - 1200) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 1600 and piketi[i] > 1400:
                msp.add_text("+{0} {1}".format(((piketi[i] - 1400) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 1800 and piketi[i] > 1600:
                msp.add_text("+{0} {1}".format(((piketi[i] - 1600) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 2000 and piketi[i] > 1800:
                msp.add_text("+{0} {1}".format(((piketi[i] - 1800) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 2200 and piketi[i] > 2000:
                msp.add_text("+{0} {1}".format(((piketi[i] - 2000) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 2400 and piketi[i] > 2200:
                msp.add_text("+{0} {1}".format(((piketi[i] - 2200) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))
            elif piketi[i] < 2600 and piketi[i] > 2400:
                msp.add_text("+{0} {1}".format(((piketi[i] - 2400) / 2).__round__(2), new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))

            else:
                msp.add_text("+00.0 {0}".format(new_nazvaniya[i]), height=1.6, rotation=90,
                             dxfattribs={"style": "PK"}).set_placement((piketi[i] - 0.3, 1.5))

def prof_writer(name_of_file, piketi, otmetki, otmetki_old, nazvaniya, ugod):
    #Инициализация
    doc = ezdxf.new("R2010")
    doc.layers.add(name="rails", lineweight=35)
    msp = doc.modelspace()
    #Сам профиль!
    profile_drawer(piketi, otmetki, msp)
    #Подписи ПК
    #Первый ПК
    doc.styles.new("PK", dxfattribs={"font": "Times New Roman.ttf"})
    msp.add_text("ПК 0+00.0", height=2.5, rotation=90,
                 dxfattribs={"style": "PK"}).set_placement((piketi[0] - 1, 30.5))
    #Последний ПК
    last_pk_drawer(piketi, msp)

    #Название и масштаб(подписи)
    msp.add_text("трасса {0}".format(name_of_file), height=2.5, rotation=0,
                 dxfattribs={"style": "PK"}).set_placement((-41, 83))
    msp.add_text("М", height=2.5, rotation=0,
                 dxfattribs={"style": "PK"}).set_placement((-46.3, 50))
    msp.add_line((-41, 51.2), (-23, 51.2))
    msp.add_text("гор 1:500", height=2.5, rotation=0,
                 dxfattribs={"style": "PK"}).set_placement((-40, 52.5))
    msp.add_text("верт 1:100", height=2.5, rotation=0,
                 dxfattribs={"style": "PK"}).set_placement((-40, 48.3))

    #будущая рейка сейчас просто линия
    msp.add_line([-5, 0], [-5, 140])

    #Таблица левая
    left_table_drawer(msp)
    #Таблица нижняя
    lower_table_drawer(piketi, msp)
    #Заполним ячейки нижней таблицы
    #Пикеты
    pk_drawer(piketi, msp)
    #Расстояния
    distance_drawer(piketi, msp)
    #Отметки
    otmetki_drawer(otmetki_old, piketi, msp)
    #Угодья
    ugod_drawer(ugod, piketi, msp)
    #Подпись ординат 1.5
    ordinata_naming(nazvaniya, piketi, msp)
    #рельсы
    rails_drawer(piketi, otmetki, nazvaniya, otmetki_old, msp)
    #Нарисуем трубы
    communication_drawer(nazvaniya, piketi, otmetki, otmetki_old, msp)

    #Сохраняем файл
    doc.saveas(name_of_file + '.dxf')

# prof_writer('first_prof', [0.0, 0.6, 26.0, 52.6, 60.8, 62.6, 200, 204], [63.2, 63.2, 62.2, 60.0, 62.0, 62.0, 65, 65],
#             ['6.97', '6.97', '11.87', '101.65', '1001.85', '6.85', '6.90', '7.40'], ['н.тр.', 'ЛЭП0,4кВ', 'воддст.200гл.0.7', 'кабель0,4кВгл.1.2',
#                                                                                 'ЛЭП0,4кВ', 'газчуг.150гл.1.2', 'кабельсвязигл.1.0', 'к.тр.'],
#             ['выгон', 'выгон', 'выгон', 'п.д.', 'щеб.', 'щеб.', 'выгон', 'выгон'])

# prof_writer('рыжова63А', scaling_piketov(['0+00.0', '0+12.3', '0+13.5', '0+18.2', '0+26.6', '0+27.0', '0+30.7']),
#             scaling_otmetok([31.60, 30.65, 30.60, 30.20, 29.65, 29.65, 29.30]), ['31.60', '30.65', '30.60', '30.20', '29.65', '29.65', '29.30'],
#             ['н.тр.', 'УП1', 'ЛЭП0,4кВ', 'УП2', 'УП3', 'угод', 'к.тр.'], ['щеб.дор.', 'щеб.дор.', 'щеб.дор.', 'щеб.дор.', 'щеб.дор.', 'выгон', 'выгон'])

