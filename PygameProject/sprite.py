from pygame.sprite import Group as group

all_sprite = group()  # все спрайты
cursor_group = group()  # курсор
grass_group = group()
object_group = group()  # все объекты карты
box_group = group()
shoot_group = group()  # стрельба персонажа
bullet_group = group()  # пули
player_group = group()  # персонаж
wall_group = group()  # объекты столкновения с игроком
collision_circle_group = group()  # коллизии для игрока
dark_group = group()  # тьма на карте
object_block_visible_group = group()  # объекты, которые блокируют взгляд игрока
not_visible_object_group = group()  # объекты которые игрок не может видеть без света
visible_object_group = group()
circle_view_group = group()
