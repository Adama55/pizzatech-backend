from fastapi import FastAPI

from .routers import router_utilisateurs , router_commandes, router_details_commande, router_pizzas

app = FastAPI(
    title="Pizzas Tech",
    description="Pizzas Tech est une API RESTful conçue"
                " pour gérer les commandes de pizza en ligne. "
                "Elle permet aux utilisateurs de consulter les pizzas "
                "disponibles, de passer des commandes, et de gérer les "
                "détails de chaque commande. L'API offre des fonctionnalités "
                "complètes pour la création, la lecture, la mise à jour et la "
                "suppression des commandes et des pizzas, facilitant ainsi une gestion efficace "
                "et intuitive des opérations liées à la vente de pizzas."
)


app.include_router(router_utilisateurs.router)
app.include_router(router_pizzas.router)
app.include_router(router_commandes.router)
app.include_router(router_details_commande.router)