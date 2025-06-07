from dao.PetPalsDAOImpl import PetPalsDAOImpl
from entity.Pet import Pet
from entity.Dog import Dog
from entity.Cat import Cat
from entity.CashDonation import CashDonation
from entity.ItemDonation import ItemDonation
from entity.AdoptionEvent import AdoptionEvent  # Assuming it's in entity
import datetime


def main():
    dao = PetPalsDAOImpl()
    event = AdoptionEvent()

    while True:
        print("\n--- PetPals Adoption Platform ---")
        print("1. Add Pet")
        print("2. List All Pets")
        print("3. Make Cash Donation")
        print("4. Make Item Donation")
        print("5. Register for Adoption Event")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter pet name: ")
                age = int(input("Enter pet age: "))
                breed = input("Enter pet breed: ")
                pet_type = input("Is it a Dog or Cat? ").strip().lower()

                if pet_type == 'dog':
                    dog_breed = input("Enter specific dog breed: ")
                    pet = Dog(name, age, breed, dog_breed)
                elif pet_type == 'cat':
                    cat_color = input("Enter cat color: ")
                    pet = Cat(name, age, breed, cat_color)
                else:
                    print("Invalid pet type.")
                    continue

                dao.add_pet(pet)
                print("Pet added successfully.")

            elif choice == '2':
                pets = dao.get_all_pets()
                if pets:
                    for pet in pets:
                        print(pet)
                else:
                    print("No pets available.")

            elif choice == '3':
                donor_name = input("Enter your name: ")
                amount = float(input("Enter donation amount: "))
                donation_date = datetime.datetime.now()
                donation = CashDonation(donor_name, amount, donation_date)
                dao.record_cash_donation(donation)
                print("Cash donation recorded successfully.")

            elif choice == '4':
                donor_name = input("Enter your name: ")
                amount = float(
                    input("Enter estimated value of item donation: "))
                item_type = input("Enter item type (e.g., food, toys): ")
                donation = ItemDonation(donor_name, amount, item_type)
                dao.record_item_donation(donation)
                print("Item donation recorded successfully.")

            elif choice == '5':
                participant_name = input("Enter your name: ")
                event.register_participant(participant_name)
                print("Registered for the event.")

            elif choice == '0':
                print("Exiting PetPals... Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
