from django.urls import path
from .views import *
from . import views
from . import api

urlpatterns = [
	#introduction page
	path('', views.index, name="index"),	
	
	#post request
	path('api/protein/', api.AddNewProtein.as_view(), name='addNewProtein'),
	#get request
	path('api/protein/<str:protein_id>/', api.SpecificProteinListView.as_view()),
	path('api/pfam/<str:domain_id>/', api.PfamListView.as_view(), name='pFamList'),
	path('api/proteins/<int:taxa_id>', api.ProteinOrganismListView.as_view(), name='proteinOrganismList'),
	path('api/pfams/<int:taxa_id>', api.OrganismDomainListView.as_view(), name='organismDomainList'),
	path('api/coverage/<str:protein_id>/', api.DomainCoverageListView.as_view(), name='domainCoverageList'),
	
	#for testing
	path('api/organisms/',views.organismsListView, name='organismsListView'),
	path('api/domains/',views.domainsListView, name='domainsListView'),
	path('api/proteins/',views.proteinsListView, name='proteinsListView'),
	path('api/organism/<int:pk>', views.modify_organism, name='modify_organism'),
	path('api/protein/<str:pk>', views.modify_protein, name='modify_protein'),
	path('api/domain/<str:pk>', views.modify_domain, name='modify_domain'),
]
