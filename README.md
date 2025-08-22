# Discord-Referee

Bot modular para Discord orientado a la gestión de ligas, torneos y equipos, con soporte multilenguaje, paneles interactivos y administración avanzada de servidores.

---

## Características

- **Paneles interactivos**: Embeds, botones y modales configurables desde archivos JSON.
- **Soporte multilenguaje**: Traducciones y textos personalizables en `src/languages/locales/`.
- **Gestión automática de canales y categorías**: Estructura del servidor definida en el idioma.
- **Persistencia en base de datos**: Soporte para MySQL/MongoDB.
- **Consola administrativa**: Control y configuración desde la terminal.
- **Arquitectura extensible**: Añade fácilmente nuevos comandos, paneles y funcionalidades.

---

## Estructura del Proyecto

```
src/
  bot/             # Inicialización del bot y gestión de guilds
  commands/        # Comandos de usuario y administración
  config/          # Configuración y variables de entorno
  console/         # Consola administrativa
  database/        # Abstracción y modelos de base de datos
  factory_cac/     # Fábricas de canales y categorías
  factory_panel/   # Generadores de paneles (embeds, botones, modales)
  languages/       # Archivos de idioma y gestor de traducciones
  server_builder/  # Lógica para construir la estructura del servidor
  utils/           # Utilidades y helpers
```

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Esquirtle/Discord-Referee.git
   cd Discord-Referee
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura el archivo `.env` en `src/config/` con tu token de bot y datos de base de datos.

4. Personaliza los archivos de idioma en `src/languages/locales/` y los paneles en `src/factory_panel/json_panels/` según tus necesidades.

---

## Uso

Ejecuta el bot con:

```bash
python src/bot/main.py
```

El bot cargará los comandos y la estructura del servidor según la configuración del idioma y los paneles definidos.

---

## Personalización

- **Paneles**: Añade o edita archivos JSON en `src/factory_panel/json_panels/` para definir nuevos paneles, botones y modales.
- **Idiomas**: Añade o edita archivos en `src/languages/locales/` para soportar nuevos idiomas o modificar textos.
- **Comandos**: Añade nuevos archivos Python en `src/commands/` para extender la funcionalidad del bot.

---

## Contribución

¡Las contribuciones son bienvenidas! Abre un issue o pull request para sugerir mejoras o reportar errores.

---

## Licencia

MIT

---

**Discord-Referee** es un proyecto en desarrollo. Para dudas o soporte, contacta al autor o abre un issue en el repositorio.