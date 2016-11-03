from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from app.forms import *
from app.models import *

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')


class EmailView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    # Url que vai dizer para onde o usuário vai ser redirecionado caso ele não esteja logado
    login_url = reverse_lazy('login')
    # Formulário que vai renderizado no template
    form_class = EmailForm
    # Url que vai dizer para onde o usuário vai ser redirecinado caso o formulário seja enviado com sucesso
    success_url = reverse_lazy('duvidas')
    # Mensagem que vai ser incluido no context dentro da variável 'messages' que é uma lista 
    success_message = "Mensagem enviada com sucesso."
    # Aponta o template dessa view
    template_name = "caminho_para_template/template.html"

# Não precisa mudar nada nessa função, só copiar e colar
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, email_list, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, email_list)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()

    def form_valid(self, form):
        to_email_list = []
        for recebedor_do_email in ModelComOsRecebedoresDoEmail.objects.all():
            to_email_list.append(recebedor_do_email.email)
        context_email = {
            'assunto': form.cleaned_data['assunto'],
            'conteudo': form.cleaned_data['conteudo'],
        }
        subject_template_name = "email/assunto.txt"
        email_template_name = "email/conteudo.txt"
        html_email_template_name = "email/conteudo.html"
        from_email = DEFAULT_FROM_EMAIL
        self.send_mail(
            subject_template_name, 
            email_template_name,
            context_email, 
            from_email, 
            to_email_list, 
            html_email_template_name,
            )
        return super(EmailView, self).form_valid(form)