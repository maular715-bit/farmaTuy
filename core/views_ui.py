from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, TemplateView
from django.shortcuts import redirect
from django.db.models import Q
from .models import Farmacia, Medicamento, InventarioFarmacia, Tipo, Usuario
from .forms import FarmaciaForm, MedicamentoForm, InventarioForm, TipoForm, UsuarioForm


class FarmaciaListView(ListView):
    model = Farmacia
    template_name = 'farmacia_list.html'
    context_object_name = 'farmacias'


class FarmaciaCreateView(CreateView):
    model = Farmacia
    form_class = FarmaciaForm
    template_name = 'farmacia_form.html'
    success_url = reverse_lazy('farmacia_list')


class FarmaciaUpdateView(UpdateView):
    model = Farmacia
    form_class = FarmaciaForm
    template_name = 'farmacia_form.html'
    success_url = reverse_lazy('farmacia_list')


class FarmaciaDetailView(DetailView):
    model = Farmacia
    template_name = 'farmacia_detail.html'
    context_object_name = 'farmacia'


class FarmaciaDeleteView(View):
    def post(self, request, pk):
        obj = Farmacia.objects.filter(pk=pk).first()
        if obj:
            obj.estatus = False
            obj.save()
        return redirect('farmacia_list')


# Similar views for Medicamento
class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'medicamento_list.html'
    context_object_name = 'medicamentos'

    def get_queryset(self):
        qs = super().get_queryset().filter(estatus=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(medicamento__icontains=q)
        # marca: search in descripcion or disposicion fields
        marca = self.request.GET.get('marca')
        if marca:
            qs = qs.filter(Q(descripcion__icontains=marca) | Q(disposicion__icontains=marca))
        # presentacion: filter by tipo_presentacion id
        presentacion = self.request.GET.get('presentacion')
        if presentacion:
            qs = qs.filter(tipo_presentacion__id=presentacion)
        # farmacia: filter medicamentos available in a farmacia via InventarioFarmacia
        farmacia_id = self.request.GET.get('farmacia')
        if farmacia_id:
            medicamento_ids = InventarioFarmacia.objects.filter(farmacia__id=farmacia_id, estatus=True).values_list('medicamento__id', flat=True)
            qs = qs.filter(id__in=medicamento_ids)
        # sorting
        sort = self.request.GET.get('sort')
        if sort == 'name_asc':
            qs = qs.order_by('medicamento')
        elif sort == 'name_desc':
            qs = qs.order_by('-medicamento')
        elif sort == 'date_asc':
            qs = qs.order_by('fecha_creacion')
        elif sort == 'date_desc':
            qs = qs.order_by('-fecha_creacion')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        ctx['marca'] = self.request.GET.get('marca', '')
        ctx['presentacion'] = self.request.GET.get('presentacion', '')
        ctx['farmacia'] = self.request.GET.get('farmacia', '')
        # provide options for selects
        ctx['presentaciones'] = Tipo.objects.filter(medicamentos_presentacion__isnull=False).distinct()
        ctx['farmacias'] = Farmacia.objects.filter(estatus=True)
        ctx['sort'] = self.request.GET.get('sort', '')
        return ctx

    paginate_by = 10


class MedicamentoCreateView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')


class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')


class MedicamentoDetailView(DetailView):
    model = Medicamento
    template_name = 'medicamento_detail.html'
    context_object_name = 'medicamento'


class MedicamentoDeleteView(View):
    def post(self, request, pk):
        obj = Medicamento.objects.filter(pk=pk).first()
        if obj:
            obj.estatus = False
            obj.save()
        return redirect('medicamento_list')


# Inventario
class InventarioListView(ListView):
    model = InventarioFarmacia
    template_name = 'inventario_list.html'
    context_object_name = 'inventarios'


class InventarioCreateView(CreateView):
    model = InventarioFarmacia
    form_class = InventarioForm
    template_name = 'inventario_form.html'
    success_url = reverse_lazy('inventario_list')


class InventarioUpdateView(UpdateView):
    model = InventarioFarmacia
    form_class = InventarioForm
    template_name = 'inventario_form.html'
    success_url = reverse_lazy('inventario_list')


class InventarioDeleteView(View):
    def post(self, request, pk):
        obj = InventarioFarmacia.objects.filter(pk=pk).first()
        if obj:
            obj.estatus = False
            obj.save()
        return redirect('inventario_list')


# Tipo
class TipoListView(ListView):
    model = Tipo
    template_name = 'tipo_list.html'
    context_object_name = 'tipos'


class TipoCreateView(CreateView):
    model = Tipo
    form_class = TipoForm
    template_name = 'tipo_form.html'
    success_url = reverse_lazy('tipo_list')


class TipoUpdateView(UpdateView):
    model = Tipo
    form_class = TipoForm
    template_name = 'tipo_form.html'
    success_url = reverse_lazy('tipo_list')


class TipoDeleteView(View):
    def post(self, request, pk):
        obj = Tipo.objects.filter(pk=pk).first()
        if obj:
            obj.estatus = False
            obj.save()
        return redirect('tipo_list')


# Usuario (basic UI)
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario_list.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuario_list')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuario_list')


class UsuarioDeleteView(View):
    def post(self, request, pk):
        obj = Usuario.objects.filter(pk=pk).first()
        if obj:
            obj.estatus = False
            obj.save()
        return redirect('usuario_list')


class PublicSearchView(TemplateView):
    template_name = 'public_search.html'

