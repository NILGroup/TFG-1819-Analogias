from django.shortcuts import render
import prototipo.functions as f
import prototipo.servicesSearchWords as services
import json



from .forms import PostFormWordSearch


def index(request):
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'button-search' in request.POST:
            words = request.POST.get('word')
            print(words)
            word = form['word'].value()
            #print(word)
            results = services.findOffsetsToTheSynsets(words)
            #print(results)
            return render(request, 'prototipo/index.html', {'form': form, 'word': word, 'results': results})



    return render(request, 'prototipo/index.html')





def prueba(request):
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'boton-final' in request.POST:

            word = form['word'].value()
            resultadoSinonimos , resultadoHiponimo, resultadoHiperonimo  = f.busquedaDePalabras(word)

            profundidad = 1
            encontrado = False

            dict_resultados = dict(sinonimos="", hiponimos="", hiperonimos="")

            while profundidad <= 3 and encontrado == False:
                dict_resultados["sinonimos"] = list(f.busquedaSinonimosEnLaRAE(resultadoSinonimos, profundidad))
                dict_resultados["hiponimos"] = list(f.busquedaHiponimosEnLaRAE(resultadoHiponimo, profundidad))
                dict_resultados["hiperonimos"] = list(f.busquedaHiperonimosEnLaRAE(resultadoHiperonimo, profundidad))

                if len(dict_resultados["sinonimos"]) > 0 or len(dict_resultados["hiponimos"]) > 0 or len(
                        dict_resultados["hiperonimos"]) > 0:
                    encontrado = True

                profundidad += 1

            return render(request, 'prototipo/formulario.html', {'form': form, 'resultadoSinonimos': resultadoSinonimos,
                                                                 'resultadoHiponimo': resultadoHiponimo,
                                                                 'resultadoHiperonimo': resultadoHiperonimo,
                                                                 'word': word, 'dict': dict_resultados,
                                                                 'json': json.dumps(dict_resultados,
                                                                                ensure_ascii=False)})

    return render(request, 'prototipo/formulario.html', {'form': form})



