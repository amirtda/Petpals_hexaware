class InvalidPetAgeException(Exception):
    def _init_(self, message="Pet age must be a positive integer."):
        super()._init_(message)


class NullReferenceException(Exception):
    def _init_(self, message="Pet property is missing (null reference)."):
        super()._init_(message)


class InsufficientFundsException(Exception):
    def _init_(self, message="Minimum donation amount is 10."):
        super()._init_(message)


class FileHandlingException(Exception):
    def _init_(self, message="Error handling the file."):
        super()._init_(message)


class AdoptionException(Exception):
    def _init_(self, message="Adoption error occurred."):
        super()._init_(message)

# ===================== Entity Classes =====================


class Pet:
    def _init_(self, name, age, breed):
        if age <= 0:
            raise InvalidPetAgeException()
        self.name = name
        self.age = age
        self.breed = breed

    def _str_(self):
        return f"Pet(Name={self.name}, Age={self.age}, Breed={self.breed})"


class Dog(Pet):
    def _init_(self, name, age, breed, dog_breed):
        super()._init_(name, age, breed)
        self.dog_breed = dog_breed


class Cat(Pet):
    def _init_(self, name, age, breed, cat_color):
        super()._init_(name, age, breed)
        self.cat_color = cat_color


class PetShelter:
    def _init_(self):
        self.available_pets = []

    def add_pet(self, pet):
        self.available_pets.append(pet)

    def remove_pet(self, pet):
        try:
            self.available_pets.remove(pet)
        except ValueError:
            raise AdoptionException("Pet not found in shelter.")

    def list_available_pets(self):
        for pet in self.available_pets:
            try:
                if not pet.name or pet.age is None:
                    raise NullReferenceException()
                print(pet)
            except NullReferenceException as e:
                print(e)

# ===================== Abstract Donation =====================


class Donation(ABC):
    def _init_(self, donor_name, amount):
        if amount < 10:
            raise InsufficientFundsException()
        self.donor_name = donor_name
        self.amount = amount

    @abstractmethod
    def record_donation(self):
        pass


class CashDonation(Donation):
    def _init_(self, donor_name, amount, donation_date):
        super()._init_(donor_name, amount)
        self.donation_date = donation_date

    def record_donation(self):
        query = """
        INSERT INTO donations (donor_name, amount, donation_date) VALUES (?, ?, ?)
        """
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            query, (self.donor_name, self.amount, self.donation_date))
        conn.commit()
        conn.close()


class ItemDonation(Donation):
    def _init_(self, donor_name, amount, item_type):
        super()._init_(donor_name, amount)
        self.item_type = item_type

    def record_donation(self):
        query = """
        INSERT INTO donations (donor_name, amount, item_type) VALUES (?, ?, ?)
        """
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (self.donor_name, self.amount, self.item_type))
        conn.commit()
        conn.close()

# ===================== Adoption Interface =====================


class IAdoptable(ABC):
    @abstractmethod
    def adopt(self):
        pass


class AdoptionEvent(IAdoptable):
    def _init_(self):
        self.participants = []

    def host_event(self):
        print("Hosting an adoption event...")
        for p in self.participants:
            print(f"Participant: {p}")

    def register_participant(self, name):
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO participants (event_id, participant_name) VALUES (?, ?)", (1, name))
        conn.commit()
        conn.close()
        self.participants.append(name)

    def adopt(self):
        print("Pet adopted!")

# ===================== Database Utilities =====================


class DBConnUtil:
    @staticmethod
    def get_connection():
        return pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-9P1BUGLI\\SQLEXPRESS;"
            "DATABASE=PetPalsDB;"
            "Trusted_Connection=yes;"
        )

# ===================== Main Application =====================


def main():
    shelter = PetShelter()
    event = AdoptionEvent()

    while True:
        print("\n--- PetPals Menu ---")
        print("1. Add Pet")
        print("2. List Pets")
        print("3. Record Donation")
        print("4. View Pets in DB")
        print("5. Register for Event")
        print("6. Host Event")
        print("0. Exit")

        choice = input("Choose: ")
        try:
            if choice == "1":
                name = input("Pet Name: ")
                age = int(input("Pet Age: "))
                breed = input("Pet Breed: ")
                pet_type = input("Type (dog/cat): ").lower()
                if pet_type == "dog":
                    dog_breed = input("Dog Breed: ")
                    pet = Dog(name, age, breed, dog_breed)
                else:
                    cat_color = input("Cat Color: ")
                    pet = Cat(name, age, breed, cat_color)
                shelter.add_pet(pet)
                print("Pet added.")
            elif choice == "2":
                shelter.list_available_pets()
            elif choice == "3":
                donor = input("Donor Name: ")
                amount = float(input("Amount: "))
                dtype = input("Type (cash/item): ").lower()
                if dtype == "cash":
                    date = datetime.datetime.now()
                    donation = CashDonation(donor, amount, date)
                else:
                    item = input("Item Type: ")
                    donation = ItemDonation(donor, amount, item)
                donation.record_donation()
                print("Donation recorded.")
            elif choice == "4":
                conn = DBConnUtil.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pets")
                for row in cursor.fetchall():
                    print(row)
                conn.close()
            elif choice == "5":
                name = input("Your name: ")
                event.register_participant(name)
            elif choice == "6":
                event.host_event()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")


if _name_ == "_main_":
    main()
