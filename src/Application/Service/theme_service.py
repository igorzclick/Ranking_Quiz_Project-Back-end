from src.Infrastructure.Model.theme_model import Theme
from src.Infrastructure.Model.player_model import Player
from src.config.data_base import db

class ThemeService:
    @staticmethod
    def create_theme(theme):
        new_theme = theme.to_dict()
        try:
        
            player = Player.query.filter_by(id=new_theme['created_by']).first()
            if not player:
                return None, "Player not found"

            if Theme.query.filter_by(name=new_theme['name']).first():
                return None, "Theme name already registered"
            
            if 'is_active' not in new_theme:
                new_theme['is_active'] = True
            
            theme = Theme(
                **new_theme
            )

            db.session.add(theme)
            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def get_all_themes():
        try:
            themes = Theme.query.all()        
            return [theme.to_dict() for theme in themes]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_theme_by_id(id):
        try:
            theme = Theme.query.filter_by(id=id).first()        
            return theme.to_dict()
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def get_theme_by_name(name):
        try:
            theme = Theme.query.filter_by(name=name).first()        
            return theme.to_dict()
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def update_theme(theme):
        new_theme = theme.to_dict()

        try:
            theme = Theme.query.filter_by(id=new_theme['id']).first()

            theme_by_name = Theme.query.filter_by(name=new_theme['name']).first()
            if theme_by_name != None and theme_by_name.id != theme.id:
                return None, "Theme name already registered"

            if not theme:
                return None, "Theme not found"

            theme.name = new_theme['name']
            theme.description = new_theme['description']
            theme.is_active = new_theme['is_active']

            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_theme(id):
        try:
            theme = Theme.query.filter_by(id=id).first()

            if not theme:
                return None, "Theme not found"

            db.session.delete(theme)
            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)