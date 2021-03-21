import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_lataa_rahaa_lataa_rahaa_tilille(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "saldo: 1.1")
    
    def test_saldo_vahenee_kun_rahaa_riittavasti(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(str(self.maksukortti), "saldo: 0.05")

    def test_saldon_vahentyessa_palautetaan_true(self):
        self.assertEqual(self.maksukortti.ota_rahaa(5), True)

    def test_saldo_ei_vahene_kun_ei_riittavasti_rahaa(self):
        self.maksukortti.ota_rahaa(20)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_kun_ei_riittavasti_saldoa_palautetaan_false(self):
        self.assertEqual(self.maksukortti.ota_rahaa(20), False)