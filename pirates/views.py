from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField, Sum
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tesouro
# Create your views here.
class SalvarTesouro:
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(LoginRequiredMixin, SalvarTesouro, CreateView):
    pass

class AtualizarTesouro(LoginRequiredMixin, SalvarTesouro, UpdateView):
    pass

class ListarTesouros(LoginRequiredMixin, ListView):
    model = Tesouro
    template_name = 'lista_tesouros.html'

    def get_queryset(self):
        return Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('preco')*F('quantidade'),\
                    output_field=DecimalField(max_digits=10, decimal_places=2, blank=True)))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = Tesouro.objects.aggregate(total_geral=Sum(ExpressionWrapper(F('preco')*F('quantidade'),\
                                    output_field=DecimalField(max_digits=10, decimal_places=2, blank=True))))['total_geral']
        return context

class RemoverTesouro(LoginRequiredMixin, DeleteView):
    model = Tesouro
    success_url = reverse_lazy('lista_tesouros')
