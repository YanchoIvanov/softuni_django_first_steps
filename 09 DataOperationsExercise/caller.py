import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name, species):
    Pet.objects.create(
        name=name,
        species=species,
    )
    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name, origin, age, description, is_magical):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )
    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    artifacts = Artifact.objects.all()
    artifacts.delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
#
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune',
# True))


def add_locations():
    Location.objects.create(
        name="Sofia",
        region="Sofia Region",
        population="1329000",
        description="The capital of Bulgaria and the largest city in the country",
        is_capital=False,
    )
    location2 = Location(
        name="Plovdiv",
        region="Plovdiv Region",
        population="346942",
        description="The second-largest city in Bulgaria with a rich historical heritage",
        is_capital=False,
    )
    location2.save()

    location3 = Location(
        name="Varna",
        region="Varna Region",
        population="330486",
        description="A city known for its sea breeze and beautiful beaches on the Black Sea",
        is_capital=False,
    )
    location3.save()


# add_locations()
# print(Location.objects.all())


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')
    location_info = []
    for location in locations:
        location_info.append(
         f"{location.name} has a population of {location.population}!"
        )
    return '\n'.join(location_info)


def new_capital():
    # Location.objects.filter(pk=1).update(is_capital=True)
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    location = Location.objects.first()
    location.delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def add_cars():
    Car.objects.create(
        model="Mercedes C63 AMG",
        year=2019,
        color="white",
        price=120000.00,
    )
    car2 = Car(
        model="Audi Q7 S line",
        year=2023,
        color="black",
        price=183900.00,
    )
    car2.save()

    car3 = Car(
        model="Chevrolet Corvette",
        year=2021,
        color="dark grey",
        price=199999.00,
    )
    car3.save()


# add_cars()
# print(Car.objects.all())


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        car.price_with_discount = float(car.price) * (1 - (sum(int(x) for x in str(car.year)) / 100))
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car():
    # Car.objects.last().delete()
    cars = Car.objects.last()
    cars.delete()


# apply_discount()
# print(get_recent_cars())


def add_tasks():
    Task.objects.create(
        title="Sample Task",
        description="This is a sample task description",
        due_date="2023-10-31",
        is_finished=False,
    )


# add_tasks()
# print(Task.objects.all())


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)
    tasks_info = []
    for task in tasks:
        tasks_info.append(
            f"Task - {task.title} needs to be done until {task.due_date}!"
        )
    return '\n'.join(tasks_info)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text, task_title):
    decode = ''.join(chr(ord(x) - 3) for x in text)
    matching_task = Task.objects.filter(title=task_title)

    for task in matching_task:
        task.description = decode
        task.save()


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title ='Simple Task') .description)


def add_rooms():
    HotelRoom.objects.create(
        room_number=101,
        room_type="Standard",
        capacity=2,
        amenities="Tv",
        price_per_night=100.00
    )
    room2 = HotelRoom(
        room_number=201,
        room_type="Deluxe",
        capacity=3,
        amenities="Wi-Fi",
        price_per_night=200.00
    )
    room2.save()

    room3 = HotelRoom(
        room_number=501,
        room_type="Deluxe",
        capacity=6,
        amenities="Jacuzzi",
        price_per_night=400.00
    )
    room3.save()


# add_rooms()
# print(HotelRoom.objects.all())


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    even_id_deluxe_rooms = []

    for room in deluxe_rooms:
        if room.id % 2 == 0:
            even_id_deluxe_rooms.append(str(room))

    return '\n'.join(even_id_deluxe_rooms)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by("id")

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

        room.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved:
        last_room.delete()


# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=101).is_reserved)


def update_characters():
    Character.objects.filter(class_name="Mage").update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name="Warrior").update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character, second_character):
    fusion_name = first_character.name + " " + second_character.name
    fusion_level = (first_character.level + second_character.level) //2
    fusion_class = "Fusion"
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ["Mage", "Scout"]:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=fusion_name,
        level=fusion_level,
        class_name=fusion_class,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()


# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)
