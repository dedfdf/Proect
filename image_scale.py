from pygame.transform import scale
from main_func import load_image
from consts import PERCENT_SCALE

percent = PERCENT_SCALE


# изменяет разрешение объекта
def set_scale(im):
    print(im.get_size())
    w, h = im.get_size()
    im = scale(im, (w * percent, h * percent))
    return im


image_bullet = set_scale(load_image('bullet.png'))

armor_icon = set_scale(load_image(f'icon/armor_icon.png', 'items'))
armor = set_scale(load_image(f'icon/armor.png', 'items'))

light_grenade_icon = set_scale(load_image(f'icon/light_grenade_icon.png', 'items'))
light_grenade = set_scale(load_image(f'icon/light_grenade.png', 'items'))

medicine_icon = set_scale(load_image(f'icon/medicine_icon.png', 'items'))
medicine = set_scale(load_image(f'icon/medicine.png', 'items'))

patron_icon = set_scale(load_image(f'icon/bullet_icon.png', 'items'))
patron = set_scale(load_image(f'icon/bullet.png', 'items'))

dict_weapons_icon = {'pistol': set_scale(load_image(f'icon/pistol.png', 'player')),
                     'automat': set_scale(load_image(f'icon/automat.png', 'player')),
                     'shotgun': set_scale(load_image(f'icon/shotgun.png', 'player')),
                     'knife': set_scale(load_image(f'icon/knife.png', 'player')),
                     'flashlight':
                         set_scale(load_image(f'icon/flashlight.png', 'player'))}

dict_health = {0: set_scale(load_image(f'icon/health_0.png', 'player')),
               1: set_scale(load_image(f'icon/health_1.png', 'player')),
               2: set_scale(load_image(f'icon/health_2.png', 'player')),
               3: set_scale(load_image(f'icon/health_3.png', 'player'))}

infinity = set_scale(load_image('icon/infinity.png', 'player'))

armor_big_icon = set_scale(load_image('icon/armor.png', 'player'))

# файл нужен для удобного изменения разрешения всех файлов
