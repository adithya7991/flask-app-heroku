from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    items = db.relationship('ItemModel', lazy='dynamic')
    # db.relationship just gets linked to ItemModel and fetches all records matching stores.id = items.store_id    

    def __init__(self, name):
        self.name = name        

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}
        # If lazy='dynamic' is used, all items obj of this store will be created only when we do self.items.all()
        # If not, then all items obj of this store will be stored in self.items when StoreModel gets created
            # and v can call then as self.items
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()        

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def return_all_stores(cls):
        return list(map(lambda x : x.json(), cls.query.all()))

    

