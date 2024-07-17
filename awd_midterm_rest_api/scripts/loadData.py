from rest_api_app.models import Organism, Protein, Domain, DomainProtein
import csv

def run():

	with open('data/assignment_data_set.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		
		Organism.objects.all().delete()
		Protein.objects.all().delete()
		Domain.objects.all().delete()
		DomainProtein.objects.all().delete()
		
		for row in reader:
			taxonomy = Organism(taxa_id = row[1], clade = row[2], genus = row[3].split(' ')[0], species = row[3].split(' ')[1])
			taxonomy.save()
			
			protein = Protein(protein_id = row[0], protein_length= row[8], taxonomy=taxonomy)
			protein.save()
			
			domain = Domain(domain_id = row[5], d_description=row[4], start_coor=row[6], end_coor=row[7], protein=protein)
			domain.save()
			
			domainProtein = DomainProtein(domain=domain, protein=protein)
			domainProtein.save()
			
	with open('data/assignment_data_sequences.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		
		for row in reader:
			protein = Protein.objects.get(protein_id = row[0])
			protein.sequence = row[1]
			protein.save()
			
	with open('data/pfam_descriptions.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		next(reader)
		
		for row in reader:
			domains = Domain.objects.filter(domain_id = row[0])
			for domain in domains:
				domain.d_pfam_description = row[1]
				domain.save()
		
		
		
		
