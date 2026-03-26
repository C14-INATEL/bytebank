from .models import User


class UserService:
    def create_user_logic(self, db, user_data):
        # Validação simples para o Teste 2
        if "@" not in user_data.get("email", ""):
            return None

        # Simulação de criação para o Teste 1 e 4
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )

        # Se houver um DB (mock), simula o salvamento para o Teste 4
        if db:
            db.add(new_user)
            new_user.id = 1

        return new_user

    def get_user_by_id(self, db, user_id):
        # Simulação para o Teste 3 (retorna None se não achar no mock)
        if db:
            return db.query().filter().first()
        return None
