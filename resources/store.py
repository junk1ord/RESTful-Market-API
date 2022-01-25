from flask_restful import Resource, reqparse
from models.storeModel import StoreModel


class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {"message": f"No store found named {name}."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store already found named {name}. Use another name."}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": f"An error occurred while creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
