# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlquote

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
def get_entity_info(request):
  """
  API endpoint to retrieve Wikidata information
  """
  entity_id = request.GET['id'] or ''
  lang = request.GET['lang'] or ''
  strategy = request.GET['strategy'] or ''

  if strategy not in ['baseline']:
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

  #add if , to manage empty results of wikidata request

  #baseline
  if strategy == 'baseline':
    infobox['properties'] = _infobox_baseline(wikidata_prop.json().get('results').get('bindings'), 10)
    infobox['label']  = wikidata_headers.json()['results']['bindings'][0]['label']['value']
    infobox['description']  = wikidata_headers.json()['results']['bindings'][0]['description']['value']
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
