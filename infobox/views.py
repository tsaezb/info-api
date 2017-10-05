# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from requests.utils import quote

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, APIException

import random

from infobox.models import Property
from infobox.serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


@api_view(['GET'])
def update_frecuency_count(request):
    _get_frecuency_count()


def _get_frecuency_count():
    query = "SELECT ?p (count(*) AS ?count) WHERE { ?s ?p ?o. } GROUP BY ?p ORDER BY DESC(?count)"
    return requests.get("https://query.wikidata.org/sparql?format=json&query="+quote(query))


@api_view(['GET'])
def get_entity_info(request):
    """
    API endpoint to retrieve Wikidata information
    """
    entity_id = request.GET['id'] or ''
    lang = request.GET['lang'] or ''
    strategy = request.GET['strategy'] or ''
    size = 10

    if strategy not in ['baseline', 'frecuency']:
        raise ValidationError('A valid strategy must be specified (or the parameter must not be used)', code=400)
    if entity_id == '':
        raise ValidationError('An entity ID must be given (add id parameter)', code=400)
    if lang == '':
        raise ValidationError('A language must be specified (add lang parameter)', code=400)

    infobox = {}
    wikidata_prop = _get_wikidata_info(entity_id, lang)
    wikidata_headers = _get_label_and_description(entity_id, lang)

    if wikidata_prop.status_code != 200:
        raise APIException("Error on Wikidata API", wikidata_prop.status_code)

    if wikidata_headers.status_code != 200:
        raise APIException("Error on Wikidata API", wikidata_headers.status_code)
    # add if , to manage empty results of wikidata request
    # baseline

    infobox['label'] = wikidata_headers.json()['results']['bindings'][0]['label']['value']
    infobox['description'] = wikidata_headers.json()['results']['bindings'][0]['description']['value']

    if strategy == 'baseline':
        infobox['properties'] = _infobox_baseline(wikidata_prop.json().get('results').get('bindings'), size)

    elif strategy == 'frecuency':
        infobox['properties'] = _infobox_frecuency_count(wikidata_prop.json().get('results').get('bindings'), size)

    return Response(infobox)


def _get_wikidata_info(entity_id, lang):
    query = "SELECT ?pLabel ?prop ?val WHERE { wd:Q" + entity_id + " ?prop ?val . ?ps wikibase:directClaim ?prop . ?ps rdfs:label ?pLabel . FILTER((LANG(?pLabel)) = '" + lang + "')}"
    return requests.get("https://query.wikidata.org/sparql?format=json&query="+quote(query))


def _get_label_and_description(entity_id, lang):
    query = "SELECT ?label ?description WHERE { wd:Q" + entity_id + " rdfs:label ?label . wd:Q" + entity_id + " schema:description ?description. FILTER((LANG(?label)) = '" + lang + "' && (LANG(?description) = '" + lang + "'))}"

    return requests.get("https://query.wikidata.org/sparql?format=json&query="+quote(query))


def _infobox_baseline(prop, n):
    random.shuffle(prop)
    return prop[:n]


def _infobox_frecuency_count(prop, n):
    for p in prop:
        p['prop']['frecuency'] = Property.objects.get(identifier=p.get('prop').get('value')).get_frecuency()
    return sorted(prop, key=lambda x: x.get('prop').get('frecuency'), reverse=True)[:n]
