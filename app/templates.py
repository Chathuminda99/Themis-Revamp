from fastapi.templating import Jinja2Templates
from app.version import __version__
from app.utils.rich_text import render_rich_text

templates = Jinja2Templates(directory="templates")
templates.env.globals["app_version"] = __version__
templates.env.filters["rich_text"] = render_rich_text
