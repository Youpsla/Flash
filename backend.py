from registration.backends.default import DefaultBackend

class MyRegistrationBackend(DefaultBackend):
    def post_activation_redirect(self, request, user):
        # return your URL here