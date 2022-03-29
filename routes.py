from controllers import RegisterControllers,LoginControllers, CrearProductoControllers, ProductosControllers

routes = {
"register": "/registeruser", "register_controllers": RegisterControllers.as_view("register_api"),
"login": "/login", "login_controllers": LoginControllers.as_view("login_api"),
"crearpructo": "/crearpructo", "CrearProductoControllers": CrearProductoControllers.as_view("crearproducto_api"),
"productos": "/productos", "productos_controllers": ProductosControllers.as_view("productos_api")
}