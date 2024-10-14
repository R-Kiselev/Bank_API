from commons.base_resources import BaseObjectResource
from models.account import Account
from schemas.account import AccountSchema

from flask_restful import Resource, request
from db_settings import db
from commons.pagination import paginate


class AccountsBankResource(Resource):
    schema = AccountSchema()

    def get(self, bank_id=None):
        query = Account.query.filter(Account.bank_id == bank_id)
        return paginate(query, self.schema)


class AccountBankResource(BaseObjectResource):
    model = Account
    schema = AccountSchema()

class AccountsClientResource(Resource):
    schema = AccountSchema()

    def get(self, client_id = None):
        query = Account.query.filter(Account.client_id == client_id)
        return paginate(query, self.schema)
    
    def post(self, client_id = None):
        req = request.json
        req['client_id'] = client_id

        data = self.schema.load(request.json)
        item = Account(**data)

        db.session.add(item)
        db.session.commit()

        return {
            "msg" : "item created",
            "item" : self.schema.dump(item)
        }, 201
    

class AccountClientResource(Resource):
    schema = AccountSchema()

    def get(self, client_id = None, account_id = None):
        account = Account.query.\
            filter(Account.client_id == client_id).\
            filter(Account.id == account_id).first()
        return self.schema.dump(account), 200

    def put(self, client_id = None, account_id = None):
        account = Account.query.\
            filter(Account.client_id == client_id).\
            filter(Account.id == account_id).first()
        
        data = self.schema.load(request.json, partial = True)
        for key, value in data.items():
            setattr(account, key, value)

        db.session.commit()
        return {
            "msg": "item updated",
            "item": self.schema.dump(account)
        }, 200
    
    def delete(self, client_id = None, account_id = None):
        account = Account.query.\
            filter(Account.client_id == client_id).\
            filter(Account.id == account_id).first()
        
        db.session.delete(account)
        db.session.commit()

        return {
            "msg" : "item deleted",
            "item" : self.schema.dump(account)
        }, 204