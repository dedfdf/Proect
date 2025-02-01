from pygame.sprite import Group as group

all_sprite = group()  # все спрайты
cursor_group = group()  # курсор
grass_group = group()
object_group = group()  # все объекты карты
box_group = group()
bullet_group = group()  # пули
player_group = group()  # персонаж
wall_group = group()  # объекты столкновения с игроком
collision_circle_group = group()  # коллизии для игрока
object_block_visible_group = group()  # объекты, которые блокируют взгляд игрока
not_visible_object_group = group()  # объекты которые игрок не может видеть без света
items_group = group()  # группа предметов
grenade_group = group()  # группа гранат
items_visible_object_groups = group()  # группа предметов, которые игрок видит
visible_object_group = group()  # объекты, которые игрок видит
icon_group = group()  # все иконки во время игры
opponents_group = group()  # группа противников
dust_group = group()  # группа пыли

all_group = [all_sprite, cursor_group, grass_group, object_group, box_group, bullet_group,
             player_group, wall_group, collision_circle_group, object_block_visible_group,
             not_visible_object_group, items_group, grenade_group, items_visible_object_groups,
             visible_object_group, icon_group, opponents_group, dust_group]
#  список всех групп
