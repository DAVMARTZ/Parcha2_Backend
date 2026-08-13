from pymongo import ReturnDocument

from companies.mongo import users_collection


def _serialize(document):
    """Convierte un documento de Mongo en un dict apto para JSON.

    Reemplaza el ``_id`` interno por un campo ``id`` legible.
    """
    if document is None:
        return None

    document["id"] = str(document["_id"])
    del document["_id"]
    return document


class UserRepository:
    """Acceso a la colección MongoDB de perfiles de usuario.

    Esta capa es la única que conoce la estructura de los documentos, lo que
    aísla a los servicios de los detalles de persistencia.
    """

    def create(self, document):
        result = users_collection.insert_one(document)
        document["id"] = str(result.inserted_id)
        return document

    def find_by_uid(self, uid):
        return _serialize(users_collection.find_one({"uid": uid}))

    def find_all(self):
        return [_serialize(document) for document in users_collection.find()]

    def update_role(self, uid, role):
        document = users_collection.find_one_and_update(
            {"uid": uid},
            {"$set": {"role": role}},
            return_document=ReturnDocument.AFTER,
        )
        return _serialize(document)
