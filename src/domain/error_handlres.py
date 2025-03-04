from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class ErrorHandler:
    @staticmethod
    def handle_error(exception, model):
        
        if isinstance(exception, ObjectDoesNotExist):
            return {"error": "Invalid data.", "details": str(exception), "status": 404}
        elif isinstance(exception, IntegrityError):
            if type(exception.args) == tuple:
                if 'foreign key constraint' in str(exception.args[0]):
                    return {"error": "Integrity Error.", "details": f"{model} with that id don't exist", "status": 400}
            return {"error": "Integrity error.", "details": f"A {model} with this data already exists or violates integrity constraints.", "status": 400}
        elif isinstance(exception, KeyError):
            return {"error": f"{model} Error", "details": str(exception), "status": 400}
        elif isinstance(exception, ValueError):
            return {"error": "Invalid data.", "details": str(exception), "status": 400}
        else:
            return {"error": "An unexpected error occurred.", "details": str(exception), "status": 500}
