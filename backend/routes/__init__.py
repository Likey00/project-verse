from .user import ns as user_ns
from .project import ns as project_ns
from .article import ns as article_ns
from extensions import api


api.add_namespace(user_ns)
api.add_namespace(project_ns)
api.add_namespace(article_ns)