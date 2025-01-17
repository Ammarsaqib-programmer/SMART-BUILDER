class Room:
    def __init__(self, room_type, area, windows, doors):
        self.type = room_type
        self.area = area
        self.windows = windows
        self.doors = doors

    def calculate_cost(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def display_info(self):
        print(f"- {self.type}:")
        print(f"  Area: {self.area} sq. m")
        print(f"  Windows: {self.windows}")
        print(f"  Doors: {self.doors}")
        print(f"  Cost: ${self.calculate_cost():,.2f}")


class LivingRoom(Room):
    def __init__(self, area, windows, doors):
        super().__init__("Living Room", area, windows, doors)

    def calculate_cost(self):
        return self.area * 50 + self.windows * 200 + self.doors * 150


class Kitchen(Room):
    def __init__(self, area, windows, doors):
        super().__init__("Kitchen", area, windows, doors)

    def calculate_cost(self):
        return self.area * 70 + self.windows * 200 + self.doors * 150


class GuestRoom(Room):
    def __init__(self, area, windows, doors):
        super().__init__("Guest Room", area, windows, doors)

    def calculate_cost(self):
        return self.area * 60 + self.windows * 200 + self.doors * 150


class Warehouse:
    def __init__(self):
        self.cement_cost = 10
        self.brick_cost = 0.5
        self.paint_cost = 5

    def estimate_materials(self, area):
        cement = area * 0.1
        bricks = area * 2
        paint = area * 0.05
        print("\nMaterial Estimation:")
        print(f"  Cement: {cement:.2f} bags (${cement * self.cement_cost:.2f})")
        print(f"  Bricks: {bricks:.2f} pieces (${bricks * self.brick_cost:.2f})")
        print(f"  Paint: {paint:.2f} liters (${paint * self.paint_cost:.2f})")


class Construction:
    def __init__(self, construction_type, area):
        self.type = construction_type
        self.area = area
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def display_info(self):
        print(f"\n{self.type} Details:")
        print(f"Total Area: {self.area:.2f} sq. m")
        print(f"Number of Rooms: {len(self.rooms)}")
        for room in self.rooms:
            room.display_info()
        print(f"Total Room Cost: ${self.calculate_total_cost():,.2f}")

    def calculate_total_cost(self):
        return sum(room.calculate_cost() for room in self.rooms)


class House(Construction):
    def __init__(self, area, color_scheme, num_floors, garage_size, has_balcony):
        super().__init__("House", area)
        self.color_scheme = color_scheme
        self.num_floors = num_floors
        self.garage_size = garage_size
        self.has_balcony = has_balcony

    def display_info(self):
        super().display_info()
        print(f"Color Scheme: {self.color_scheme}")
        print(f"Number of Floors: {self.num_floors}")
        print(f"Garage Size: {self.garage_size} cars")
        print(f"Has Balcony: {'Yes' if self.has_balcony else 'No'}")


class Building(Construction):
    def __init__(self, area, num_floors, color_scheme):
        super().__init__("Building", area)
        self.num_floors = num_floors
        self.color_scheme = color_scheme

    def display_info(self):
        super().display_info()
        print(f"Number of Floors: {self.num_floors}")
        print(f"Color Scheme: {self.color_scheme}")


# Utility Functions
def get_valid_input(prompt, input_type, condition=lambda x: True, error_message="Invalid input."):
    while True:
        try:
            value = input_type(input(prompt))
            if condition(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print(error_message)


def main():
    print("Welcome to the Construction Planning System!")
    while True:
        construction_type = get_valid_input(
            "Enter the type of construction (House/Building): ",
            str,
            lambda x: x.lower() in ["house", "building"],
            "Please enter 'House' or 'Building'."
        ).capitalize()

        area = get_valid_input(
            "Enter the total area (in sq. m): ",
            float,
            lambda x: (50 <= x <= 500) if construction_type == "House" else (100 <= x <= 1000),
            "Invalid area. House: 50-500 sq. m, Building: 100-1000 sq. m."
        )

        if construction_type == "House":
            color_scheme = input("Enter the house color scheme: ")
            num_floors = get_valid_input("Enter the number of floors: ", int, lambda x: x > 0, "Floors must be positive.")
            garage_size = get_valid_input("Enter the garage size (in cars): ", int, lambda x: x >= 0, "Garage size cannot be negative.")
            has_balcony = input("Does the house have a balcony? (yes/no): ").strip().lower() == 'yes'
            construction = House(area, color_scheme, num_floors, garage_size, has_balcony)
        else:
            num_floors = get_valid_input("Enter the number of floors: ", int, lambda x: x > 0, "Floors must be positive.")
            color_scheme = input("Enter the building color scheme: ")
            construction = Building(area, num_floors, color_scheme)

        while True:
            print("\nAdding a Room:")
            room_type = get_valid_input(
                "Enter room type (LivingRoom/Kitchen/GuestRoom): ",
                str,
                lambda x: x.lower() in ["livingroom", "kitchen", "guestroom"],
                "Invalid room type."
            ).capitalize()

            room_area = get_valid_input("Enter the room area (in sq. m): ", float, lambda x: x > 0, "Area must be positive.")
            windows = get_valid_input("Enter the number of windows: ", int, lambda x: x >= 0, "Windows cannot be negative.")
            doors = get_valid_input("Enter the number of doors: ", int, lambda x: x >= 0, "Doors cannot be negative.")

            if room_type == "Livingroom":
                room = LivingRoom(room_area, windows, doors)
            elif room_type == "Kitchen":
                room = Kitchen(room_area, windows, doors)
            elif room_type == "Guestroom":
                room = GuestRoom(room_area, windows, doors)
            construction.add_room(room)

            if input("Do you want to add another room? (yes/no): ").strip().lower() != 'yes':
                break

        warehouse = Warehouse()
        warehouse.estimate_materials(construction.area)
        construction.display_info()

        if input("\nIs this plan acceptable? (yes/no): ").strip().lower() == 'yes':
            print("Construction plan finalized!")
            break
        else:
            print("Restarting the planning process...\n")


if __name__ == "__main__":
    main()
