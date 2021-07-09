# -*- coding: utf-8 -*-
import random
import time
import unittest
import allure
from src.functions.functions import Functions as Selenium
import HtmlTestRunner

@allure.feature(u'Carga de documentos')
@allure.testcase(u'[Flujo carga Doc] Crear un flujo')
@allure.severity(allure.severity_level.NORMAL)
@allure.description(u"""validaciones: </br>
Comportamiento del ultimo modal tras crear el flujo</br></br>""")

class test_flow_009(Selenium, unittest.TestCase):

    def setUp(self):
        with allure.step(u'PASO 1 : Ingresar al navegador'):
            Selenium.open_browser(self, navegador="CHROME")
            self.dataRoles = ['felipe.bravo', 'juan.suaza', 'dvalero84', 'nadia.gallardo'] #USUARIOS PARA EL FLUJO
            self.dataComentario = ['Hola necesitamos que en conjunto pongamos mas de nuestra parte', 'No tengo ningun comentario',
                                   'Por favor poner ojo con esto', 'Te asigne un par de días', 'Necesito aprobación de esto lo antes posible',
                                   'Estamos haciendo unas pruebas', 'Estos son test', 'Comentarios de pruebas', 'Es necesario aprobar esto ahora',
                                   'Genial aprobación']

    @allure.title(u'Crear un flujo')
    @allure.story(u'Validar el comportamiento al crear un flujo he interactuar con el ultimo modal..')
    def test_create_flow(self):
        with allure.step(u'PASO 2 : Ingresar con el usuario Admin'):
            usuario = ['juan.suaza', 'nadia.gallardo', 'felipe.bravo', 'dvalero84'] #USUARIOS PARA INICIAR SESIÓN
            nomUser = random.choice(usuario) #'nadia.gallardo'
            Selenium.get_signin_administrator(self, nomUser) #Cambiar el usuario colocar alguno diferente del admin

        with allure.step(u'PASO 3 : Rellenar formulario'):
            names = Selenium.carga_doc_controlado(self)
            names

        with allure.step(u'PASO 4 : Realizar el llenado y validaciones.'):
            Selenium.get_json_file(self, "flujoCargaDocumento")
            campos = ['Input nombre', 'Input dias', 'Input comentario']
            roles = ['owner', 'CoAuthor', 'Stakeholder', 'Reviewed', 'Approved', 'released']
            for x in range(6):
                x += 1
                Selenium.check_element(self, f"button {x}")
                Selenium.check_visibility_element_located(self, f"button {x}")
                self.driver.execute_script('arguments[0].scrollIntoView(true);', Selenium.get_elements(self, f"button {x}"))
                if x > 1 and x < 6:
                    Selenium.check_visibility_element_located(self, f"button {x}")
                    Selenium.get_elements(self, f"button {x}").click()
                    if x == 6:
                        Selenium.foto(self, "Botones")

            for a in range(6):
                for b in range(3):
                    check = Selenium.check_element(self, campos[b] + " " + roles[a])
                    assert check == True, f"Error, no se encontro el {campos[b]}" f"{roles[a]}"
                    if a >= 0 and a <= 5 and not b == 2:
                        Selenium.get_elements(self, 'Button Siguiente').click()
                        check = Selenium.check_exists_by_xpath(self, "//p[contains(text(), 'Campo requerido')]")
                        if check == False:
                            Selenium.foto(self, "Campos requeridos")
                            assert check == True, f"Error el campo {campos[b]} {roles[a]}, no tiene la validacion 'Campos requeridos'"
                    if b == 0:
                        rol = random.choice(self.dataRoles)
                        if b == 0 and a == 0:
                            while rol == nomUser:
                                rol = random.choice(self.dataRoles)
                        Selenium.get_elements(self, campos[b] + " " + roles[a]).send_keys(rol)
                        time.sleep(0.5)
                        Selenium.send_especific_keys(self, campos[b] + " " + roles[a], "Enter")
                    if b == 1:
                        Selenium.get_elements(self, campos[b] + " " + roles[a]).send_keys(random.randint(1,99))
                    if b == 2:
                        Selenium.get_elements(self, campos[b] + " " + roles[a]).send_keys(random.choice(self.dataComentario))
            Selenium.get_elements(self, "textbox").send_keys(random.choice(self.dataComentario))
            enabled = Selenium.get_elements(self, 'Button Siguiente').is_enabled()
            if enabled == False:
                Selenium.foto(self, "Boton siguiente bloqueado")
                assert enabled == True, "El boton siguiente al parecer esta bloqueado"
            Selenium.get_elements(self, 'Button Siguiente').click()

            #################time.sleep(99*99)#################

            Selenium.check_element(self, "confirmar")
            Selenium.foto(self, "Modal resumen")
            Selenium.get_elements(self, "confirmar").click()

            #############VALIDANDO EL COMPORTAMIENTO DEL ULTIMO MODAL###############
            Selenium.check_element(self, "button Ok")
            Selenium.foto(self, "button Ok")
            ul = self.driver.find_element_by_xpath("//div[@id='swal2-content']").text
            id = Selenium.split(self, ul, " ")
            Selenium.get_elements(self, "button Ok").click()

            check = Selenium.check_exists_by_xpath(self, "//h3[contains(text(),'Gestión de documentos')]")
            if check == False:
                Selenium.foto(self, "Gestion de documentos")
                assert check == True, "ERROR, no se encuentra el titulo 'Gestión de documentos' "

            Selenium.get_json_file(self, "notification")
            Selenium.check_element(self, "Button")
            Selenium.get_elements(self, "Button").click()

            Selenium.foto(self, "Notificación con el id"+id[2])
            xpath = f"//p[contains(text(),'{id[2]}')]"
            checkID = Selenium.check_exists_by_xpath(self, xpath)
            if checkID == False:
                assert checkID == True, f"Error no se encuentra el id '{id[2]}' en la notificación"
            self.driver.find_element_by_xpath(xpath).click()

    def tearDown(self):
        Selenium.tearDown(self)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='report'))