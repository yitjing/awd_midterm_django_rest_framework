from rest_api_app.models import *
from rest_api_app.serializers import *

#imports to test Rest Api
from rest_framework.test import APITestCase
from django.urls import reverse

import json
from rest_framework import status
from django.test import TestCase, Client

# Create your tests here.

# test foreign key on models	
class TestProteinModelFk(TestCase):
	
	def test_fk(self):
		# create a organism
		taxonomy = Organism(taxa_id='53326', clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy.save()
		
		#create a protein and link one to many relationship to the organism
		protein = Protein(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy)
		protein.save()
		
		#get the protein with protein_id=A0A016S8J7
		data = Protein.objects.get(protein_id='A0A016S8J7')
		#check if "data" has a organism with a taxa_id = 53326
		self.assertEqual(data.taxonomy.taxa_id, 53326)

# test rest api	
# get the object and test the field value
class OrganismTest(TestCase):
	def setUp(self):
		Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')

	
	def test_orgainsm_genus(self):
		organism_ceylanicum = Organism.objects.get(taxa_id =53326)
		organism_robertsii = Organism.objects.get(taxa_id =568076)


		self.assertEqual(organism_ceylanicum.__str__(), 'Ancylostoma ceylanicum')
		self.assertEqual(organism_robertsii.__str__(), 'Metarhizium robertsii')
		
class ProteinTest(TestCase):
	def setUp(self):
		taxonomy_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		
		Protein.objects.create(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy_a)
		Protein.objects.create(protein_id="A0A014PQC0", sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy_b)
		
	def test_protein_id(self):
		protein_a = Protein.objects.get(sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA')
		protein_b = Protein.objects.get(sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK')
	
		self.assertEqual(protein_a.__str__(), 'A0A016S8J7')
		self.assertEqual(protein_b.__str__(), 'A0A014PQC0')
		
class DomainTest(TestCase):
	def setUp(self):
		taxonomy = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		protein = Protein.objects.create(protein_id="A0A014PQC0", sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy)
		
		Domain.objects.create(domain_id='PF02800', d_description='Glyceraldehyde 3-phosphate dehydrogenase catalytic domain', d_pfam_description='Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain', start_coor=157, end_coor=314, protein=protein)
		
	def test_domain_id(self):
		domain = Domain.objects.get(d_description='Glyceraldehyde 3-phosphate dehydrogenase catalytic domain')
		
		self.assertEqual(domain.__str__(), 'PF02800')

#initialize the APIClient app
client = Client()

# Testing that all model objects are equal to their corresponding serializer representations.
class AllOrganismsTest(TestCase):
	def setUp(self):
		Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		Organism.objects.create(taxa_id =7160, clade='E', genus='Aedes', species='albopictus')
		
	#pulls the test from the view to test it
	def test_get_all_organisms(self):
		#get API response
		response = client.get(reverse('organismsListView'))
		#get data from db/models
		organisms = Organism.objects.all()
		#get data from serializer
		serializer = OrganismSerializer(organisms, many=True)
		#organism objects from models matches organism objects in serializer
		self.assertEqual(response.data, serializer.data)
		
		#check if server response 200. if yes test pass
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
class AllProteinsTest(TestCase):
	def setUp(self):
		taxonomy_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		taxonomy_c = Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		
		Protein.objects.create(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy_a)
		Protein.objects.create(protein_id='A0A014PQC0', sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy_b)
		Protein.objects.create(protein_id='A0A022PT25', sequence='MALNSILSRPSSFSSRNLLKNYSASDSAFSLPIQSISFLNPIPLFSNVSFNNASPAFSSVPVRAASASGSPSATVAQSPELKIKIVPTQPIEGQKTGTSGLRKKVKVFMQDNYLANWIQALFDSLPPEDYKGGVLVLGGDGRYFNKEAAQIIIKIAAGNGVGKILVGKDGIMSTPAVSAVIRKRKANGGFVMSASHNPGGPDYDWGIKFNYSSGQPAPESITDKIYGNTLSISEIKMVDFPDVDLSLLGLIDYGNFSVEVVDPVADYLELMENVFDFSLIKSLLSRPDFRFVFDAMHAVTGAYAKPIFVDKLGASPDSILNGVPLEDFGHGHPDPNLTYAEDLVKIMYGDNGPAFGAASDGDGDRNMVLGKGFFVTPSDSVAIIAANAEEAIPYFKSGPKGLARSMPTSGALDRVAKKLNLPFFEVPTGWKFFGNLMDAGNLSICGEESFGTGSDHIREKDGIWAVLAWMSIIAFRNKDKKAGEKLVSVADVVTEHWATYGRNFFSRYDYEESLECESEGANKMVEHLRDIISKSKEGDVYGNYTLQFADDFNYTDPVDGSVVSKQGIRFVFTDGSRIIFRLSGTGSAGATVRIYIEQFEPEASKHDVDAQIALKPLIDLALSTSKLKEFTGREKPTVIT', protein_length= '640', taxonomy=taxonomy_c)
		
	#pulls the test from the view to test it
	def test_get_all_proteins(self):
		#get API response
		response = client.get(reverse('proteinsListView'))
		#get data from db/models
		proteins = Protein.objects.all()
		#get data from serializer
		serializer = ProteinSerializer(proteins, many=True)
		#protein objects from models matches protein objects in serializer
		self.assertEqual(response.data, serializer.data)
		
		#check if server response 200. if yes test pass
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
class AllDomainsTest(TestCase):
	def setUp(self):
		taxonomy_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		taxonomy_c = Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		
		protein_a = Protein.objects.create(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy_a)
		protein_b = Protein.objects.create(protein_id='A0A014PQC0', sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy_b)
		protein_c = Protein.objects.create(protein_id='A0A022PT25', sequence='MALNSILSRPSSFSSRNLLKNYSASDSAFSLPIQSISFLNPIPLFSNVSFNNASPAFSSVPVRAASASGSPSATVAQSPELKIKIVPTQPIEGQKTGTSGLRKKVKVFMQDNYLANWIQALFDSLPPEDYKGGVLVLGGDGRYFNKEAAQIIIKIAAGNGVGKILVGKDGIMSTPAVSAVIRKRKANGGFVMSASHNPGGPDYDWGIKFNYSSGQPAPESITDKIYGNTLSISEIKMVDFPDVDLSLLGLIDYGNFSVEVVDPVADYLELMENVFDFSLIKSLLSRPDFRFVFDAMHAVTGAYAKPIFVDKLGASPDSILNGVPLEDFGHGHPDPNLTYAEDLVKIMYGDNGPAFGAASDGDGDRNMVLGKGFFVTPSDSVAIIAANAEEAIPYFKSGPKGLARSMPTSGALDRVAKKLNLPFFEVPTGWKFFGNLMDAGNLSICGEESFGTGSDHIREKDGIWAVLAWMSIIAFRNKDKKAGEKLVSVADVVTEHWATYGRNFFSRYDYEESLECESEGANKMVEHLRDIISKSKEGDVYGNYTLQFADDFNYTDPVDGSVVSKQGIRFVFTDGSRIIFRLSGTGSAGATVRIYIEQFEPEASKHDVDAQIALKPLIDLALSTSKLKEFTGREKPTVIT', protein_length= '640', taxonomy=taxonomy_c)
		

		Domain.objects.create(domain_id='PF01650', d_description='Peptidase C13 legumain', d_pfam_description='Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain', start_coor=40, end_coor=94, protein=protein_a)
		Domain.objects.create(domain_id='PF02800', d_description='Glyceraldehyde 3-phosphate dehydrogenase catalytic domain', d_pfam_description='Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain', start_coor=157, end_coor=314, protein=protein_b)
		Domain.objects.create(domain_id='PF00408', d_description='Alpha-D-phosphohexomutase C-terminal', d_pfam_description='Phosphoglucomutase/phosphomannomutase: C-terminaldomain', start_coor=564, end_coor=615, protein=protein_c)
		
	#pulls the test from the view to test it
	def test_get_all_domains(self):
		#get API response
		response = client.get(reverse('domainsListView'))
		#get data from db/models
		domains = Domain.objects.all()
		#get data from serializer
		serializer = DomainSerializer(domains, many=True)
		#domain objects from models matches domain objects in serializer
		self.assertEqual(response.data, serializer.data)
		
		#check if server response 200. if yes test pass
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
class SingleOrganismTest(TestCase):
	def setUp(self):
		self.organism_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		self.organism_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		self.organism_c = Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		
	def test_get_valid_single_organism(self):
		#pass ceylanicum species organism to view via modify_organism
		response = client.get(reverse('modify_organism', kwargs={'pk': self.organism_a.pk}))
		#get ceylanicum from models
		organism = Organism.objects.get(pk=self.organism_a.pk)
		serializer = OrganismSerializer(organism)
		self.assertEqual(response.data, serializer.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	def test_get_invalid_organism(self):
		invalid_id = 123456
		response = self.client.get(reverse('modify_organism', kwargs={'pk': invalid_id}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		
class SingleProteinTest(TestCase):
	def setUp(self):
		taxonomy_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		taxonomy_c = Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		
		self.protein_a = Protein.objects.create(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy_a)
		self.protein_b = Protein.objects.create(protein_id='A0A014PQC0', sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy_b)
		self.protein_c = Protein.objects.create(protein_id='A0A022PT25', sequence='MALNSILSRPSSFSSRNLLKNYSASDSAFSLPIQSISFLNPIPLFSNVSFNNASPAFSSVPVRAASASGSPSATVAQSPELKIKIVPTQPIEGQKTGTSGLRKKVKVFMQDNYLANWIQALFDSLPPEDYKGGVLVLGGDGRYFNKEAAQIIIKIAAGNGVGKILVGKDGIMSTPAVSAVIRKRKANGGFVMSASHNPGGPDYDWGIKFNYSSGQPAPESITDKIYGNTLSISEIKMVDFPDVDLSLLGLIDYGNFSVEVVDPVADYLELMENVFDFSLIKSLLSRPDFRFVFDAMHAVTGAYAKPIFVDKLGASPDSILNGVPLEDFGHGHPDPNLTYAEDLVKIMYGDNGPAFGAASDGDGDRNMVLGKGFFVTPSDSVAIIAANAEEAIPYFKSGPKGLARSMPTSGALDRVAKKLNLPFFEVPTGWKFFGNLMDAGNLSICGEESFGTGSDHIREKDGIWAVLAWMSIIAFRNKDKKAGEKLVSVADVVTEHWATYGRNFFSRYDYEESLECESEGANKMVEHLRDIISKSKEGDVYGNYTLQFADDFNYTDPVDGSVVSKQGIRFVFTDGSRIIFRLSGTGSAGATVRIYIEQFEPEASKHDVDAQIALKPLIDLALSTSKLKEFTGREKPTVIT', protein_length= '640', taxonomy=taxonomy_c)
		
	def test_get_valid_single_protein(self):
		#pass protein_id to view via modify_protein
		response = client.get(reverse('modify_protein', kwargs={'pk': self.protein_a.pk}))
		#get ceylanicum from models
		protein = Protein.objects.get(pk=self.protein_a.pk)
		serializer = ProteinSerializer(protein)
		self.assertEqual(response.data, serializer.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	def test_get_invalid_protein(self):
		invalid_id = 'A292379'
		response = self.client.get(reverse('modify_protein', kwargs={'pk': invalid_id}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		
		
class SingleDomainTest(TestCase):
	def setUp(self):
		taxonomy_a = Organism.objects.create(taxa_id =53326, clade='E', genus='Ancylostoma', species='ceylanicum')
		taxonomy_b = Organism.objects.create(taxa_id =568076, clade='E', genus='Metarhizium', species='robertsii')
		taxonomy_c = Organism.objects.create(taxa_id =415, clade='E', genus='Erythranthe', species='guttata')
		
		protein_a = Protein.objects.create(protein_id='A0A016S8J7', sequence='MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA', protein_length= '101', taxonomy=taxonomy_a)
		protein_b = Protein.objects.create(protein_id='A0A014PQC0', sequence='MAPVKVGINGFGRIGRIVFRNAAEHPEIEVVAVNDPFIDTEYAAYMLKYDSSHGIFKGDIKKEADGLVVNGKKVKFFTERDPSAIPWKSAGAEYIVESTGVFTTTDKAKAHLAGGAKKVVISAPSADAPMYVMGVNEKTYDGKADVISNASCTTNCLAPLAKVIHDKFTIVEGLMTTVHSYTATQKTVDGPSGKDWRGGRGAAQNIIPSSTGAAKAVGKVIPDLNGKLTGMSMRVPTANVSVVDLTARIEKGASYDEIKEAIKEAANGPLKGILAYTEDDVVSSDMNGNTNSSIFDAKAGISLNKNFVKLVSWYDNEWGYSRRVLDLLAYIAKVDAGK', protein_length= '101', taxonomy=taxonomy_b)
		protein_c = Protein.objects.create(protein_id='A0A022PT25', sequence='MALNSILSRPSSFSSRNLLKNYSASDSAFSLPIQSISFLNPIPLFSNVSFNNASPAFSSVPVRAASASGSPSATVAQSPELKIKIVPTQPIEGQKTGTSGLRKKVKVFMQDNYLANWIQALFDSLPPEDYKGGVLVLGGDGRYFNKEAAQIIIKIAAGNGVGKILVGKDGIMSTPAVSAVIRKRKANGGFVMSASHNPGGPDYDWGIKFNYSSGQPAPESITDKIYGNTLSISEIKMVDFPDVDLSLLGLIDYGNFSVEVVDPVADYLELMENVFDFSLIKSLLSRPDFRFVFDAMHAVTGAYAKPIFVDKLGASPDSILNGVPLEDFGHGHPDPNLTYAEDLVKIMYGDNGPAFGAASDGDGDRNMVLGKGFFVTPSDSVAIIAANAEEAIPYFKSGPKGLARSMPTSGALDRVAKKLNLPFFEVPTGWKFFGNLMDAGNLSICGEESFGTGSDHIREKDGIWAVLAWMSIIAFRNKDKKAGEKLVSVADVVTEHWATYGRNFFSRYDYEESLECESEGANKMVEHLRDIISKSKEGDVYGNYTLQFADDFNYTDPVDGSVVSKQGIRFVFTDGSRIIFRLSGTGSAGATVRIYIEQFEPEASKHDVDAQIALKPLIDLALSTSKLKEFTGREKPTVIT', protein_length= '640', taxonomy=taxonomy_c)
		

		self.domain_a = Domain.objects.create(domain_id='PF01650', d_description='Peptidase C13 legumain', d_pfam_description='Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain', start_coor=40, end_coor=94, protein=protein_a)
		self.domain_b = Domain.objects.create(domain_id='PF02800', d_description='Glyceraldehyde 3-phosphate dehydrogenase catalytic domain', d_pfam_description='Glyceraldehyde3-phosphatedehydrogenase: C-terminaldomain', start_coor=157, end_coor=314, protein=protein_b)
		self.domain_c = Domain.objects.create(domain_id='PF00408', d_description='Alpha-D-phosphohexomutase C-terminal', d_pfam_description='Phosphoglucomutase/phosphomannomutase: C-terminaldomain', start_coor=564, end_coor=615, protein=protein_c)
		
	def test_get_valid_single_domain(self):
		#pass domain_id to view via modify_domain
		response = client.get(reverse('modify_domain', kwargs={'pk': self.domain_a.pk}))
		#get ceylanicum from models
		domain = Domain.objects.get(pk=self.domain_a.pk)
		serializer = DomainSerializer(domain)
		self.assertEqual(response.data, serializer.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
	def test_get_invalid_domain(self):
		invalid_id = 800980
		response = self.client.get(reverse('modify_domain', kwargs={'pk': invalid_id}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		

		
				
		

