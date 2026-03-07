class Customer:
    def __init__(self, name: str, customer_id: str, email: str):
        self.__name = str(name).strip()
        self.customer_id = str(customer_id).strip()
        self.__email = str(email).strip()

    def __str__(self) -> str:
        return f"{self.__name} ({self.customer_id}), email: {self.__email}"
    # геттер
    @property
    def name(self) -> str:
        return self.__name
    # геттер и сеттер для email
    @property
    def email(self) -> str:
        return self.__email
    @email.setter
    def email(self, new_email: str) -> str:
        if not new_email:
            raise ValueError("Email не может быть пустым")
        if '@' not in new_email:
            raise ValueError("Email должен содержать символ '@'")
        self.__email = str(new_email).strip()
