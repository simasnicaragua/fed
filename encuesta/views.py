# -*- coding: UTF-8 -*-
from decorators import session_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from forms import *
from models import *

def get_orgs(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []
    proyects = Proyecto.objects.filter(tipo__in=lista)
    for p in proyects:
        results.append(p.organizacion.id)
    orgs = Organizacion.objects.filter(id__in=list(set(results))).order_by('nombre_corto').values('id', 'nombre_corto')

    return HttpResponse(simplejson.dumps(list(orgs)), mimetype='application/json')

def proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=int(id))
    return render_to_response('proyecto.html', RequestContext(request, locals()))

def organizacion(request, id):
    organizacion = get_object_or_404(Organizacion, pk=int(id))
    return render_to_response('organizacion.html', RequestContext(request, locals()))

def _queryset_filtrado(request, resultado):
    '''metodo para obtener el queryset de encuesta
    segun los filtros del formulario que son pasados
    por la variable de sesion'''    
    return Encuesta.objects.filter(organizacion__in=request.session['organizacion'], proyecto__tipo__in=request.session['tipo'], periodo__in=request.session['periodo'], anio=request.session['anio'])

def _tiene_datos(request):    
    lista = []    
    encuestas = Encuesta.objects.filter(organizacion__in=request.session['organizacion'], proyecto__tipo__in=request.session['tipo'], periodo__in=request.session['periodo'], anio=request.session['anio'])
    for e in encuestas:
        for r in e.resultadotrabajado_set.all():
            lista.append(r.resultado.pk)

    return list(set(lista))

@login_required
def index(request):
    informes = Encuesta.objects.all().order_by('-id')[:5]
    return render_to_response('index.html', RequestContext(request, locals()))

@login_required
def lista(request, id=None):
    resultados = Resultado.objects.all()
    dicc = {}
    dicc2 = {}
    org_list = []    
    depas = []
    flag = False
    if id != None:
        selecto = int(id)
        try:
            r = resultados.get(pk=id)
            flag = True
            for rt in r.resultadotrabajado_set.all():
                org_list.append(rt.encuesta.organizacion)

            for org in org_list:
                depas = []
                rts = ResultadoTrabajado.objects.filter(encuesta__organizacion=org, resultado=r)
                for resultado in rts:
                    for m in resultado.municipio.all():
                        depas.append(m.departamento)
                dicc[org] = list(set(depas))

            departamentos = Departamento.objects.all()
            for depa in departamentos:
                orgs = []
                rts = ResultadoTrabajado.objects.filter(municipio__in=depa.municipio_set.all(), resultado=r)
                for rt in rts:
                    orgs.append(rt.encuesta.organizacion)
                dicc2[depa] = list(set(orgs))
        except:
            pass
    return render_to_response('fed/lista.html', RequestContext(request, locals()))

@login_required(redirect_field_name='next')
def influencia(request):
    if request.is_ajax():
        form = InfluenciaForm(request.POST)
        if form.is_valid():
            lista = []
            dicc = {}
            resultados = []
            bandera = 1            
            encuestas = Encuesta.objects.filter(organizacion__in=form.cleaned_data['organizacion'], proyecto__tipo__in=form.cleaned_data['tipo'], periodo__in=form.cleaned_data['periodo'], anio=form.cleaned_data['anio'])
            for encuesta in encuestas:
                for resultado in encuesta.resultadotrabajado_set.filter(resultado__in=form.cleaned_data['resultado']):
                    for muni in resultado.municipio.all():
                        lista.append(muni)
            munis = set(lista)
            for municipio in munis:
                #consultar los proyectos de estos municipios
                rts = municipio.resultadotrabajado_set.filter(resultado__in=form.cleaned_data['resultado'])
                #rts = ResultadoTrabajado.objects.filter(resultado__in=form.cleaned_data['resultado'], municipio=municipio)
                proys = []
                for r in rts:
                    if r.encuesta.organizacion in form.cleaned_data['organizacion']:
                        proys.append(r.encuesta.proyecto.pk)
                proyectos = Proyecto.objects.filter(id__in=proys, tipo__in=form.cleaned_data['tipo']).values('id', 'nombre', 'organizacion__nombre_corto')

                dicc = {
                    'punto': (float(municipio.latitud), float(municipio.longitud)),
                    'municipio': municipio.nombre,
                    'proyectos': list(proyectos)
                }
                resultados.append(dicc)
            return HttpResponse(simplejson.dumps(resultados), mimetype='application/json')
    else:
        form = InfluenciaForm()        
        bandera = 0
        return render_to_response('fed/influencia.html', RequestContext(request, locals()))

    return render_to_response('fed/influencia.html', RequestContext(request, locals()))

def indicadores(request):
    metas = Meta.objects.all()
    if request.method == 'POST':
        form = IndicadoresForm(request.POST)
        if form.is_valid():
            bandera = 1
            request.session['tipo'] = form.cleaned_data['tipo']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            orgs_aux = form.cleaned_data['organizacion']
            #request.session['municipio'] = form.cleaned_data['municipio']
            request.session['periodo'] = form.cleaned_data['periodo']
            request.session['anio'] = form.cleaned_data['anio']
            request.session['activo'] = True
            
            #dato de session para llenar los datos seleccionados en el form
            request.session['todo'] = request.POST
            resultados = Resultado.objects.all()
            datos = _tiene_datos(request)
    else:        
        q = request.GET.get('q', '')
        if q:
            bandera = 1
            resultados = Resultado.objects.all()
            datos = _tiene_datos(request)
            form = IndicadoresForm(request.session['todo'])
        else:
            form = IndicadoresForm()
            bandera = 0
    return render_to_response('fed/indicadores.html', RequestContext(request, locals()))

def resultado1(request):
    bandera = 11;
    resultado = Resultado.objects.get(pk=1)
    return render_to_response('fed/res/resultado1.html', RequestContext(request, locals()))


def meta(request, slug):    
    meta = get_object_or_404(Meta, slug=slug)
    metas = Meta.objects.all()
    acciones = []
    tabla = {}
    informe = InformeObjetivo3.objects.filter(anio=request.session['anio'], periodo__in=request.session['periodo'])
    datos = DatoInformeOb3.objects.filter(informe__in=informe, meta=meta)
    for d in datos:
        acciones.append(d.tipo_accion)
    axns = list(set(acciones))
    for a in axns:
        orgs = []
        tabla[a] = {}
        dato = datos.filter(tipo_accion=a)
        cantidad = dato.count()
        tabla[a]['cantidad'] = cantidad
        sumas = dato.aggregate(hombres_sum=Sum('hombres'), mujeres_sum=Sum('mujeres'))
        tabla[a]['hombres'] = sumas['hombres_sum']
        tabla[a]['mujeres'] = sumas['mujeres_sum']
        for d in dato:
            for o in d.organizacion.all():
                orgs.append(o)
        organizaciones = list(set(orgs))
        tabla[a]['orgs'] = organizaciones

    #para graficos
    try:
        objeto = Meta.objects.get(pk=3)
        if meta == objeto:
            centinel = True
            ORGS = request.session['organizacion']
            si_hay = ORGS.filter(sistema=CHOICE1[0][0]).count()
            hay_pero_no = ORGS.filter(sistema=CHOICE1[1][0]).count()
            no_hay = ORGS.filter(sistema=CHOICE1[2][0]).count()

            total = si_hay + hay_pero_no + no_hay
            val1 = get_prom(total, si_hay)
            val2 = get_prom(total, hay_pero_no)
            val3 = get_prom(total, no_hay)
        
            si_hay_plan = ORGS.filter(plan=CHOICE2[0][0]).count()
            no_utiliza = ORGS.filter(plan=CHOICE2[1][0]).count()
            no_hay_plan = ORGS.filter(plan=CHOICE2[2][0]).count()

            total2 = si_hay_plan + no_utiliza + no_hay_plan
            val4 = get_prom(total2, si_hay_plan)
            val5 = get_prom(total2, no_utiliza)
            val6 = get_prom(total2, no_hay_plan)

            ninguna = ORGS.filter(organizaciones=CHOICE3[0][0]).count()
            en_proceso = ORGS.filter(organizaciones=CHOICE3[1][0]).count()
            logrado = ORGS.filter(organizaciones=CHOICE3[2][0]).count()

            total3 = ninguna + en_proceso + logrado
            val7 = get_prom(total3, ninguna)
            val8 = get_prom(total3, en_proceso)
            val9 = get_prom(total3, logrado)
        else:
            centinel = False
    except:
        pass

    return render_to_response('fed/meta.html', RequestContext(request, locals()))

#vistas para indicadores, no hay forma de volverlos dinamicos
@session_required
def indicador111(request):
    resultado = Resultado.objects.get(pk=1)
    tabla = {}
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)
    for opcion in CHOICE_MEDIO:
        query = AccionEfectuadaMedio.objects.filter(encuesta__in=a, accion=opcion[0])
        cantidad_sum = query.aggregate(cantidad_sum=Sum('cantidad'))['cantidad_sum']
        viol_part_sum = query.aggregate(viol_part_sum=Sum('viol_part'))['viol_part_sum']
        ssr_sum = query.aggregate(ssr_sum=Sum('ssr'))['ssr_sum']
        ssr_part_sum = query.aggregate(ssr_part_sum=Sum('ssr_part'))['ssr_part_sum']
        vih_sida_sum = query.aggregate(vih_sida_sum=Sum('vih_sida'))['vih_sida_sum']
        vih_part_sum = query.aggregate(vih_part_sum=Sum('vih_sida_part'))['vih_part_sum']
        masculinidad_sum = query.aggregate(masculinidad_sum=Sum('masculinidad'))['masculinidad_sum']
        masc_part_sum = query.aggregate(masc_part_sum=Sum('masc_part'))['masc_part_sum']
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
        div_sexual_part_sum = query.aggregate(div_sexual_part_sum=Sum('div_sexual_part'))['div_sexual_part_sum']
        equidad_sum = query.aggregate(equidad_sum=Sum('equidad'))['equidad_sum']
        participantes_sum = query.aggregate(participantes_sum=Sum('participantes'))['participantes_sum']
        tabla[opcion[1]] = {
            'cantidad':cantidad_sum,
            'viol_part': viol_part_sum,
            'ssr': ssr_sum,
            'ssr_part': ssr_part_sum,
            'vih_sida': vih_sida_sum,
            'vih_part': vih_part_sum,
            'masculinidad': masculinidad_sum,
            'masc_part': masc_part_sum,
            'div_sexual': div_sexual_sum,
            'div_sexual_part': div_sexual_part_sum,
            'equidad': equidad_sum,
            'participantes': participantes_sum
            }


    for opcion in CHOICE_REGION:
        query = AccionEfectuadaRegion.objects.filter(encuesta__in=a, accion=opcion[0])
        cantidad_sum = query.aggregate(cantidad_sum=Sum('cantidad'))['cantidad_sum']
        viol_part_sum = query.aggregate(viol_part_sum=Sum('viol_part'))['viol_part_sum']
        ssr_sum = query.aggregate(ssr_sum=Sum('ssr'))['ssr_sum']
        ssr_part_sum = query.aggregate(ssr_part_sum=Sum('ssr_part'))['ssr_part_sum']
        vih_sida_sum = query.aggregate(vih_sida_sum=Sum('vih_sida'))['vih_sida_sum']
        vih_part_sum = query.aggregate(vih_part_sum=Sum('vih_sida_part'))['vih_part_sum']
        masculinidad_sum = query.aggregate(masculinidad_sum=Sum('masculinidad'))['masculinidad_sum']
        masc_part_sum = query.aggregate(masc_part_sum=Sum('masc_part'))['masc_part_sum']
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
        div_sexual_part_sum = query.aggregate(div_sexual_part_sum=Sum('div_sexual_part'))['div_sexual_part_sum']
        equidad_sum = query.aggregate(equidad_sum=Sum('equidad'))['equidad_sum']
        participantes_sum = query.aggregate(participantes_sum=Sum('participantes'))['participantes_sum']

        tabla2[opcion[1]] = {
            'cantidad':cantidad_sum,
            'viol_part': viol_part_sum,
            'ssr': ssr_sum,
            'ssr_part': ssr_part_sum,
            'vih_sida': vih_sida_sum,
            'vih_part': vih_part_sum,
            'masculinidad': masculinidad_sum,
            'masc_part': masc_part_sum,
            'div_sexual': div_sexual_sum,
            'div_sexual_part': div_sexual_part_sum,
            'equidad': equidad_sum,
            'participantes': participantes_sum
            }

    for opcion in CHOICE_DOCS:
        query = AccionEfectuadaDocumento.objects.filter(encuesta__in=a, accion=opcion[0])
        cantidad_sum = query.aggregate(cantidad_sum=Sum('cantidad'))['cantidad_sum']
        viol_aprob_sum = query.aggregate(viol_aprob_sum=Sum('viol_aprob'))['viol_aprob_sum']
        ssr_sum = query.aggregate(ssr_sum=Sum('ssr'))['ssr_sum']
        ssr_aprob_sum = query.aggregate(ssr_aprob_sum=Sum('ssr_aprob'))['ssr_aprob_sum']
        vih_sida_sum = query.aggregate(vih_sida_sum=Sum('vih_sida'))['vih_sida_sum']
        vih_aprob_sum = query.aggregate(vih_aprob_sum=Sum('viol_aprob'))['vih_aprob_sum']
        masculinidad_sum = query.aggregate(masculinidad_sum=Sum('masculinidad'))['masculinidad_sum']
        masc_aprob_sum = query.aggregate(masc_aprob_sum=Sum('masc_aprob'))['masc_aprob_sum']
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
        div_aprob_sum = query.aggregate(div_aprob_sum=Sum('div_aprob'))['div_aprob_sum']
        equidad_sum = query.aggregate(equidad_sum=Sum('equidad'))['equidad_sum']
        participantes_sum = query.aggregate(participantes_sum=Sum('participantes'))['participantes_sum']        

        tabla3[opcion[1]] = {
            'cantidad':cantidad_sum,
            'viol_aprob': viol_aprob_sum,
            'ssr': ssr_sum,
            'ssr_aprob': ssr_aprob_sum,
            'vih_sida': vih_sida_sum,
            'vih_aprob': vih_aprob_sum,
            'masculinidad': masculinidad_sum,
            'masc_aprob': masc_aprob_sum,
            'div_sexual': div_sexual_sum,
            'div_sexual_aprob': div_aprob_sum,
            'equidad': equidad_sum,
            'participantes': participantes_sum
            }

    return render_to_response('fed/indicador111.html', RequestContext(request, locals()))

@session_required
def indicador112(request):
    resultado = Resultado.objects.get(pk=1)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in CHOICE_REGION:
        query = ParticipacionComisionDecision.objects.filter(encuesta__in=a, accion=opcion[0])
        instancias_sum = query.aggregate(instancias_sum=Sum('cantidad_instancias'))['instancias_sum']
        acciones_promovidas_sum = query.aggregate(acciones_promovidas_sum=Sum('cantidad_acciones_promovidas'))['acciones_promovidas_sum']
        acciones_efectivas_sum = query.aggregate(acciones_efectivas_sum=Sum('cantidad_acciones_efectivas'))['acciones_efectivas_sum']
        prom = get_prom(acciones_promovidas_sum, acciones_efectivas_sum)

        tabla[opcion[1]] = {
            'instancias':instancias_sum,
            'acciones_promovidas': acciones_promovidas_sum,
            'acciones_efectivas': acciones_efectivas_sum,
            'prom':prom
            }

    return render_to_response('fed/indicador112.html', RequestContext(request, locals()))

#ELIMINADO A SOLICITUD DE FED INDICADOR 113

@session_required
def indicador114(request):
    resultado = Resultado.objects.get(pk=1)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    '''if len(a)==0:
        return HttpResponse('No hay datos', mimetype='text/plain')'''

    for opcion in CHOICE_REGION:
        query = AccionObservatorio.objects.filter(encuesta__in=a, accion=opcion[0])
        observatorio_sum = query.aggregate(observatorio_sum=Sum('cantidad_observatorios'))['observatorio_sum']
        acciones_realizadas_sum = query.aggregate(acciones_realizadas_sum=Sum('cantidad_acciones_realiz'))['acciones_realizadas_sum']
        acciones_web_sum = query.aggregate(acciones_web_sum=Sum('cantidad_acciones_web'))['acciones_web_sum']
        prom = get_prom(acciones_realizadas_sum, acciones_web_sum)

        tabla[opcion[1]] = {
            'observatorio':observatorio_sum,
            'acciones_realizadas': acciones_realizadas_sum,
            'acciones_web': acciones_web_sum,
            'prom':prom
            }

    return render_to_response('fed/indicador114.html', RequestContext(request, locals()))

def resultado2(request):
    bandera = 11;
    resultado = Resultado.objects.get(pk=2)
    return render_to_response('fed/res/resultado1.html', RequestContext(request, locals()))

@session_required
def indicador121(request):
    resultado = Resultado.objects.get(pk=2)
    tabla = {}
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in CHOICE_MEDIO:
        #calculando denuncias realizadas
        query = DenunciaSocialRealizada.objects.filter(encuesta__in=a, accion=opcion[0])        
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('persona_div_sexual'))['div_sexual_sum']
        discapacidad_sum = query.aggregate(discapacidad_sum=Sum('persona_discapacidad'))['discapacidad_sum']
        vih_sum = query.aggregate(vih_sum=Sum('persona_vih'))['vih_sum']
        racial_sum = query.aggregate(racial_sum=Sum('persona_racial'))['racial_sum']
        joven_sum = query.aggregate(joven_sum=Sum('persona_joven'))['joven_sum']

        tabla[opcion[1]] = {
            'sexual':div_sexual_sum,
            'discapacidad': discapacidad_sum,
            'vih': vih_sum,
            'racial': racial_sum,
            'joven':joven_sum
            }

        #TODO ELIMINADO A PETICION DE FED
    return render_to_response('fed/indicador121.html', RequestContext(request, locals()))

@session_required
def indicador122(request):
    resultado = Resultado.objects.get(pk=2)
    tabla = {}
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)

    #ELIMINANDO A PETICION DE FED

    opcion = CHOICE_JURIDICA[0][0]
    query = DenunciaJuridica.objects.filter(encuesta__in=a, accion=opcion)    
    div_sexual_sum = query.aggregate(div_sexual_sum=Sum('persona_div_sexual'))['div_sexual_sum']
    discapacidad_sum = query.aggregate(discapacidad_sum=Sum('persona_discapacidad'))['discapacidad_sum']
    vih_sum = query.aggregate(vih_sum=Sum('persona_vih'))['vih_sum']
    racial_sum = query.aggregate(racial_sum=Sum('persona_racial'))['racial_sum']
    joven_sum = query.aggregate(joven_sum=Sum('persona_joven'))['joven_sum']
    tabla[CHOICE_JURIDICA[0][1]] = {
        'sexual':div_sexual_sum,
        'discapacidad': discapacidad_sum,
        'vih': vih_sum,
        'racial': racial_sum,
        'joven':joven_sum
    }
    opcion2 = CHOICE_JURIDICA[1][0]
    query2 = DenunciaJuridica.objects.filter(encuesta__in=a, accion=opcion2)    
    div_sexual_sum2 = query2.aggregate(div_sexual_sum2=Sum('persona_div_sexual'))['div_sexual_sum2']
    discapacidad_sum2 = query2.aggregate(discapacidad_sum2=Sum('persona_discapacidad'))['discapacidad_sum2']
    vih_sum2 = query2.aggregate(vih_sum2=Sum('persona_vih'))['vih_sum2']
    racial_sum2 = query2.aggregate(racial_sum2=Sum('persona_racial'))['racial_sum2']
    joven_sum2 = query2.aggregate(joven_sum2=Sum('persona_joven'))['joven_sum2']

    tabla[CHOICE_JURIDICA[1][1]] = {
        'sexual':div_sexual_sum2,
        'discapacidad': discapacidad_sum2,
        'vih': vih_sum2,
        'racial': racial_sum2,
        'joven':joven_sum2
    }

    tabla2['Efectividad %'] = {
        'sexual':get_prom(div_sexual_sum, div_sexual_sum2),
        'discapacidad': get_prom(discapacidad_sum, discapacidad_sum2),
        'vih': get_prom(vih_sum, vih_sum2),
        'racial': get_prom(racial_sum, racial_sum2),
        'joven':get_prom(joven_sum, joven_sum2)
    }   
    
    return render_to_response('fed/indicador122.html', RequestContext(request, locals()))

@session_required
def indicador211(request):
    resultado = Resultado.objects.get(pk=3)
    tabla = {}
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS_REFLEXION:
        query = AccionRealizadaReflexion.objects.filter(encuesta__in=a, accion=opcion[0])
        hombres_sum = query.aggregate(hombres_sum=Sum('hombres'))['hombres_sum']
        mujeres_sum = query.aggregate(mujeres_sum=Sum('mujeres'))['mujeres_sum']
        jovenes_sum = query.aggregate(jovenes_sum=Sum('jovenes'))['jovenes_sum']
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
        vih_sum = query.aggregate(vih_sum=Sum('vih'))['vih_sum']
        etnica_sum = query.aggregate(etnica_sum=Sum('etnica'))['etnica_sum']
        discapacidad_sum = query.aggregate(discapacidad_sum=Sum('discapacidad'))['discapacidad_sum']
        global_sum = query.aggregate(global_sum=Sum('total'))['global_sum']        

        tabla[opcion[1]] = {
            'hombres':hombres_sum,
            'mujeres': mujeres_sum,
            'jovenes': jovenes_sum,
            'div_sexual': div_sexual_sum,
            'vih': vih_sum,
            'etnica': etnica_sum,
            'discapacidad': discapacidad_sum,
            'global': global_sum
            }

    for opcion in MEDIOS_REFLEXION:
        query = InvolucramientoPobMeta.objects.filter(encuesta__in=a, accion=opcion[0])
        prev_vio_sum = query.aggregate(prev_vio_sum=Sum('prev_vio'))['prev_vio_sum']
        ssr_sum = query.aggregate(ssr_sum=Sum('ssr'))['ssr_sum']
        vih_sida_sum = query.aggregate(vih_sida_sum=Sum('vih_sida'))['vih_sida_sum']
        masculinidad_sum = query.aggregate(masculinidad_sum=Sum('masculinidad'))['masculinidad_sum']
        div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
        equidad_sum = query.aggregate(equidad_sum=Sum('equidad'))['equidad_sum']
        global_sum = query.aggregate(global_sum=Sum('total'))['global_sum']
        tabla3[opcion[1]] = {
            'prev_vio':prev_vio_sum,
            'ssr': ssr_sum,
            'vih_sida': vih_sida_sum,
            'masculinidad': masculinidad_sum,
            'div_sexual': div_sexual_sum,
            'equidad': equidad_sum,
            'global': global_sum
            }
            
    return render_to_response('fed/indicador211.html', RequestContext(request, locals()))

@session_required
def indicador212(request):
    resultado = Resultado.objects.get(pk=3)    
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)    

    #obteniendo los promedios
    opcion = PERSONAS_REFLEXION[0][0]
    query = AccionRelizadaReflexionPersona.objects.filter(encuesta__in=a, accion=opcion)
    hombres_sum = query.aggregate(hombres_sum=Sum('hombres'))['hombres_sum']
    mujeres_sum = query.aggregate(mujeres_sum=Sum('mujeres'))['mujeres_sum']
    jovenes_sum = query.aggregate(jovenes_sum=Sum('jovenes'))['jovenes_sum']
    div_sexual_sum = query.aggregate(div_sexual_sum=Sum('div_sexual'))['div_sexual_sum']
    vih_sum = query.aggregate(vih_sum=Sum('vih'))['vih_sum']
    etnica_sum = query.aggregate(etnica_sum=Sum('etnica'))['etnica_sum']
    discapacidad_sum = query.aggregate(discapacidad_sum=Sum('discapacidad'))['discapacidad_sum']
    global_sum = query.aggregate(global_sum=Sum('total'))['global_sum']

    tabla2[PERSONAS_REFLEXION[0][1]] = {
        'hombres':hombres_sum,
        'mujeres': mujeres_sum,
        'jovenes': jovenes_sum,
        'div_sexual': div_sexual_sum,
        'vih': vih_sum,
        'etnica': etnica_sum,
        'discapacidad': discapacidad_sum,
        'global': global_sum
    }
    opcion2 = PERSONAS_REFLEXION[1][0]
    query2 = AccionRelizadaReflexionPersona.objects.filter(encuesta__in=a, accion=opcion2)
    hombres_sum2 = query2.aggregate(hombres_sum2=Sum('hombres'))['hombres_sum2']
    mujeres_sum2 = query2.aggregate(mujeres_sum2=Sum('mujeres'))['mujeres_sum2']
    jovenes_sum2 = query2.aggregate(jovenes_sum2=Sum('jovenes'))['jovenes_sum2']
    div_sexual_sum2 = query2.aggregate(div_sexual_sum2=Sum('div_sexual'))['div_sexual_sum2']
    vih_sum2 = query2.aggregate(vih_sum2=Sum('vih'))['vih_sum2']
    etnica_sum2 = query2.aggregate(etnica_sum2=Sum('etnica'))['etnica_sum2']
    discapacidad_sum2 = query2.aggregate(discapacidad_sum2=Sum('discapacidad'))['discapacidad_sum2']
    global_sum2 = query2.aggregate(global_sum2=Sum('total'))['global_sum2']

    tabla2[PERSONAS_REFLEXION[1][1]] = {
        'hombres':hombres_sum2,
        'mujeres': mujeres_sum2,
        'jovenes': jovenes_sum2,
        'div_sexual': div_sexual_sum2,
        'vih': vih_sum2,
        'etnica': etnica_sum2,
        'discapacidad': discapacidad_sum2,
        'global': global_sum2
    }

    tabla3['Efectividad %'] = {
        'hombres':get_prom(hombres_sum, hombres_sum2),
        'mujeres': get_prom(mujeres_sum, mujeres_sum2),
        'jovenes': get_prom(jovenes_sum, jovenes_sum2),
        'div_sexual': get_prom(div_sexual_sum, div_sexual_sum2),
        'vih':get_prom(vih_sum, vih_sum2),
        'etnica':get_prom(etnica_sum, etnica_sum2),
        'discapacidad':get_prom(discapacidad_sum, discapacidad_sum2),
        'global':get_prom(global_sum, global_sum2),
    }

    return render_to_response('fed/indicador212.html', RequestContext(request, locals()))

@session_required
def indicador221(request):
    resultado = Resultado.objects.get(pk=4)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS2:
        query = AccionImpulsadaOrg.objects.filter(encuesta__in=a, accion=opcion[0])
        acciones_emprendidas_sum = query.aggregate(acciones_emprendidas_sum=Sum('acciones_emprendidas'))['acciones_emprendidas_sum']
        #acciones_cambios_actitud_sum = query.aggregate(acciones_cambios_actitud_sum=Sum('acciones_cambios_actitud'))['acciones_cambios_actitud_sum']
        #prom1 = get_prom(acciones_emprendidas_sum, acciones_cambios_actitud_sum)
        acciones_impulsadas_masculinidad_sum = query.aggregate(acciones_impulsadas_masculinidad_sum=Sum('acciones_impulsadas_masculinidad'))['acciones_impulsadas_masculinidad_sum']
        #acciones_cambios_masculinidad_sum = query.aggregate(acciones_cambios_masculinidad_sum=Sum('acciones_cambios_masculinidad'))['acciones_cambios_masculinidad_sum']
        #prom2 = get_prom(acciones_impulsadas_masculinidad_sum, acciones_cambios_masculinidad_sum)

        tabla[opcion[1]] = {
            'acciones_emprendidas':acciones_emprendidas_sum,
            #'acciones_cambios_actitud': acciones_cambios_actitud_sum,
            #'prom1':prom1,
            'acciones_impulsadas_masculinidad':acciones_impulsadas_masculinidad_sum,
            #'acciones_cambios_masculinidad': acciones_cambios_masculinidad_sum,
            #'prom2':prom2
            }

    return render_to_response('fed/indicador221.html', RequestContext(request, locals()))

@session_required
def indicador222(request):
    resultado = Resultado.objects.get(pk=4)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS2:
        query = AccionImpulsadaGrupo.objects.filter(encuesta__in=a, accion=opcion[0])
        acciones_emprendidas_sex_sum = query.aggregate(acciones_emprendidas_sex_sum=Sum('acciones_emprendidas_sex'))['acciones_emprendidas_sex_sum']        
        acciones_emprendidas_discapa_sum = query.aggregate(acciones_emprendidas_discapa_sum=Sum('acciones_emprendidas_discapa'))['acciones_emprendidas_discapa_sum']        

        tabla[opcion[1]] = {
            'acciones_emprendidas':acciones_emprendidas_sex_sum, 
            'acciones_impulsadas_masculinidad':acciones_emprendidas_discapa_sum, 
            }

    return render_to_response('fed/indicador222.html', RequestContext(request, locals()))

@session_required
def indicador223(request):
    resultado = Resultado.objects.get(pk=4)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS2:
        query = AccionImpulsadaGrupo.objects.filter(encuesta__in=a, accion=opcion[0])
        acciones_emprendidas_etnia_sum = query.aggregate(acciones_emprendidas_etnia_sum=Sum('acciones_emprendidas_etnia'))['acciones_emprendidas_etnia_sum']        
        acciones_emprendidas_jovenes_sum = query.aggregate(acciones_emprendidas_jovenes_sum=Sum('acciones_emprendidas_jovenes'))['acciones_emprendidas_jovenes_sum']
        
        tabla[opcion[1]] = {
            'acciones_emprendidas_etnia':acciones_emprendidas_etnia_sum, 
            'acciones_impulsadas_jovenes':acciones_emprendidas_jovenes_sum, 
            }

    return render_to_response('fed/indicador223.html', RequestContext(request, locals()))


@session_required
def indicador230(request):
    tabla = {}
    resultado = Resultado.objects.get(pk=5)
    a = _queryset_filtrado(request, resultado)   

    for opcion in ATENCION_SALUD:
        query2 = AtencionSalud.objects.filter(encuesta__in=a, accion=opcion[0])
        hombres_sum2 = query2.aggregate(hombres_sum2=Sum('hombres'))['hombres_sum2']
        mujeres_sum2 = query2.aggregate(mujeres_sum2=Sum('mujeres'))['mujeres_sum2']
        jovenes_sum2 = query2.aggregate(jovenes_sum2=Sum('jovenes'))['jovenes_sum2']
        div_sexual_sum2 = query2.aggregate(div_sexual_sum2=Sum('div_sexual'))['div_sexual_sum2']
        vih_sum2 = query2.aggregate(vih_sum2=Sum('vih'))['vih_sum2']
        etnica_sum2 = query2.aggregate(etnica_sum2=Sum('etnica'))['etnica_sum2']
        discapacidad_sum2 = query2.aggregate(discapacidad_sum2=Sum('discapacidad'))['discapacidad_sum2']
        global_sum2 = query2.aggregate(global_sum2=Sum('total'))['global_sum2']

        tabla[opcion[1]] = {
            'hombres':hombres_sum2,
            'mujeres': mujeres_sum2,
            'jovenes': jovenes_sum2,
            'div_sexual': div_sexual_sum2,
            'vih': vih_sum2,
            'etnica': etnica_sum2,
            'discapacidad': discapacidad_sum2,
            'global': global_sum2
            }

    return render_to_response('fed/indicador230.html', RequestContext(request, locals()))

@session_required
def indicador231(request):
    resultado = Resultado.objects.get(pk=5)
    tabla = {}
    tabla2 = {}
    a = _queryset_filtrado(request, resultado)

    opcion = CHOICE_VICTIMAS[0][0]
    query = AtencionVictima.objects.filter(encuesta__in=a, accion=opcion)    
    servicio_psicologia_sum = query.aggregate(servicio_psicologia_sum=Sum('servicio_psicologia'))['servicio_psicologia_sum']
    servicio_legal_sum = query.aggregate(servicio_legal_sum=Sum('servicio_legal'))['servicio_legal_sum']    

    tabla[CHOICE_VICTIMAS[0][1]] = {
        'servicio_psicologia': servicio_psicologia_sum,
        'servicio_legal': servicio_legal_sum        
        }

    opcion2 = CHOICE_VICTIMAS[1][0]
    query2 = AtencionVictima.objects.filter(encuesta__in=a, accion=opcion2)    
    servicio_psicologia_sum2 = query2.aggregate(servicio_psicologia_sum2=Sum('servicio_psicologia'))['servicio_psicologia_sum2']
    servicio_legal_sum2 = query2.aggregate(servicio_legal_sum2=Sum('servicio_legal'))['servicio_legal_sum2']    

    tabla[CHOICE_VICTIMAS[1][1]] = {
        'servicio_psicologia': servicio_psicologia_sum2,
        'servicio_legal': servicio_legal_sum2, 
        }    

    return render_to_response('fed/indicador231.html', RequestContext(request, locals()))

@session_required
def indicador232(request):
    resultado = Resultado.objects.get(pk=5)
    tabla = {}
    tabla2 = {}
    tabla3 = {}
    a = _queryset_filtrado(request, resultado)

    opcion = CHOICE_DENUNCIAS[0][0]
    query = DenunciaViolencia.objects.filter(encuesta__in=a, accion=opcion)
    comisariato_sum = query.aggregate(comisariato_sum=Sum('comisariato'))['comisariato_sum']
    fiscalia_sum = query.aggregate(fiscalia_sum=Sum('fiscalia'))['fiscalia_sum']

    tabla[CHOICE_DENUNCIAS[0][1]] = {
        'comisariato':comisariato_sum,
        'fiscalia': fiscalia_sum,
        }

    opcion2 = CHOICE_DENUNCIAS[1][0]
    query2 = DenunciaViolencia.objects.filter(encuesta__in=a, accion=opcion2)
    comisariato_sum2 = query2.aggregate(comisariato_sum2=Sum('comisariato'))['comisariato_sum2']
    fiscalia_sum2 = query2.aggregate(fiscalia_sum2=Sum('fiscalia'))['fiscalia_sum2']

    tabla[CHOICE_DENUNCIAS[1][1]] = {
        'comisariato':comisariato_sum2,
        'fiscalia': fiscalia_sum2,
        }    
    opcion3 = CHOICE_DENUNCIAS[2][0]
    query3 = DenunciaViolencia.objects.filter(encuesta__in=a, accion=opcion3)
    comisariato_sum3 = query3.aggregate(comisariato_sum3=Sum('comisariato'))['comisariato_sum3']
    fiscalia_sum3 = query3.aggregate(fiscalia_sum3=Sum('fiscalia'))['fiscalia_sum3']

    tabla2[CHOICE_DENUNCIAS[2][1]] = {
        'comisariato':comisariato_sum3,
        'fiscalia': fiscalia_sum3,
        }
    
    return render_to_response('fed/indicador232.html', RequestContext(request, locals()))

@session_required
def indicador233(request):
    resultado = Resultado.objects.get(pk=5)
    tabla = {}    
    a = _queryset_filtrado(request, resultado)

    opcion = CHOICE_ALBERGUES[0][0]
    query = AtencionVictimaAlbergue.objects.filter(encuesta__in=a, accion=opcion)
    mujeres_sum = query.aggregate(mujeres_sum=Sum('mujeres'))['mujeres_sum']
    jovenes_sum = query.aggregate(jovenes_sum=Sum('jovenes'))['jovenes_sum']
    ninos_ninas_sum = query.aggregate(ninos_ninas_sum=Sum('ninos_ninas'))['ninos_ninas_sum']

    tabla[CHOICE_ALBERGUES[0][1]] = {
        'mujeres':mujeres_sum,
        'jovenes': jovenes_sum,
        'ninos_ninas': ninos_ninas_sum,
        }

    opcion2 = CHOICE_ALBERGUES[1][0]
    query2 = AtencionVictimaAlbergue.objects.filter(encuesta__in=a, accion=opcion2)
    mujeres_sum2 = query2.aggregate(mujeres_sum2=Sum('mujeres'))['mujeres_sum2']
    jovenes_sum2 = query2.aggregate(jovenes_sum2=Sum('jovenes'))['jovenes_sum2']
    ninos_ninas_sum2 = query2.aggregate(ninos_ninas_sum2=Sum('ninos_ninas'))['ninos_ninas_sum2']

    tabla[CHOICE_ALBERGUES[1][1]] = {
        'mujeres':mujeres_sum2,
        'jovenes': jovenes_sum2,
        'ninos_ninas': ninos_ninas_sum2,
        }    

    return render_to_response('fed/indicador233.html', RequestContext(request, locals()))

@session_required
def indicador234(request):
    resultado = Resultado.objects.get(pk=5)
    tabla = {}
    tabla2 = {}
    a = _queryset_filtrado(request, resultado)

    opcion = CHOICE_REF[0][0]
    query = ReferenciaContraRef.objects.filter(encuesta__in=a, accion=opcion)
    mujeres_sum = query.aggregate(mujeres_sum=Sum('mujeres'))['mujeres_sum']
    jovenes_sum = query.aggregate(jovenes_sum=Sum('jovenes'))['jovenes_sum']
    ninos_ninas_sum = query.aggregate(ninos_ninas_sum=Sum('ninos_ninas'))['ninos_ninas_sum']

    tabla[CHOICE_REF[0][1]] = {
        'mujeres':mujeres_sum,
        'jovenes': jovenes_sum,
        'ninos_ninas': ninos_ninas_sum,
        }

    opcion2 = CHOICE_REF[1][0]
    query2 = ReferenciaContraRef.objects.filter(encuesta__in=a, accion=opcion2)
    mujeres_sum2 = query2.aggregate(mujeres_sum2=Sum('mujeres'))['mujeres_sum2']
    jovenes_sum2 = query2.aggregate(jovenes_sum2=Sum('jovenes'))['jovenes_sum2']
    ninos_ninas_sum2 = query2.aggregate(ninos_ninas_sum2=Sum('ninos_ninas'))['ninos_ninas_sum2']

    tabla[CHOICE_REF[1][1]] = {
        'mujeres':mujeres_sum2,
        'jovenes': jovenes_sum2,
        'ninos_ninas': ninos_ninas_sum2,
        }

    tabla2['Efectividad %'] = {
        'mujeres':get_prom(mujeres_sum, mujeres_sum2),
        'jovenes': get_prom(jovenes_sum, jovenes_sum2),
        'ninos_ninas': get_prom(ninos_ninas_sum, ninos_ninas_sum2),
        }

    return render_to_response('fed/indicador234.html', RequestContext(request, locals()))

@session_required
def indicador311(request):
    resultado = Resultado.objects.get(pk=6)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS3:
        query = AccionPromuevenIntercambio.objects.filter(encuesta__in=a, accion=opcion[0])
        acciones_org_part_sum = query.aggregate(acciones_org_part_sum=Sum('acciones_org_part'))['acciones_org_part_sum']
        participantes_sum = query.aggregate(participantes_sum=Sum('participantes'))['participantes_sum']
        acciones_efectivas_sum = query.aggregate(acciones_efectivas_sum=Sum('acciones_efectivas'))['acciones_efectivas_sum']
        prom = get_prom(acciones_org_part_sum, acciones_efectivas_sum)

        tabla[opcion[1]] = {
            'acciones_org_part':acciones_org_part_sum,
            'participantes': participantes_sum,
            'acciones_efectivas':acciones_efectivas_sum,
            'prom':prom
            }

    return render_to_response('fed/indicador311.html', RequestContext(request, locals()))

@session_required
def indicador312(request):
    resultado = Resultado.objects.get(pk=6)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in MEDIOS3:
        query = AccionFortaleceCapacidad.objects.filter(encuesta__in=a, accion=opcion[0])
        acciones_sum = query.aggregate(acciones_sum=Sum('acciones'))['acciones_sum']
        participantes_sum = query.aggregate(participantes_sum=Sum('participantes'))['participantes_sum']
        acciones_efectivas_sum = query.aggregate(acciones_efectivas_sum=Sum('acciones_efectivas'))['acciones_efectivas_sum']
        prom = get_prom(acciones_sum, acciones_efectivas_sum)

        tabla[opcion[1]] = {
            'acciones_org_part':acciones_sum,
            'participantes': participantes_sum,
            'acciones_efectivas':acciones_efectivas_sum,
            'prom':prom
            }

    return render_to_response('fed/indicador312.html', RequestContext(request, locals()))

@session_required
def indicador313(request):
    resultado = Resultado.objects.get(pk=6)
    tabla = {}
    a = _queryset_filtrado(request, resultado)

    for opcion in CHOICE4:
        query = AccionFortaleceCapAdmitiva.objects.filter(encuesta__in=a, accion=opcion[0])
        mejorar_sistema_sum = query.aggregate(mejorar_sistema_sum=Sum('mejorar_sistema'))['mejorar_sistema_sum']
        mejorar_plan_sum = query.aggregate(mejorar_plan_sum=Sum('mejorar_plan'))['mejorar_plan_sum']
        mejorar_apoyo_sum = query.aggregate(mejorar_apoyo_sum=Sum('mejorar_apoyo'))['mejorar_apoyo_sum']


        tabla[opcion[1]] = {
            'mejorar_sistema':mejorar_sistema_sum,
            'mejorar_plan': mejorar_plan_sum,
            'mejorar_apoyo':mejorar_apoyo_sum,
            }

    #para graficos    
    si_hay = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, sistema=CHOICE1[0][0]).count()
    hay_pero_no = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, sistema=CHOICE1[1][0]).count()
    no_hay = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, sistema=CHOICE1[2][0]).count()
    
    total = si_hay + hay_pero_no + no_hay    
    val1 = get_prom(total, si_hay)
    val2 = get_prom(total, hay_pero_no)
    val3 = get_prom(total, no_hay)

    si_hay_plan = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, plan=CHOICE2[0][0]).count()
    no_utiliza = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, plan=CHOICE2[1][0]).count()
    no_hay_plan = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, plan=CHOICE2[2][0]).count()

    total2 = si_hay_plan + no_utiliza + no_hay_plan
    val4 = get_prom(total2, si_hay_plan)
    val5 = get_prom(total2, no_utiliza)
    val6 = get_prom(total2, no_hay_plan)

    ninguna = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, organizaciones=CHOICE3[0][0]).count()
    en_proceso = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, organizaciones=CHOICE3[1][0]).count()
    logrado = EstadoCapacidadAdmitiva.objects.filter(encuesta__in=a, organizaciones=CHOICE3[2][0]).count()

    total3 = ninguna + en_proceso + logrado
    val7 = get_prom(total3, ninguna)
    val8 = get_prom(total3, en_proceso)
    val9 = get_prom(total3, logrado)


    return render_to_response('fed/indicador313.html', RequestContext(request, locals()))

#obtener la vista adecuada para los indicadores
def _get_view(request, vista):
    if vista in VALID_VIEWS:
        return VALID_VIEWS[vista](request)
    else:
        raise ViewDoesNotExist("Tried %s in module %s Error: View not define in VALID_VIEWS." % (vista, 'encuesta.views'))

VALID_VIEWS = {
    '1': resultado1,
    '2': resultado2,

    #inicia vistas de indicadores
    'acciones-impulsadas': indicador111,
    'participacion-en-instancias': indicador112,
    #INDICADOR ELIMINADO POR FED
    'observatorios-para-vigilancia': indicador114,
    #indicadores para resultado 1.2
    'acciones-publicas': indicador121,
    'acciones-de-denuncias-juridicas': indicador122,
    #indicadores para resultado 2.1
    'acciones-efectuadas': indicador211,
    'cambios-en-las-poblaciones': indicador212,
    #indicadores para resultado 2.2.1
    'acciones-por-organizaciones': indicador221,
    'grupos-div-sexual-y-discapacidad': indicador222,
    'grupos-etnico-indigenas-y-jovenes': indicador223,
    #indicadores para resultado 2.3
    'atencion-a-la-salud': indicador230,
    'servicios-de-atencion': indicador231,
    'denuncias-interpuestas': indicador232,
    'victimas-atendidas': indicador233,
    'referencias-y-contrareferencias': indicador234,
    #indicadores para resultado 3.1
    'intercambio-teorico-y-metod':indicador311,
    'medir-y-reportar-indicadores': indicador312,
    'mejorar-la-gestion': indicador313,
    }

def get_prom(total, cantidad):
    if total == None or cantidad == None or total == 0:
        x = 0
    else:
        x = (cantidad * 100) / float(total)
    return x
