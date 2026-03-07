class Customer:
    def __init__(self, name: str, customer_id: str, email: str):
        self.name = str(name).strip()
        self.customer_id = str(customer_id).strip()
        self._email = str(email).strip()

    def __str__(self) -> str:
        return f"Имя: {self.name}, email: {self.email}"

    # геттер и сеттер для email
    @property
    def email(self) -> str:
        return self._email
    @email.setter
    def email(self, new_email: str) -> str:
        if not new_email:
            raise ValueError("Email не может быть пустым")
        if '@' not in new_email:
            raise ValueError("Email должен содержать символ '@'")
        self._email = str(new_email).strip()
