from fastapi import FastAPI

from .routers import router_utilisateurs , router_commandes, router_details_commande, router_pizzas

app = FastAPI(
    title="Pizzas tech",
)

app.include_router(router_utilisateurs.router)
app.include_router(router_pizzas.router)
app.include_router(router_commandes.router)
app.include_router(router_details_commande.router)