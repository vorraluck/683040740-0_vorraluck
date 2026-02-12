if __name__ == "__main__":
    van = DeliveryVan("Toyota", "HiAce", 2022, 4, "AB-1234", 1000)
    van.begin_service()

    trailer = Trailer("TR-999", 2000, 4)
    trailer.load_cargo(800)
    print("Weight per axle:", trailer.get_weight_per_axle())
