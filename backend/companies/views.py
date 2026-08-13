from datetime import datetime, timezone
from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from companies.mongo import companies_collection, material_listings_collection

class CompanyViewSet(viewsets.ViewSet):
    # Exige autenticación para acceder a este conjunto de endpoints.
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Obtiene el uid del usuario autenticado desde Firebase.
        uid = request.firebase_user.get("uid")

        # Consulta las empresas registradas por ese usuario.
        companies = list(
            companies_collection.find(
                {"owner_uid": uid},
                {
                    "owner_uid": 1,
                    "name": 1,
                    "nit": 1,
                    "city": 1,
                    "sector": 1,
                    "size": 1,
                    "employes": 1,
                    "created_at": 1,
                },
            )
        )

        # Convierte ObjectId a string para serializar la respuesta en JSON.
        for company in companies:
            company["id"] = str(company["_id"])
            del company["_id"]

        # Retorna la lista de empresas.
        return Response(companies)

    def create(self, request):
        # Obtiene el uid del usuario autenticado.
        uid = request.firebase_user.get("uid")

        # Obtiene los datos enviados por el frontend.
        data = request.data

        # Construye el documento que será almacenado en MongoDB.
        document = {
            "owner_uid": uid,
            "name": data.get("name"),
            "nit": data.get("nit"),
            "city": data.get("city"),
            "sector": data.get("sector"),
            "size": data.get("size"),
            "employes": data.get("employes"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Inserta la empresa y recupera el id generado.
        result = companies_collection.insert_one(document)

        # Retorna el id del registro creado.
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)


class MaterialListingViewSet(viewsets.ViewSet):
    # Exige autenticación para acceder a este conjunto de endpoints.
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Obtiene el uid del usuario autenticado.
        uid = request.firebase_user.get("uid")

        # Busca las empresas que pertenecen a ese usuario.
        companies = list(companies_collection.find({"owner_uid": uid}, {"_id": 1}))

        # Extrae los identificadores de las empresas.
        company_ids = [company["_id"] for company in companies]

        # Busca publicaciones asociadas a esas empresas.
        items = list(material_listings_collection.find({"company_id": {"$in": company_ids}}))

        # Convierte identificadores a string para responder en JSON.
        for item in items:
            item["id"] = str(item["_id"])
            item["company_id"] = str(item["company_id"])
            del item["_id"]

        # Retorna la lista de publicaciones.
        return Response(items)

    def create(self, request):
        # Obtiene los datos enviados por el cliente.
        data = request.data

        # Construye el documento de publicación.
        document = {
            "company_id": ObjectId(data.get("company_id")),
            "material_type": data.get("material_type"),
            "quantity": float(data.get("quantity")),
            "unit": data.get("unit", "kg"),
            "location": data.get("location"),
            "price": data.get("price"),
            "material-status": data.get("status_Material"),
            "status": data.get("status", "available"),
            "published_by": request.firebase_user.get("uid"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Inserta la publicación en la colección.
        result = material_listings_collection.insert_one(document)

        # Retorna el id del documento creado.
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    # Endpoint mínimo para verificar que el backend está respondiendo.
    return Response({"status": "ok"})