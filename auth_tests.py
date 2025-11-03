import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class AuthTestSuite(unittest.TestCase):

    frontend_host = "http://localhost"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=2)
        self.addCleanup(self.driver.quit)

    def close_toasts(self):
        toasts = self.driver.find_elements(By.CLASS_NAME, "chakra-alert")
        for toast in toasts:
            close_button = toast.find_element(
                By.XPATH, './/button[@aria-label="Close"]'
            )
            close_button.click()

    def get_and_maximize_window(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def login_as_admin(self):
        self.get_and_maximize_window(f"{self.frontend_host}/login")
        self.wait = WebDriverWait(self.driver, timeout=5)
        self.wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
        self.driver.find_element(By.ID, "input-email").send_keys("admin@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-1234")
        self.driver.find_element(By.ID, "btn-submit").click()
        self.wait.until(lambda _: "login" not in self.driver.current_url)

    def test_01_valid_login(self):
        self.get_and_maximize_window(f"{self.frontend_host}/login")

        self.driver.find_element(By.ID, "input-email").send_keys("admin@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-1234")
        self.driver.find_element(By.ID, "btn-submit").click()

        wait = WebDriverWait(self.driver, timeout=2)

        wait.until(lambda _: "login" not in self.driver.current_url)

        self.assertIn(
            "Inicio",
            self.driver.find_element(By.ID, "label-heading").text,
        )

    def test_02_invalid_login(self):
        self.get_and_maximize_window(f"{self.frontend_host}/login")

        self.driver.find_element(By.ID, "input-email").send_keys("admin@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-1235")
        self.driver.find_element(By.ID, "btn-submit").click()

        wait = WebDriverWait(self.driver, timeout=5)

        wait.until(EC.visibility_of_element_located((By.ID, "input-email-error")))

        self.assertIn(
            "Inicio de sesión inválido",
            self.driver.find_element(By.ID, "input-email-error").text,
        )

    def test_03_register(self):
        self.get_and_maximize_window(f"{self.frontend_host}/register")

        self.driver.find_element(By.ID, "input-email").send_keys("admin@mail.com")
        self.driver.find_element(By.ID, "input-firstname").send_keys("Student")
        self.driver.find_element(By.ID, "input-lastname").send_keys("Test")
        self.driver.find_element(By.ID, "button-continue-form").click()

        wait = WebDriverWait(self.driver, timeout=5)

        wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-4321")
        self.driver.find_element(By.ID, "input-confirm-password").send_keys(
            "Abcde-4321"
        )
        self.driver.find_element(By.ID, "button-submit").click()

        wait.until(EC.visibility_of_element_located((By.ID, "input-register-error")))
        self.assertIn(
            "El correo electrónico es inválido o ya se encuentra registrado en la plataforma",
            self.driver.find_element(By.ID, "input-register-error").text,
        )
        self.driver.find_element(By.ID, "input-email").clear()
        self.driver.find_element(By.ID, "input-email").send_keys("student@mail.com")

        self.driver.find_element(By.ID, "button-continue-form").click()
        wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
        self.driver.find_element(By.ID, "button-submit").click()

        wait.until(lambda _: "login" in self.driver.current_url)

        self.assertTrue(EC.visibility_of_element_located((By.ID, "image-logo-login")))

    def test_04_enablement(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/users")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")

        # Try to disable itself
        enablement_button = table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'admin@mail.com')]//td//button[starts-with(@id, 'enablement-')]",
        )
        enablement_button.click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "enablement-modal-button-confirm"))
        )
        enablement_modal_button_confirm = self.driver.find_element(
            By.ID, "enablement-modal-button-confirm"
        )

        enablement_modal_button_confirm.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-error-')]")
            )
        )

        toast = self.driver.find_elements(
            By.XPATH, "//div[contains(@id, 'toast-error-')]"
        )[0]

        self.assertIn(
            "No puedes modificar el atributo de activación sobre tí mismo",
            toast.text,
        )

        # Disable user

        enablement_button = table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'student@mail.com')]//td//button[starts-with(@id, 'enablement-')]",
        )
        enablement_button.click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "enablement-modal-button-confirm"))
        )
        enablement_modal_button_confirm = self.driver.find_element(
            By.ID, "enablement-modal-button-confirm"
        )

        enablement_modal_button_confirm.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'enablement-toast-success-')]")
            )
        )

        toast = self.driver.find_elements(
            By.XPATH, "//div[contains(@id, 'enablement-toast-success-')]"
        )[0]

        self.assertIn(
            "El usuario ha sido desactivado exitosamente",
            toast.text,
        )

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'enablement-toast-success-')]")
            )
        )

        # Enable user back

        enablement_button.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'enablement-toast-success-')]")
            )
        )

        toast = self.driver.find_elements(
            By.XPATH, "//div[contains(@id, 'enablement-toast-success-')]"
        )[0]

        self.assertIn(
            "El usuario ha sido activado exitosamente",
            toast.text,
        )

    def test_05_modify_user_data(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/users")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'student@mail.com')]",
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        # Editing user data
        Select(self.driver.find_element(By.ID, "select-role")).select_by_visible_text(
            "Profesor"
        )
        input_firstname = self.driver.find_element(By.ID, "input-firstname")
        input_firstname.clear()
        input_firstname.send_keys("Juan")

        input_lastname = self.driver.find_element(By.ID, "input-lastname")
        input_lastname.clear()
        input_lastname.send_keys("Diego")

        email_input = self.driver.find_element(By.ID, "input-email")
        email_input.clear()
        email_input.send_keys("teacher@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-4321")
        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'teacher@mail.com')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        # Checking changes made
        selected_option = Select(
            self.driver.find_element(By.ID, "select-role")
        ).first_selected_option
        self.assertEqual("Profesor", selected_option.text)

        self.assertEqual(
            "Juan",
            self.driver.find_element(By.ID, "input-firstname").get_attribute("value"),
        )
        self.assertEqual(
            "Diego",
            self.driver.find_element(By.ID, "input-lastname").get_attribute("value"),
        )
        self.assertEqual(
            "teacher@mail.com",
            self.driver.find_element(By.ID, "input-email").get_attribute("value"),
        )
        self.assertEqual(
            "", self.driver.find_element(By.ID, "input-password").get_attribute("value")
        )

    def test_06_admin_create_user(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/users")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        self.driver.find_element(By.ID, "button-add-item").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        # Add user
        Select(self.driver.find_element(By.ID, "select-role")).select_by_visible_text(
            "Administrador"
        )
        self.driver.find_element(By.ID, "input-firstname").send_keys("Francisco")
        self.driver.find_element(By.ID, "input-lastname").send_keys("José")
        email_input = self.driver.find_element(By.ID, "input-email")
        email_input.clear()
        email_input.send_keys("student@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-1234")
        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'student@mail.com')]",
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        # Check saved data
        selected_option = Select(
            self.driver.find_element(By.ID, "select-role")
        ).first_selected_option
        self.assertEqual("Administrador", selected_option.text)

        self.assertEqual(
            "Francisco",
            self.driver.find_element(By.ID, "input-firstname").get_attribute("value"),
        )
        self.assertEqual(
            "José",
            self.driver.find_element(By.ID, "input-lastname").get_attribute("value"),
        )
        self.assertEqual(
            "student@mail.com",
            self.driver.find_element(By.ID, "input-email").get_attribute("value"),
        )
        self.assertEqual(
            "", self.driver.find_element(By.ID, "input-password").get_attribute("value")
        )

    def test_07_delete_user(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/users")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        # Trying to delete itself

        delete_button = table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'admin@mail.com')]//td//button[starts-with(@id, 'delete-')]",
        )
        delete_button.click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "deletion-modal-button-confirm"))
        )
        deletion_modal_button_confirm = self.driver.find_element(
            By.ID, "deletion-modal-button-confirm"
        )

        deletion_modal_button_confirm.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-error-')]")
            )
        )

        toast = self.driver.find_elements(
            By.XPATH, "//div[contains(@id, 'toast-error-')]"
        )[0]

        self.assertIn(
            "No puedes borrarte a tí mismo por aquí",
            toast.text,
        )

        # Delete another user
        table_body = self.driver.find_element(By.ID, "table-body")

        delete_button = table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'student@mail.com')]//td//button[starts-with(@id, 'delete-')]",
        )

        delete_button.click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "deletion-modal-button-confirm"))
        )
        deletion_modal_button_confirm = self.driver.find_element(
            By.ID, "deletion-modal-button-confirm"
        )

        deletion_modal_button_confirm.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'deletion-toast-success-')]")
            )
        )

        toast = self.driver.find_elements(
            By.XPATH, "//div[contains(@id, 'deletion-toast-success-')]"
        )[0]

        self.assertIn(
            "El usuario ha sido borrado exitosamente",
            toast.text,
        )

    def test_08_change_profile_data(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/profile")
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))
        input_firstname = self.driver.find_element(By.ID, "input-firstname")
        input_firstname.clear()
        input_firstname.send_keys("John")
        input_lastname = self.driver.find_element(By.ID, "input-lastname")
        input_lastname.clear()
        input_lastname.send_keys("Doe")
        self.driver.find_element(By.ID, "button-submit").click()

        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))
        self.assertEqual(
            "John",
            self.driver.find_element(By.ID, "input-firstname").get_attribute("value"),
        )
        self.assertEqual(
            "Doe",
            self.driver.find_element(By.ID, "input-lastname").get_attribute("value"),
        )

        self.driver.find_element(By.ID, "button-change-password").click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "form-change-password"))
        )

        input_current_password = self.driver.find_element(
            By.ID, "input-current-password"
        )

        input_current_password.send_keys("Incorrect password")

        self.driver.find_element(By.ID, "input-new-password").send_keys("Abcde-1234")
        self.driver.find_element(By.ID, "input-confirm-new-password").send_keys(
            "Abcde-1234"
        )

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "input-current-password-error"))
        )

        self.assertEqual(
            "Contraseña actual incorrecta",
            self.driver.find_element(By.ID, "input-current-password-error").text,
        )
        input_current_password.clear()
        input_current_password.send_keys("Abcde-1234")

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-change-password-success')]")
            )
        )

        self.assertEqual(
            "Su contraseña ha sido actualizada exitosamente",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-change-password-success')]"
            ).text,
        )

    def login_as_teacher(self):
        self.get_and_maximize_window(f"{self.frontend_host}/login")
        self.wait = WebDriverWait(self.driver, timeout=5)
        self.wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
        self.driver.find_element(By.ID, "input-email").send_keys("teacher@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-4321")
        self.driver.find_element(By.ID, "btn-submit").click()
        self.wait.until(lambda _: "login" not in self.driver.current_url)

    def test_09_permissions_change(self):
        self.login_as_teacher()
        self.get_and_maximize_window(f"{self.frontend_host}/")
        self.wait.until(EC.visibility_of_element_located((By.ID, "layout-base")))

        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-users")) == 0)
        self.assertTrue(
            len(self.driver.find_elements(By.ID, "navlink-permissions")) == 0
        )
        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-roles")) == 0)

        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/")
        self.wait.until(EC.visibility_of_element_located((By.ID, "layout-base")))

        navlinks_permission = self.driver.find_elements(By.ID, "navlink-permissions")

        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-users")) > 0)
        self.assertTrue(len(navlinks_permission) > 0)
        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-roles")) > 0)

        navlinks_permission[0].click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "panel-permissions")))

        Select(self.driver.find_element(By.ID, "select-role")).select_by_visible_text(
            "Profesor"
        )

        panel_permissions = self.driver.find_element(By.ID, "panel-permissions")

        accordions = panel_permissions.find_elements(
            By.XPATH,
            "//button[contains(@id, 'accordion-button')]",
        )

        for a in accordions:
            a.click()

        panel_permissions.find_element(
            By.XPATH,
            "//tr[contains(., 'Puede gestionar todos los roles y los permisos asociados a ellos')]//label[contains(@class, 'chakra-checkbox')]",
        ).click()

        panel_permissions.find_element(
            By.XPATH,
            "//tr[contains(., 'Puede ver la información de todos los usuarios en la plataforma. Usado al momento de listarlos a todos y obtener información individual')]//label[contains(@class, 'chakra-checkbox')]",
        ).click()

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-update-permission-success-')]")
            )
        )

        self.assertEqual(
            "Los cambios fueron guardados",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-update-permission-success-')]"
            ).text,
        )

        self.login_as_teacher()

        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-users")) > 0)
        self.assertTrue(
            len(self.driver.find_elements(By.ID, "navlink-permissions")) > 0
        )
        self.assertTrue(len(self.driver.find_elements(By.ID, "navlink-roles")) > 0)

    def test_10_modify_roles(self):
        self.login_as_teacher()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/roles")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Administrador')]",
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-role")))

        form_role = self.driver.find_element(
            By.ID,
            "form-role",
        )

        input_name = form_role.find_element(By.ID, "input-name")
        input_name.clear()
        input_name.send_keys("Profesor")

        textarea_description = form_role.find_element(By.ID, "textarea-description")
        textarea_description.clear()
        textarea_description.send_keys("Descripción modificada")

        button_submit = self.driver.find_element(By.ID, "button-submit")

        button_submit.click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "input-name-error")))

        self.assertEqual(
            "Ya existe un rol con ese nombre",
            form_role.find_element(By.ID, "input-name-error").text,
        )

        input_name.clear()
        input_name.send_keys("Administrador")

        input_level = form_role.find_element(By.ID, "input-level")
        input_level.send_keys(Keys.BACKSPACE)
        input_level.send_keys(1)

        button_submit.click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "input-level-error")))

        self.assertEqual(
            "La jerarquía de roles nativos debe ser conservada",
            form_role.find_element(By.ID, "input-level-error").text,
        )

        input_level.send_keys(Keys.BACKSPACE)
        input_level.send_keys(4)

        button_submit.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-role-mutation-success')]")
            )
        )

        self.assertEqual(
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-role-mutation-success-')]"
            ).text,
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Profesor')]",
        ).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-role")))

        form_role = self.driver.find_element(
            By.ID,
            "form-role",
        )

        input_level = form_role.find_element(By.ID, "input-level")
        input_level.send_keys(Keys.BACKSPACE)
        input_level.send_keys(3)

        button_submit = self.driver.find_element(By.ID, "button-submit")

        button_submit.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-role-mutation-success')]")
            )
        )

        self.assertEqual(
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-role-mutation-success-')]"
            ).text,
        )

    def test_11_create_delete_roles(self):
        self.login_as_admin()
        self.get_and_maximize_window(f"{self.frontend_host}/controlpanel/roles")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        self.driver.find_element(By.ID, "button-add-item").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-role")))

        form_role = self.driver.find_element(
            By.ID,
            "form-role",
        )

        form_role.find_element(By.ID, "input-name").send_keys("Prueba")

        form_role.find_element(By.ID, "input-level").send_keys("1")

        form_role.find_element(By.ID, "textarea-description").send_keys("Rol de prueba")

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-role-mutation-success')]")
            )
        )

        self.assertEqual(
            "Rol creado",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-role-mutation-success-')]"
            ).text,
        )

        self.driver.find_element(By.ID, "navlink-users").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        self.driver.find_element(By.ID, "table-body").find_element(
            By.XPATH,
            f"//tr[contains(., 'teacher@mail.com')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        Select(self.driver.find_element(By.ID, "select-role")).select_by_visible_text(
            "Prueba"
        )

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-role-mutation-success')]")
            )
        )

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        self.driver.find_element(By.ID, "navlink-roles").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        self.driver.find_element(By.ID, "table-body").find_element(
            By.XPATH,
            f"//tr[contains(., 'Prueba')]//td//button[starts-with(@id, 'delete-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "button-modal-role-delete-confirm")
            )
        )
        self.driver.find_element(By.ID, "button-modal-role-delete-confirm").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-delete-error-')]")
            )
        )

        self.assertEqual(
            "No se pueden eliminar roles que tienen usuarios asignados",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-delete-error-')]"
            ).text,
        )

        self.driver.find_element(By.ID, "navlink-users").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//tr[contains(., 'teacher@mail.com')]",
                )
            )
        )
        self.driver.find_element(By.ID, "table-body").find_element(
            By.XPATH,
            f"//tr[contains(., 'teacher@mail.com')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-user")))

        Select(self.driver.find_element(By.ID, "select-role")).select_by_visible_text(
            "Profesor"
        )

        self.wait.until(
            lambda driver: all(
                not element.is_displayed()
                for element in driver.find_elements(
                    By.XPATH, "//div[contains(@id, 'toast-')]"
                )
            )
        )

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        self.driver.find_element(By.ID, "navlink-roles").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        self.driver.find_element(By.ID, "table-body").find_element(
            By.XPATH,
            f"//tr[contains(., 'Prueba')]//td//button[starts-with(@id, 'delete-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "button-modal-role-delete-confirm")
            )
        )
        self.driver.find_element(By.ID, "button-modal-role-delete-confirm").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-delete-success-')]")
            )
        )

        self.assertEqual(
            "El rol ha sido eliminado exitosamente",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-delete-success-')]"
            ).text,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
