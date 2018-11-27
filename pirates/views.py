from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Tesouro
# Create your views here.

class SalvarTesouro:
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(SalvarTesouro, CreateView):
    pass

class AtualizarTesouro(SalvarTesouro, UpdateView):
    pass

class ListarTesouros(View):
    def get(self,request):
        lst_tesouros = Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
        valor_total = 0
        for tesouro in lst_tesouros:
            valor_total += tesouro.valor_total
        return render(request,"lista_tesouros.html",{"lista_tesouros":lst_tesouros,
                                                     "total_geral":valor_total})

class RemoverTesouro(DeleteView):
    model = Tesouro
    success_url = reverse_lazy('lista_tesouros')
