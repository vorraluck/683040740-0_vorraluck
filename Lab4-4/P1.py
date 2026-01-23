from room import Bedroom, Kitchen

def main():
    # Test Bedroom
    bedroom = Bedroom(length=12, width=10, bed_size=5)
    print(bedroom.describe_room())
    print("Bedroom area:", bedroom.calculate_area(), "sq ft")
    print("Bed size:", bedroom.bed_size, "ft")
    print("Recommended lighting:",
          bedroom.get_recommended_lighting(), "lumens/sq ft")
    print()

    # Test Kitchen with island
    kitchen1 = Kitchen(length=15, width=12, has_island=True)
    print(kitchen1.describe_room())
    print("Kitchen area:", kitchen1.calculate_area(), "sq ft")
    island, wall = kitchen1.calculate_counter_space()
    print("Island counter area:", island, "sq ft")
    print("Wall counter area:", wall, "sq ft")
    print("Recommended lighting:",
          kitchen1.get_recommended_lighting(), "lumens/sq ft")
    print()

    # Test Kitchen without island
    kitchen2 = Kitchen(length=15, width=12, has_island=False)
    print(kitchen2.describe_room())
    island, wall = kitchen2.calculate_counter_space()
    print("Island counter area:", island, "sq ft")
    print("Wall counter area:", wall, "sq ft")

if __name__ == "__main__":
    main()
    print(Kitchen.calculate_counter_space.__doc__)