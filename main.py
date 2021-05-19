import cv2
import numpy as np
import pyautogui
from time import sleep
from pynput.keyboard import Key, Listener

# each element = (name, image, height, width)
continents = [('South America', 'continents/south_america.png', 650, 630),
              ('Africa', 'continents/africa.png', 800, 550),
              ('Antarctica', 'continents/antarctica.png', 850, 880),
              ('Asia', 'continents/asia.png', 1000, 500),
              ('Australia', 'continents/australia.png', 1200, 700),
              ('Europe', 'continents/europe.png', 880, 440),
              ('North America', 'continents/north_america.png', 500, 500)]

countries = [
    ('Afghanistan', 'countries/Afghanistan.png', 960, 485),
    ('Albania', 'countries/Albania.png', 809, 452),
    ('Algeria', 'countries/Algeria.png', 757, 506),
    ('Angola', 'countries/Angola.png', 800, 640),
    ('Argentina', 'countries/Argentina.png', 537, 712),
    ('Armenia', 'countries/Armenia.png', 890, 457),
    ('Australia', 'countries/Australia.png', 1194, 681),
    ('Austria', 'countries/Austria.png', 791, 425),
    ('Azerbajdzhan', 'countries/Azerbajdzhan.png', 899, 454),
    ('Bangladesh', 'countries/Bangladesh.png', 1036, 522),
    ('Belarus', 'countries/Belarus.png', 834, 399),
    ('Belgium', 'countries/Belgium.png', 760, 415),
    ('Belize', 'countries/Belize.png', 458, 540),
    ('Benin', 'countries/Benin.png', 752, 566),
    ('Bolivia', 'countries/Bolivia.png', 537, 655),
    ('Bosnia and Herzegovina', 'countries/Bosnia and Herzegovina.png', 801, 440),
    ('Botswana', 'countries/Botswana.png', 823, 675),
    ('Brazil', 'countries/Brazil.png', 585, 642),
    ('British guiana', 'countries/British guiana.png', 554, 580),
    ('Bulgaria', 'countries/Bulgaria.png', 825, 446),
    ('Burkina faso', 'countries/Burkina faso.png', 740, 558),
    ('Burundi', 'countries/Burundi.png', 842, 612),
    ('Butane', 'countries/Butane.png', 1036, 504),
    ('Cambodia', 'countries/Cambodia.png', 1086, 557),
    ('Cameroon', 'countries/Cameroon.png', 784, 582),
    ('Canada', 'countries/Canada.png', 402, 370),
    ('Central African Republic', 'countries/Central African Republic.png', 816, 579),
    ('Chad', 'countries/Chad.png', 802, 547),
    ('Chile', 'countries/Chile.png', 514, 729),
    ('China', 'countries/China.png', 1078, 468),
    ('Code devouar', 'countries/Code devouar.png', 727, 576),
    ('Colombia', 'countries/Colombia.png', 502, 586),
    ('Congo', 'countries/Congo.png', 796, 601),
    ('Costa Rica', 'countries/Costa Rica.png', 472, 569),
    ('Cuba', 'countries/Cuba.png', 492, 527),
    ('Czech Republic', 'countries/Czech Republic.png', 789, 415),
    ('Denmark', 'countries/Denmark.png', 774, 386),
    ('Djibouti', 'countries/Djibouti.png', 883, 560),
    ('Dominican Republic', 'countries/Dominican Republic.png', 516, 538),
    ('Democratic Republic of the Congo', 'countries/Democratic Republic of the Congo.png', 820, 607),
    ('Ecuador', 'countries/Ecuador.png', 491, 607),
    ('Egypt', 'countries/Egypt.png', 843, 504),
    ('El Salvador', 'countries/El Salvador.png', 456, 553),
    ('Equatorial Guinea', 'countries/Equatorial Guinea.png', 779, 595),
    ('Eritrea', 'countries/Eritrea.png', 867, 545),
    ('Estonia', 'countries/Estonia.png', 827, 373),
    ('Ethiopia', 'countries/Ethiopia.png', 871, 569),
    ('Finland', 'countries/Finland.png', 830, 341),
    ('France', 'countries/France.png', 754, 429),
    ('Gabon', 'countries/Gabon.png', 784, 602),
    ('Georgia', 'countries/Georgia.png', 885, 450),
    ('Germany', 'countries/Germany.png', 772, 402),
    ('Gold coast', 'countries/Gold coast.png', 741, 572),
    ('Greece', 'countries/Greece.png', 820, 470),
    ('Guatemala', 'countries/Guatemala.png', 451, 548),
    ('Guinea', 'countries/Guinea.png', 710, 567),
    ('Guinea-bissau', 'countries/Guinea-bissau.png', 696, 559),
    ('Haiti', 'countries/Haiti.png', 510, 534),
    ('Honduras', 'countries/Honduras.png', 462, 550),
    ('Hrvatska', 'countries/Hrvatska.png', 797, 434),
    ('Hungary', 'countries/Hungary.png', 808, 430),
    ('Iceland', 'countries/Iceland.png', 682, 347),
    ('India', 'countries/India.png', 1003, 522),
    ('Indonesia', 'countries/Indonesia.png', 1128, 603),
    ('Iran', 'countries/Iran.png', 922, 484),
    ('Iraq', 'countries/Iraq.png', 884, 485),
    ('Ireland', 'countries/Ireland.png', 717, 400),
    ('Israel', 'countries/Israel.png', 858, 489),
    ('Italy', 'countries/Italy.png', 788, 450),
    ('Japan', 'countries/Japan.png', 1195, 473),
    ('Jordan', 'countries/Jordan.png', 862, 497),
    ('Kazakhstan', 'countries/Kazakhstan.png', 968, 426),
    ('Kenya', 'countries/Kenya.png', 864, 600),
    ('Kongo', 'countries/Kongo.png', 819, 608),
    ('Kyrgyzstan', 'countries/Kyrgyzstan.png', 987, 450),
    ('Laos', 'countries/Laos.png', 1078, 535),
    ('Latvia', 'countries/Latvia.png', 829, 384),
    ('Lesotho', 'countries/Lesotho.png', 836, 703),
    ('Liberia', 'countries/Liberia.png', 713, 578),
    ('Libya', 'countries/Libya.png', 798, 502),
    ('Lithuania', 'countries/Lithuania.png', 823, 391),
    ('Madagascar', 'countries/Madagascar.png', 896, 661),
    ('Malawi', 'countries/Malawi.png', 854, 644),
    ('Malaya', 'countries/Malaya.png', 1080, 590),
    ('Mali', 'countries/Mali.png', 738, 537),
    ('Mauritania', 'countries/Mauritania.png', 712, 535),
    ('Mexico', 'countries/Mexico.png', 412, 525),
    ('Moldova', 'countries/Moldova.png', 837, 428),
    ('Mongolia', 'countries/Mongolia.png', 1064, 427),
    ('Morocco', 'countries/Morocco.png', 721, 490),
    ('Mozambic', 'countries/Mozambic.png', 855, 666),
    ('Myanmar', 'countries/Myanmar.png', 1058, 530),
    ('Namibia', 'countries/Namibia.png', 798, 675),
    ('Nepal', 'countries/Nepal.png', 1013, 501),
    ('Netherlands', 'countries/Netherlands.png', 761, 405),
    ('New Zealand', 'countries/New Zealand.png', 1299, 756),
    ('Nicaragua', 'countries/Nicaragua.png', 471, 556),
    ('Nigeria', 'countries/Nigeria.png', 766, 572),
    ('Nigger', 'countries/Nigger.png', 775, 545),
    ('North Korea', 'countries/North Korea.png', 1155, 460),
    ('North macedonia', 'countries/North macedonia.png', 815, 452),
    ('Norway', 'countries/Norway.png', 823, 314),
    ('Oman', 'countries/Oman.png', 930, 526),
    ('Pakistan', 'countries/Pakistan.png', 968, 498),
    ('Panama', 'countries/Panama.png', 483, 571),
    ('Papua New Guinea', 'countries/Papua New Guinea.png', 1209, 623),
    ('Paraguay', 'countries/Paraguay.png', 558, 680),
    ('Peru', 'countries/Peru.png', 500, 627),
    ('Philippines', 'countries/Philippines.png', 1144, 563),
    ('Pipa americana', 'countries/Pipa americana.png', 564, 586),
    ('Poland', 'countries/Poland.png', 809, 410),
    ('Portugal', 'countries/Portugal.png', 717, 457),
    ('Romania', 'countries/Romania.png', 823, 431),
    ('Russia', 'countries/Russia.png', 1042, 343),
    ('Rwanda', 'countries/Rwanda.png', 841, 606),
    ('Saudi Arabia', 'countries/Saudi Arabia.png', 890, 524),
    ('Senegal', 'countries/Senegal.png', 697, 552),
    ('Serbia', 'countries/Serbia.png', 811, 444),
    ('Sierra Leone', 'countries/Sierra Leone.png', 705, 573),
    ('Slovakia', 'countries/Slovakia.png', 805, 422),
    ('Solomon islands', 'countries/Solomon islands.png', 1264, 630),
    ('Somalia', 'countries/Somalia.png', 903, 567),
    ('South Africa', 'countries/South Africa.png', 823, 707),
    ('South Korea', 'countries/South Korea.png', 1159, 473),
    ('South Sudan', 'countries/South Sudan.png', 833, 578),
    ('Spain', 'countries/Spain.png', 734, 459),
    ('Sri lanka', 'countries/Sri lanka.png', 1008, 576),
    ('Sudan', 'countries/Sudan.png', 841, 542),
    ('Sweden', 'countries/Sweden.png', 801, 353),
    ('Switzerland', 'countries/Switzerland.png', 770, 430),
    ('Syria', 'countries/Syria.png', 869, 477),
    ('Taiwan', 'countries/Taiwan.png', 1137, 521),
    ('Tajikistan', 'countries/Tajikistan.png', 977, 463),
    ('Tanzania', 'countries/Tanzania.png', 856, 626),
    ('Thailand', 'countries/Thailand.png', 1071, 550),
    ('Togo', 'countries/Togo.png', 747, 572),
    ('Tunis', 'countries/Tunis.png', 775, 483),
    ('Turkey', 'countries/Turkey.png', 855, 459),
    ('Turkmenia', 'countries/Turkmenia.png', 935, 459),
    ('UAE', 'countries/UAE.png', 920, 521),
    ('UK', 'countries/UK.png', 739, 402),
    ('USA', 'countries/USA.png', 433, 462),
    ('Uganda', 'countries/Uganda.png', 850, 598),
    ('Ukraine', 'countries/Ukraine.png', 846, 418),
    ('Uruguay', 'countries/Uruguay.png', 564, 717),
    ('Uzbekistan', 'countries/Uzbekistan.png', 954, 452),
    ('Venezuela', 'countries/Venezuela.png', 534, 576),
    ('Vietnam', 'countries/Vietnam.png', 1096, 558),
    ('Yemen', 'countries/Yemen.png', 895, 548),
    ('Zambia', 'countries/Zambia.png', 826, 649),
    ('Zimbabwe', 'countries/Zimbabwe.png', 840, 666)
]


def take_screenshot():
    img = pyautogui.screenshot(region=(460, 100, 850, 50))
    img = cv2.cvtColor(np.array(img.getdata(), dtype='uint8').reshape((img.size[1], img.size[0], 3)),
                       cv2.COLOR_BGR2GRAY)
    return img


def find_patt(image, pattern, thres):
    (patt_H, patt_W) = pattern.shape[:2]
    res = cv2.matchTemplate(image, pattern, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > thres)
    return patt_H, patt_W, loc[::-1]


def play(patterns):
    sleep(0.005)
    img = take_screenshot()
    for patt in patterns:
        p_img = cv2.imread(patt[1], 0)
        h, w, points = find_patt(img, p_img, 0.92)
        if len(points[0]) != 0:
            print(patt[0])
            pyautogui.moveTo(patt[2], patt[3])
            pyautogui.click()
            break


def on_press(key):
    if key == Key.ctrl:
        for _ in range(152):
            play(countries)


with Listener(on_press=on_press) as listener:
    listener.join()
