from .models import Order, OrderedItem, Client, Categoric, Type

def cart(request) :
    product_amount_cart = 0
    if request.user.is_authenticated:
        client = request.user.client #? one to one relationship
    else :
        if request.COOKIES.get('id_session') :
            id_session = request.COOKIES.get("id_session")
            client, created = Client.objects.get_or_create(id_session=id_session)
        else : #? if the client enters directly on the cart, whithout generating cookies
            return {"product_amount_cart" : product_amount_cart} #? return initial quantity, which is 0
    order, created = Order.objects.get_or_create(client=client, finished=False) #? will get or create a new order if there is none for the client mentioned above. Will return the order and a boolean that says if it was created or not
    #! How many products are on the user's order
    items_ordered = OrderedItem.objects.filter(order = order) #? gets all the items of the order
    for item in items_ordered:
        product_amount_cart += item.quantity #? adds the quantity of each item as one order can have many items
    return {"product_amount_cart" : product_amount_cart, "items_ordered" : items_ordered}


def category_type(request):
    categories_navbar = Categoric.objects.all()
    categories_with_types = []

    for category in categories_navbar:
        # Obtenha os tipos associados à categoria atual
        types = Type.objects.filter(product__category=category).distinct()
        # Adicione a categoria e seus tipos a uma estrutura de dados
        categories_with_types.append({
            "category": category,
            "types": types
        })

    return {
        "categories_with_types": categories_with_types,
    }

def is_part_of_team(request) :
    team = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Team").exists(): #? if the user is authenticated and the group Team is created (parameters obtained from admin page)
            team = True
    return {"Team" : team}

