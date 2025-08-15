import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import requests


class CompetenciesTestSuite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=2)
        self.addCleanup(self.driver.quit)

    def get_and_maximize_window(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def login_as_admin(self):
        self.get_and_maximize_window("http://localhost:5173/login")
        self.wait = WebDriverWait(self.driver, timeout=5)
        self.wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
        self.driver.find_element(By.ID, "input-email").send_keys("admin@mail.com")
        self.driver.find_element(By.ID, "input-password").send_keys("Abcde-1234")
        self.driver.find_element(By.ID, "btn-submit").click()
        self.wait.until(lambda _: "login" not in self.driver.current_url)

    def test_01_create_competency(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/competencies")

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-competency")))

        self.driver.find_element(By.ID, "input-description").send_keys(
            "Competency Test 1"
        )

        Select(
            self.driver.find_element(By.ID, "select-bloom-taxonomy-level")
        ).select_by_visible_text("4")

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'toast-competency-mutation-succeed-')]")
            )
        )

        self.assertEqual(
            "Competencia creada",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-competency-mutation-succeed-')]",
            ).text,
        )

    def test_02_edit_competency(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/competencies")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Competency Test 1')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-competency")))

        input_description = self.driver.find_element(By.ID, "input-description")
        input_description.clear()
        input_description.send_keys("Change competency Test 1")

        Select(
            self.driver.find_element(By.ID, "select-bloom-taxonomy-level")
        ).select_by_visible_text("5")

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'toast-competency-mutation-succeed-')]")
            )
        )

        self.assertEqual(
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-competency-mutation-succeed-')]",
            ).text,
        )

    def test_03_add_competency_to_course(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-course")))
        self.driver.find_element(By.ID, "input-name").send_keys(
            "Test Course for competencies"
        )
        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description of test course for competencies"
        )

        self.driver.find_element(By.ID, "submit-button").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'toast-course-mutation-success-')]",
                )
            )
        )

        self.assertEqual(
            "Curso creado",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-course-mutation-success-')]",
            ).text,
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "select-competency")))

        Select(
            self.driver.find_element(By.ID, "select-competency")
        ).select_by_visible_text("Change competency Test 1")

        self.driver.find_element(By.ID, "button-add-existing-competency").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(., 'Change competency Test 1')]",
                )
            )
        )

    def test_04_add_learning_output_to_competency(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "select-competency")))

        self.driver.find_element(
            By.XPATH,
            f"//button[starts-with(@id, 'button-add-learning-output-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@class, 'input-learning-output-description')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            f"//*[contains(@class, 'input-learning-output-description')]",
        ).send_keys("Test Learning Output 1")

        Select(
            self.driver.find_element(
                By.XPATH,
                f"//select[contains(@class, 'select-learning-output-bloom-taxonomy-level')]",
            )
        ).select_by_visible_text("4")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-submit-learning-output-form')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-submit-learning-output-form')]",
        ).click()

        # form-learning-output
        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//form[contains(@class, 'form-learning-output')]",
                )
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(., 'Test Learning Output 1')]",
                )
            )
        )

    def test_05_add_performance_indicator_to_learning_output(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "select-competency")))

        self.driver.find_element(
            By.XPATH,
            f"//p[contains(., 'Change competency Test 1')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'button-add-performance-indicator-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            f"//button[starts-with(@id, 'button-add-performance-indicator-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@class, 'input-performance-indicator-description')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            f"//*[contains(@class, 'input-performance-indicator-description')]",
        ).send_keys("Test Performance Indicator 1")

        Select(
            self.driver.find_element(
                By.XPATH,
                f"//select[contains(@class, 'select-performance-indicator-bloom-taxonomy-level')]",
            )
        ).select_by_visible_text("3")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'button-submit-performance-indicator-form')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'button-submit-performance-indicator-form')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//form[contains(@class, 'form-performance-indicator')]",
                )
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(., 'Test Performance Indicator 1')]",
                )
            )
        )

    def test_06_edit_competencies_tree(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "select-competency")))

        # Editing learning output

        self.driver.find_element(
            By.XPATH,
            f"//p[contains(., 'Change competency Test 1')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-edit-learning-output-')]",
                )
            )
        )

        # Open learning output edit form

        self.driver.find_element(
            By.XPATH,
            f"//button[contains(@id, 'button-edit-learning-output-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@class, 'input-learning-output-description')]",
                )
            )
        )

        Select(
            self.driver.find_element(
                By.XPATH,
                f"//select[contains(@class, 'select-learning-output-bloom-taxonomy-level')]",
            )
        ).select_by_visible_text("1")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-submit-learning-output-form')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-submit-learning-output-form')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-level-error-')]",
                )
            )
        )

        self.assertEqual(
            "El nivel del resultado de aprendizaje no puede ser menor que el de sus componentes hijos",
            self.driver.find_element(
                By.XPATH,
                "//*[contains(@id, 'toast-level-error-')]",
            ).text,
        )

        self.driver.find_element(
            By.XPATH,
            "//*[contains(@id, 'toast-level-error-')]//button",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-level-error-')]",
                )
            )
        )

        # Open learning output edit form

        self.driver.find_element(
            By.XPATH,
            f"//button[contains(@id, 'button-edit-learning-output-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@class, 'input-learning-output-description')]",
                )
            )
        )

        input_learning_output = self.driver.find_element(
            By.XPATH,
            f"//*[contains(@class, 'input-learning-output-description')]",
        )

        input_learning_output.clear()

        input_learning_output.send_keys("Change Test Learning Output 1")

        Select(
            self.driver.find_element(
                By.XPATH,
                f"//select[contains(@class, 'select-learning-output-bloom-taxonomy-level')]",
            )
        ).select_by_visible_text("5")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-submit-learning-output-form')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-submit-learning-output-form')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//form[contains(@class, 'form-learning-output')]",
                )
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(., 'Change Test Learning Output 1')]",
                )
            )
        )
        # Editing Performance Indicator

        self.driver.find_element(
            By.XPATH,
            f"//p[contains(., 'Change Test Learning Output 1')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-edit-performance-indicator-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            f"//button[contains(@id, 'button-edit-performance-indicator-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@class, 'input-performance-indicator-description')]",
                )
            )
        )

        input_performance_indicator = self.driver.find_element(
            By.XPATH,
            f"//*[contains(@class, 'input-performance-indicator-description')]",
        )

        input_performance_indicator.clear()

        input_performance_indicator.send_keys("Change Test Performance Indicator 1")

        Select(
            self.driver.find_element(
                By.XPATH,
                f"//select[contains(@class, 'select-performance-indicator-bloom-taxonomy-level')]",
            )
        ).select_by_visible_text("4")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'button-submit-performance-indicator-form')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'button-submit-performance-indicator-form')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//form[contains(@class, 'form-performance-indicator')]",
                )
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(., 'Change Test Performance Indicator 1')]",
                )
            )
        )

    def test_07_edit_competency_level_from_management_view(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/competencies")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Change competency Test 1')]",
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "form-competency",
                )
            )
        )

        Select(
            self.driver.find_element(By.ID, "select-bloom-taxonomy-level")
        ).select_by_visible_text("4")

        self.driver.find_element(
            By.ID,
            "button-submit",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-competency-mutation-error-')]",
                )
            )
        )

        self.assertEqual(
            "La competencia tiene un resultado de aprendizaje con un nivel superior al asignado asociado",
            self.driver.find_element(
                By.XPATH,
                "//*[contains(@id, 'toast-competency-mutation-error-')]",
            ).text,
        )

        self.driver.find_element(
            By.XPATH,
            "//*[contains(@id, 'toast-competency-mutation-error-')]//button",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-competency-mutation-error-')]",
                )
            )
        )

    def test_08_associate_performance_indicator_to_activity(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'edit-content-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "sections-container")))
        sections_container = self.driver.find_element(By.ID, "sections-container")

        section = sections_container.find_element(
            By.XPATH,
            "//*[contains(@id , 'course-section-id-')]",
        )

        Select(
            section.find_element(
                By.XPATH,
                "//*[contains(@id , 'select-activity-type-')]",
            )
        ).select_by_visible_text("Actividad evaluativa")

        section.find_element(
            By.XPATH,
            "//*[contains(@id , 'button-add-activity-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "form-evaluative-activity"))
        )
        self.driver.find_element(
            By.ID,
            "input-name",
        ).send_keys("Test Evaluative Activity 1")

        self.driver.find_element(
            By.ID,
            "input-description",
        ).send_keys("Test Evaluative Activity 1 Description")

        Select(
            self.driver.find_element(
                By.ID,
                "select-grading-method",
            )
        ).select_by_value("average")

        Select(
            self.driver.find_element(
                By.ID,
                "select-performance-indicators",
            )
        ).select_by_visible_text("1.1.1 - Change Test Performance Indicator 1")

        Select(
            self.driver.find_element(
                By.ID,
                "select-performance-indicators",
            )
        ).select_by_visible_text("1.1.1 - Change Test Performance Indicator 1")

        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(By.ID, "switch-enable-max-attempts"),
        )

        self.driver.execute_script("window.scrollBy(0, 1000);")

        self.wait.until(EC.element_to_be_clickable((By.ID, "input-max-attempts")))

        self.driver.find_element(
            By.ID,
            "input-max-attempts",
        ).send_keys("3")

        self.driver.find_element(
            By.ID,
            "input-grading-criteria-description",
        ).send_keys("Test Grading Criteria Item 1")

        self.driver.find_element(
            By.ID,
            "input-grading-criteria-percentage",
        ).send_keys("100")

        self.driver.find_element(
            By.ID,
            "button-add-grading-criteria-item",
        ).click()

        self.driver.find_element(
            By.ID,
            "button-submit",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-evaluative-activity-mutation-')]",
                )
            )
        )

        self.assertEqual(
            self.driver.find_element(
                By.XPATH,
                "//*[contains(@id, 'toast-evaluative-activity-mutation-')]",
            ).text,
            "Actividad evaluativa creada",
        )

    def test_09_edit_evaluative_activity(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'edit-content-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "sections-container")))

        self.driver.find_element(
            By.XPATH, "//p[contains(., 'Test Evaluative Activity 1')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "form-evaluative-activity"))
        )

        input_name = self.driver.find_element(
            By.ID,
            "input-name",
        )
        input_name.clear()
        input_name.send_keys("Change Test Evaluative Activity 1")

        input_description = self.driver.find_element(
            By.ID,
            "input-description",
        )

        input_description.clear()
        input_description.send_keys("Change Test Evaluative Activity 1")

        Select(
            self.driver.find_element(
                By.ID,
                "select-grading-method",
            )
        ).select_by_value("best")

        self.driver.find_element(
            By.ID,
            "button-submit",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-evaluative-activity-mutation-')]",
                )
            )
        )

        self.assertEqual(
            self.driver.find_element(
                By.XPATH,
                "//*[contains(@id, 'toast-evaluative-activity-mutation-')]",
            ).text,
            "Cambios guardados",
        )

    def test_10_upload_grade(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/explore/courses")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'course-card-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//div[contains(@id, 'course-card-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-view-course')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-view-course')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "button-register-course"))
        )

        self.driver.find_element(By.ID, "button-register-course").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'toast-register-mutation-success-')]")
            )
        )

        success_toast = self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'toast-register-mutation-success-')]"
        )

        self.assertEqual(success_toast.text, "Te has registrado en el curso")

        self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'toast-register-mutation-success-')]//button"
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'toast-register-mutation-success-')]")
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//div[contains(@id, 'container-tabs')]//button[contains(., 'Contenido')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(., 'Change Test Evaluative Activity 1')]")
            )
        )

        self.driver.find_element(
            By.XPATH, "//p[contains(., 'Change Test Evaluative Activity 1')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "button-create-token"))
        )

        prev_token = ""
        if len(self.driver.find_elements(By.ID, "text-token")) > 0:
            prev_token = self.driver.find_element(By.ID, "text-token").text

        self.driver.find_element(By.ID, "button-create-token").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "text-token")))

        self.wait.until(
            lambda _: self.driver.find_element(By.ID, "text-token").text != prev_token
        )

        token = self.driver.find_element(By.ID, "text-token").text

        request_error = True

        try:
            response = requests.put(
                "http://localhost/competencies/control-panel/activity-attempt/update/",
                json={
                    "token": {"PIN": token},
                    "evaluaciones": [
                        {
                            "index": 1,
                            "name": "Test Grading Criteria Item 1",
                            "percentage_grade": 100,
                        },
                        {"index": 2, "name": "Final grade", "percentage_grade": 100},
                    ],
                },
            )
            if response.status_code == 200:
                request_error = False

        except Exception as e:
            print(e)

        self.driver.implicitly_wait(3)

        self.assertFalse(request_error)

        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'edit-content-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "sections-container")))

        self.driver.find_element(
            By.XPATH, "//p[contains(., 'Test Evaluative Activity 1')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "form-evaluative-activity"))
        )

        self.assertTrue(
            len(self.driver.find_elements(By.ID, "text-attempted-warning")) > 0
        )

    def test_11_try_deleting_used_competency(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/competencies")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")

        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Change competency Test 1')]//button[contains(@id, 'button-delete-competency-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "button-delete-confirm"))
        )

        self.driver.find_element(
            By.ID,
            "button-delete-confirm",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'toast-delete-error-')]")
            )
        )

        self.assertIn(
            "La competencia es padre del indicador de logro",
            self.driver.find_element(
                By.XPATH,
                "//*[contains(@id, 'toast-delete-error-')]",
            ).text,
        )

    def test_12_deleting_evaluative_activity(self):

        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'edit-content-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@id, 'delete-activity-button-')]")
            )
        )

        self.driver.find_element(
            By.XPATH, "//button[contains(@id, 'delete-activity-button-')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@id, 'delete-activity-confirm-button-')]")
            )
        )

        self.driver.find_element(
            By.XPATH, "//button[contains(@id, 'delete-activity-confirm-button-')]"
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//button[contains(@id, 'delete-activity-button-')]")
            )
        )

    def test_13_deleting_performance_indicator(self):

        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "select-competency")))

        self.driver.find_element(
            By.XPATH, "//p[contains(., 'Change competency Test 1')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(., 'Change Test Learning Output 1')]")
            )
        )

        # self.driver.find_element(
        #     By.XPATH, "*[contains(., 'Change Test Learning Output 1')]"
        # ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-delete-performance-indicator-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-delete-performance-indicator-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-confirm-delete-performance-indicator-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-confirm-delete-performance-indicator-')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-delete-performance-indicator-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-delete-learning-output-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-confirm-delete-learning-output-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-confirm-delete-learning-output-')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-delete-learning-output-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-remove-competency-from-course-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-confirm-remove-competency-from-course-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@id, 'button-confirm-remove-competency-from-course-')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'button-remove-competency-from-course-')]",
                )
            )
        )

    def test_14_creating_competency_directly_into_course(self):

        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course for competencies')]//td//button[starts-with(@id, 'hierarchy-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "button-create-competency"))
        )

        self.driver.find_element(By.ID, "button-create-competency").click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-competency")))

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'button-submit-competency')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH, "//textarea[contains(@class, 'input-description-competency')]"
        ).send_keys("Competency test 2")

        Select(
            self.driver.find_element(
                By.XPATH,
                "//select[contains(@class, 'select-bloom-taxonomy-level-competency')]",
            )
        ).select_by_visible_text("4")

        self.driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'button-submit-competency')]",
        ).click()

        self.wait.until(EC.invisibility_of_element_located((By.ID, "form-competency")))

        self.assertTrue(
            len(
                self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(., 'Competency test 2')]",
                )
            )
            > 0
        )


if __name__ == "__main__":

    unittest.main(verbosity=2)
