from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from control_estudios.forms import CursoFormulario
from control_estudios.models import Estudiante, Curso


def listar_estudiantes(request):
    contexto = {
        "profesor": "Lautaro",
        "estudiantes": Estudiante.objects.all(),
    }
    http_response = render(
        request=request,
        template_name='control_estudios/lista_estudiantes.html',
        context=contexto,
    )
    return http_response


def listar_cursos(request):
    # Data de pruebas, más adelante la llenaremos con nuestros cursos de verdad
    contexto = {
        "cursos": Curso.objects.all(),
    }
    http_response = render(
        request=request,
        template_name='control_estudios/lista_cursos.html',
        context=contexto,
    )
    return http_response


def crear_curso_version_1(request):
    if request.method == "POST":
        # Guardado de datos
        data = request.POST  # request.POST es un diccionario

        # creo un curso en memoria RAM
        curso = Curso(nombre=data['nombre'], comision=data['comision'])

        # .save lo guarda en la base de datos
        curso.save()

        # Redirecciono al usuario a la lista de cursos
        url_exitosa = reverse('lista_cursos')
        return redirect(url_exitosa)
    else:  # GET
        # Descargar formulario inicial
        http_response = render(
            request=request,
            template_name='control_estudios/formulario_curso_a_mano.html',
        )
        return http_response


def crear_curso(request):
    if request.method == "POST":
        # Guardado de datos
        # Creo un objeto formulario con la data que envio el usuario
        formulario = CursoFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data  # es un diccionario
            nombre = data["nombre"]
            comision = data["comision"]
            # creo un curso en memoria RAM
            curso = Curso(nombre=nombre, comision=comision)
            # Lo guardan en la Base de datos
            curso.save()

            # Redirecciono al usuario a la lista de cursos
            url_exitosa = reverse('lista_cursos')  # estudios/cursos/
            return redirect(url_exitosa)
    else:  # GET
        # Descargar formulario inicial
        formulario = CursoFormulario()
    http_response = render(
        request=request,
        template_name='control_estudios/formulario_curso.html',
        context={'formulario': formulario}
    )
    return http_response


def buscar_cursos(request):
    if request.method == "POST":
        data = request.POST
        busqueda = data["busqueda"]
        # Filtro simple
        # cursos = Curso.objects.filter(comision__contains=busqueda)
        # Ejemplo filtro avanzado
        cursos = Curso.objects.filter(
            Q(nombre__icontains=busqueda) | Q(comision__contains=busqueda)
        )

        contexto = {
            "cursos": cursos,
        }
        http_response = render(
            request=request,
            template_name='control_estudios/lista_cursos.html',
            context=contexto,
        )
        return http_response
