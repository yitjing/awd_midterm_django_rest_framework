from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
# used to create the table and relationships in the database

# Organisms HAVE MANY Proteins
# Organisms HAVE A Genus name
# Organisms HAVE A Species name
class Organism(models.Model):
	taxa_id = models.IntegerField(primary_key=True)
	clade = models.CharField(max_length=50)
	genus = models.CharField(max_length=100)
	species = models.CharField(max_length=100)
	
	def __str__(self):
		return self.genus + " " + self.species

# Proteins HAVE MANY domains
# Proteins HAVE ONE sequence
class Protein(models.Model):
	protein_id = models.CharField(primary_key=True, max_length=50)
	sequence = models.CharField(max_length=100)
	protein_length = models.IntegerField(default=0)
	taxonomy = models.ForeignKey(Organism, on_delete = models.CASCADE, related_name='proteins')
	domain = models.ManyToManyField('Domain', related_name ='proteins')
	def __str__(self):
		return self.protein_id
		
# Domains HAVE ONE pfam domain ID
class Domain(models.Model):
	id = models.AutoField(primary_key=True)
	domain_id = models.CharField(max_length=50, default=0)
	d_description = models.CharField(max_length=100)
	start_coor = models.IntegerField()
	end_coor = models.IntegerField()
	d_pfam_description = models.CharField(max_length=100, default='nothing')
	protein = models.ForeignKey(Protein, on_delete = models.CASCADE, related_name='domains')
	
	def __str__(self):
		return self.domain_id
		
class DomainProtein(models.Model):
	domain = models.ForeignKey(Domain, on_delete = models.CASCADE)
	protein = models.ForeignKey(Protein, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.domain.domain_id + " " + self.protein.protein_id
