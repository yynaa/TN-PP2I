class Error():
    def __init__(self,message:str,path_to_logfile:str) -> None:
        self.error_message = message
        self.path_to_logfile = path_to_logfile
        
        pass

    def get_message(self):
        return self.error_message

# -------------------------------------------------------------------

path_to_logefile = ""

no_such_login_error = Error("Il n'y a pas de compte avec ce login.",path_to_logefile)
no_such_email_error = Error("Il n'y a pas de compte avec cet email.",path_to_logefile)
already_used_login_error = Error("Il existe déjà un compte avec ce login.",path_to_logefile)
already_used_email_error = Error("Il existe déjà un compte avec cet email.",path_to_logefile)
invalid_password_error = Error("Le login n'est pas valide (ne peut contenir que des chiffres et des lettres).",path_to_logefile)
same_password_as_before_error = Error("Ce nouveau mot de passe est identique au précédent.",path_to_logefile)
wrong_password_error = Error("Le mot de passe est erronné.",path_to_logefile)