import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.riittavasti_maksukortti = Maksukortti(500)
        self.alle_maksukortti = Maksukortti(100)

    # kassapäätteen alustamisen testaus

    def test_kassapaate_alussa_rahaa_1000_euroa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kassapaate_alussa_ei_yhtaan_myytya_maukasta_lounasta(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassapaate_alussa_ei_yhtaan_myytya_edullista_lounasta(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    # käteismaksun testaaminen

    # edullisesti
    def test_kateismaksu_syo_edullisesti_onnistuessa_kassassa_rahaa_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_kateismaksu_syo_edullisesti_ei_riittavasti_rahaa_kassassa_rahaa_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kateismaksu_syo_edullisesti_tasarahalla_palautetaan_nolla(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(240), 0)

    def test_kateismaksu_syo_edullisesti_suuremmalla_summalla_palautetaan_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_kateismaksu_syo_edullisesti_ei_riittavasti_rahaa_palautuu_maksu(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)

    def test_kateismaksu_syo_edullisesti_onnistuessa_myytyjen_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateismaksu_syo_edullisesti_epaonnistuessa_myytyjen_maara_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset, 0)

    # maukkaasti
    def test_kateismaksu_syo_maukkaasti_onnistuessa_kassassa_rahaa_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_kateismaksu_syo_maukkaasti_ei_riittavasti_rahaa_kassassa_rahaa_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kateismaksu_syo_maukkaasti_tasarahalla_palautetaan_nolla(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(400), 0)

    def test_kateismaksu_syo_maukkaasti_suuremmalla_summalla_palautetaan_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_kateismaksu_syo_maukkaasti_ei_riittavasti_rahaa_palautuu_maksu(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100), 100)

    def test_kateismaksu_syo_maukkaasti_onnistuessa_myytyjen_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateismaksu_syo_maukkaasti_epaonnistuessa_myytyjen_maara_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # korttioston testaaminen

    # edullisesti
    def test_korttimaksu_syo_edullisesti_onnistuessa_palauttaa_true(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.riittavasti_maksukortti), True)

    def test_korttimaksu_syo_edullisesti_onnistuessa_veloittaa_korttia(self):
        self.kassapaate.syo_edullisesti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.riittavasti_maksukortti.saldo, 260)

    def test_korttimaksu_syo_edullisesti_epaonnistuessa_palauttaa_false(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.alle_maksukortti), False)

    def test_korttimaksu_syo_edullisesti_epaonnistuessa_ei_veloita_korttia(self):
        self.kassapaate.syo_edullisesti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.alle_maksukortti.saldo, 100)
    
    def test_korttimaksu_syo_edullisesti_onnistuessa_myytyjen_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttimaksu_syo_edullisesti_epaonnistuessa_myytyjen_maara_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_korttimaksu_syo_edullisesti_onnistuessa_ei_muuta_rahaa_kassassa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_korttimaksu_syo_edullisesti_epaonnistuessa_ei_muuta_rahaa_kassassa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # maukkaasti
    def test_korttimaksu_syo_maukkaasti_onnistuessa_palauttaa_true(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.riittavasti_maksukortti), True)

    def test_korttimaksu_syo_maukkaasti_onnistuessa_veloittaa_korttia(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.riittavasti_maksukortti.saldo, 100)

    def test_korttimaksu_syo_maukkaasti_epaonnistuessa_palauttaa_false(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.alle_maksukortti), False)

    def test_korttimaksu_syo_maukkaasti_epaonnistuessa_ei_veloita_korttia(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.alle_maksukortti.saldo, 100)
    
    def test_korttimaksu_syo_maukkaasti_onnistuessa_myytyjen_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttimaksu_syo_maukkaasti_epaonnistuessa_myytyjen_maara_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttimaksu_syo_maukkaasti_onnistuessa_ei_muuta_rahaa_kassassa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.riittavasti_maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_korttimaksu_syo_maukkaasti_epaonnistuessa_ei_muuta_rahaa_kassassa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.alle_maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # rahan lataaminen kortille

    def test_lataa_rahaa_kortille_siirtaa_kortille_rahaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.riittavasti_maksukortti, 500)
        self.assertEqual(self.riittavasti_maksukortti.saldo, 1000)
    
    def test_lataa_rahaa_kortille_ei_siirra_negatiivista_summaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.riittavasti_maksukortti, -500)
        self.assertEqual(self.riittavasti_maksukortti.saldo, 500)
    
    def test_lataa_rahaa_kortille_onnistuessa_kasvattaa_kassassa_rahaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.riittavasti_maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_lataa_rahaa_kortille_epaonnistuessa_ei_kasvata_rahaa_kassassa(self):
        self.kassapaate.lataa_rahaa_kortille(self.riittavasti_maksukortti, -500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)