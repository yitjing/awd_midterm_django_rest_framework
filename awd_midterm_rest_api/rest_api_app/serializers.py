from rest_framework import serializers
from .models import Organism, Domain, Protein, DomainProtein

# fields is what is shown on the rest api (the json format from the example given)
# fields indicate the fields in the model
# organism serializer
class OrganismSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organism
		fields = ['taxa_id', 'clade', 'genus', 'species']
		
# pfam domain serializer
class PfamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Domain
		fields = ['domain_id', 'd_pfam_description']

# domain serializer		
class DomainSerializer(serializers.ModelSerializer):
	class Meta:
		model= Domain
		fields = ['domain_id', 'd_pfam_description','d_description', 'start_coor', 'end_coor']

#protein serializer		
class ProteinSerializer(serializers.ModelSerializer):
	class Meta:
		model = Protein
		fields = ['protein_id','sequence','protein_length']

# display specific protein details for a given organism		
class SpecificProteinSerializer(serializers.ModelSerializer):
	domains= DomainSerializer(many=True)
	taxonomy = OrganismSerializer()
	
	class Meta:
		model = Protein
		fields = ['protein_id', 'sequence', 'taxonomy', 'protein_length', 'domains']
		
	def validate(self, attrs):
		taxonomy_data = attrs.get('taxonomy')
		domains = attrs.get('domains')
		
		# validate taxonomy fields
		if not taxonomy_data:
			raise serializers.ValidationError("taxonomy field is required")
		# validate domains field
		if not domains:
			raise serializers.ValidationError("domains field is required")
		return attrs
	
	def create(self, validated_data):
		taxonomy_data = validated_data.pop('taxonomy')
		domains_data = validated_data.pop('domains')
		
		taxonomy = Organism.objects.create(**taxonomy_data)
		protein = Protein.objects.create(taxonomy=taxonomy, **validated_data)
	
		for domain_data in domains_data:
			Domain.objects.create(protein=protein, **domain_data)
		return protein	

# display all proteins for a given organism		
class OrganismProteinSerializer(serializers.ModelSerializer):
	class Meta:
		model = DomainProtein
		fields = ['domain','protein']

# display a list of all domains for a given organism		
class OrganismDomainSerializer(serializers.ModelSerializer):
	pfam_id = PfamSerializer(source='domain')
	class Meta:
		model = DomainProtein
		fields = ['domain', 'pfam_id']
		
# display the calculation of the domain coverage	
class DomainCoverageSerializer(serializers.ModelSerializer):
	#That is Sum of the protein domain lengths (start-stop)/length of protein.
	coverage = serializers.FloatField()
	class Meta:
		model = Domain
		fields = ['coverage']
