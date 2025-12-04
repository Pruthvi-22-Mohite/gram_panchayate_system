from django.utils.deprecation import MiddlewareMixin
from django.utils import translation
from django.conf import settings

class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware to handle language switching based on user preference
    """
    
    def process_request(self, request):
        # Get language from session
        language = request.session.get('django_language')
        
        # If not in session, try to get from cookie
        if not language:
            language = request.COOKIES.get('django_language')
        
        # If still not found, use default language
        if not language or language not in [lang[0] for lang in settings.LANGUAGES]:
            language = settings.LANGUAGE_CODE.split('-')[0]  # Extract 'en' from 'en-us'
        
        # Activate the language
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()