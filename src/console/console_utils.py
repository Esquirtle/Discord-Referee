def mostrar_servidores(connected_guilds):
    if not connected_guilds:
        print("No hay servidores conectados.")
        return
    print("Servidores conectados:")
    for idx, guild in enumerate(connected_guilds):
        if hasattr(guild, 'name'):
            print(f"[{idx}] {guild.name} (ID: {guild.id})")
        else:
            print(f"[{idx}] {guild}")

def seleccionar_servidor(connected_guilds):
    mostrar_servidores(connected_guilds)
    if not connected_guilds:
        return None
    while True:
        seleccion = input("Selecciona el número del servidor: ").strip()
        if seleccion.isdigit():
            idx = int(seleccion)
            if 0 <= idx < len(connected_guilds):
                return connected_guilds[idx]
        print("Selección inválida. Intenta de nuevo.")
