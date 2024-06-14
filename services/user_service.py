from models import Session, User, CardQuantity

class UserService:

    def __init__(self):
        self.session = Session()

    def get_users(self):
        all_user = self.session.query(User).all()
        return [user.name for user in all_user]

    def get_user_id_by_name(self, name):
        user = self.session.query(User).filter_by(name=name).first()
        if user:
            return user.id
        return None

    def get_quantity_of_card(self, user_id, card_id):
        card_quantity = self.session.query(CardQuantity).filter_by(user_id=user_id, card_id=card_id).first()
        if card_quantity:
            return card_quantity.quantity
        else:
            return 0

    def set_user(self, name):
        try:
            new_user = User(name=name)
            self.session.add(new_user)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True

    def update_quantity_by_id(self, card_id, user_id, new_quantity):
        card = self.session.query(CardQuantity).filter_by(card_id=card_id, user_id=user_id).first()
        if card:
            card.quantity = new_quantity
        else:
            new_card_quantity = CardQuantity(card_id=card_id, user_id=user_id, quantity=new_quantity)
            try:
                self.session.add(new_card_quantity)
            except Exception as e:
                self.session.rollback()
                print(f"Error: {e}")
                return False
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            return False
        return True
