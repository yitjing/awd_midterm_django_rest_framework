import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from rest_api_app.models import *
from rest_api_app.serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#static webpage
def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render({}, request))
	
## Testing ##
# API view to get all organism
@api_view(['GET','POST'])
def organismsListView(request):
	#get all organisms
	if request.method == 'GET':
		organisms = Organism.objects.all()
		serializer = OrganismSerializer(organisms, many=True)
		return Response(serializer.data)
		#insert a new record for a organism
	elif request.method == 'POST':
		return Response({})

# API view to get all proteins		
@api_view(['GET','POST'])
def proteinsListView(request):
	#get all proteins
	if request.method == 'GET':
		proteins = Protein.objects.all()
		serializer = ProteinSerializer(proteins, many=True)
		return Response(serializer.data)
		#insert a new record for a protein
	elif request.method == 'POST':
		return Response({})

# API view to get all domains		
@api_view(['GET','POST'])
def domainsListView(request):
	#get all domains
	if request.method == 'GET':
		domains = Domain.objects.all()
		serializer = DomainSerializer(domains, many=True)
		return Response(serializer.data)
		#insert a new record for a domain
	elif request.method == 'POST':
		return Response({})
		
		
@api_view(['GET','UPDATE','DELETE'])
def modify_organism(request, pk):
	try:
		organism = Organism.objects.get(pk=pk)
	except Organism.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	#get details of a single organism
	if request.method == 'GET':
		serializer = OrganismSerializer(organism)
		return Response(serializer.data)
		
@api_view(['GET','UPDATE','DELETE'])
def modify_protein(request, pk):
	try:
		protein = Protein.objects.get(pk=pk)
	except Protein.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	#get details of a single protein
	if request.method == 'GET':
		serializer = ProteinSerializer(protein)
		return Response(serializer.data)
		
@api_view(['GET','UPDATE','DELETE'])
def modify_domain(request, pk):
	try:
		domain = Domain.objects.get(pk=pk)
	except Domain.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	#get details of a single domain
	if request.method == 'GET':
		serializer = DomainSerializer(domain)
		return Response(serializer.data)
