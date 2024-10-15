from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product

import requests

from django.shortcuts import render

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    
class ProductCreateView(CreateView):
    model = Product
    fields = ['nome', 'descricao', 'quantidade', 'preco']
    template_name = 'product_form.html'
    success_url = reverse_lazy('product-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        product = self.object
        
        data = {
            'product_id': product.id,
            'nome': product.nome,
            'quantidade': product.quantidade,
            'preco': str(product.preco),
        }
        
        makeWebhookUrl = 'https://hook.us2.make.com/dkjuu0425bj2r0x8hdqrdy5pwychwsor'
        
        try:
            webhook_response = requests.post(makeWebhookUrl, json=data)
            if webhook_response.status_code == 200:
                print("Deu bom")
            else:
                print("Deu merda")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar webhook: {e}")
            
        return HttpResponseRedirect(self.success_url)
    
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['nome', 'descricao', 'quantidade', 'preco']
    template_name = 'product_form.html'
    success_url = reverse_lazy('product-list')
    
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')