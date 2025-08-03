import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import time


class ResourcesTestSuite(unittest.TestCase):
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

    def test_01_create_course(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-course")))
        self.driver.find_element(By.ID, "input-name").send_keys("Test Course 1")
        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description of test course 1"
        )

        image_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "custom_resource_img.png")
        )

        input_file = self.driver.find_element(By.ID, "input-file")

        ActionChains(self.driver).move_to_element(input_file).click().perform()

        input_file.send_keys(image_file)

        self.driver.find_element(By.ID, "submit-button").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-course-mutation-success-')]")
            )
        )

        self.assertEqual(
            "Curso creado",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-course-mutation-success-')]"
            ).text,
        )

    def test_02_create_category(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/coursecategories"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "course-category-form"))
        )

        self.driver.find_element(By.ID, "input-name").send_keys(
            "Test Course Category 1"
        )
        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description of test course category 1"
        )

        self.driver.find_element(By.ID, "submit-button").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'toast-course-category-mutation-success-')]",
                )
            )
        )

        self.assertEqual(
            "Categoría de curso creada",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-course-category-mutation-success-')]",
            ).text,
        )

    def test_03_edit_category(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/coursecategories"
        )
        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course Category 1')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "course-category-form"))
        )

        input_name = self.driver.find_element(By.ID, "input-name")
        input_name.clear()
        input_name.send_keys("Edited Test Course Category 1")

        input_description = self.driver.find_element(By.ID, "input-description")
        input_description.clear()
        input_description.send_keys("Edited Description of test course category 1")
        self.driver.find_element(By.ID, "submit-button").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'toast-course-category-mutation-success-')]",
                )
            )
        )

        self.assertEqual(
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-course-category-mutation-success-')]",
            ).text,
        )

    def test_04_edit_course(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course 1')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "form-course")))
        input_name = self.driver.find_element(By.ID, "input-name")
        input_name.clear()
        input_name.send_keys("Edited Test Course 1")
        input_description = self.driver.find_element(By.ID, "input-description")
        input_description.clear()
        input_description.send_keys("Edited Description of test course 1")
        Select(
            self.driver.find_element(By.ID, "select-course-category")
        ).select_by_visible_text("Edited Test Course Category 1")

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
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-course-mutation-success-')]",
            ).text,
        )

        self.get_and_maximize_window("http://localhost:5173/explore/courses")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'course-card-')]")
            )
        )

        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'button-disable-course-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "button-disable-course-confirm"))
        )

        self.driver.find_element(By.ID, "button-disable-course-confirm").click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'button-disable-course-')]",
                )
            )
        )

        self.get_and_maximize_window("http://localhost:5173/explore/courses")

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'course-card-')]")
            )
        )

        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'button-enable-course-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'button-enable-course-')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'button-enable-course-')]",
                )
            )
        )

    def test_05_try_deleting_used_course_category(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/coursecategories"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Edited Test Course Category 1')]//td//button[starts-with(@id, 'delete-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "deletion-modal-button-confirm"))
        )
        self.driver.find_element(By.ID, "deletion-modal-button-confirm").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'deletion-toast-error-')]",
                )
            )
        )
        self.assertEqual(
            "La categoría de curso se encuentra actualmente en uso",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'deletion-toast-error-')]",
            ).text,
        )

    def test_06_edit_course_content(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'edit-content-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "sections-container")))
        sections_container = self.driver.find_element(By.ID, "sections-container")

        add_course_section_form = sections_container.find_element(
            By.XPATH,
            "//*[contains(@id , 'add-course-section')]",
        )
        add_course_section_form.find_element(
            By.ID, "add-course-section-input"
        ).send_keys("New section")
        add_course_section_form.find_element(
            By.ID, "add-course-section-submit-button"
        ).click()

        # Check if new section was created
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='sections-container']//span[contains(., 'New section')]",
                )
            )
        )

        section = sections_container.find_element(
            By.XPATH,
            "//*[contains(@id , 'course-section-id-')]",
        )

        section.find_element(
            By.XPATH,
            "//*[contains(@id , 'button-add-activity-')]",
        ).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "lesson-form")))

        self.driver.find_element(By.ID, "input-name").send_keys("Test name for lesson")

        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description for test name for lesson"
        )

        lesson_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "lesson_document_file.pdf")
        )

        input_file = self.driver.find_element(By.ID, "input-file")

        ActionChains(self.driver).move_to_element(input_file).click().perform()

        input_file.send_keys(lesson_file)

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'toast-lesson-mutation-success-')]",
                )
            )
        )

        self.assertEqual(
            "Lección de curso creada",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-lesson-mutation-success-')]",
            ).text,
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'sections-container')]",
                )
            )
        )

        sections_container = self.driver.find_element(By.ID, "sections-container")

        section = sections_container.find_element(
            By.XPATH,
            "//*[contains(@id , 'course-section-id-')]",
        )

        activity = section.find_element(
            By.XPATH, "//div[contains(@id, 'element-activity-')]"
        )

        activity.find_element(
            By.XPATH, "//button[contains(@id, 'delete-activity-button-')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@id, 'delete-activity-confirm-button-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH, "//button[contains(@id, 'delete-activity-confirm-button-')]"
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@id, 'element-activity-')]",
                )
            )
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'collapse-section-options-button-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'collapse-section-options-button-')]"
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'delete-section-button-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'delete-section-button-')]"
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'delete-section-button-')]",
                )
            )
        )

    def test_07_create_formation_line(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/formationlines"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "formation-line-form"))
        )

        self.driver.find_element(By.ID, "input-name").send_keys(
            "Formation line for testing"
        )

        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description for formation line for testing"
        )

        self.driver.find_element(By.ID, "input-search-course").send_keys("Edited")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'table-data-searched-courses-')]",
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//*[contains(@id, 'table-data-searched-courses-')]",
        ).click()

        image_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "custom_resource_img.png")
        )

        input_file = self.driver.find_element(By.ID, "input-file")

        ActionChains(self.driver).move_to_element(input_file).click().perform()

        input_file.send_keys(image_file)

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-formation-line-mutation-')]",
                )
            )
        )

        self.assertEqual(
            "Camino de aprendizaje creada",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-formation-line-mutation-')]",
            ).text,
        )

    def test_08_edit_formation_line(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/formationlines"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Formation line for testing')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "formation-line-form"))
        )

        input_name = self.driver.find_element(By.ID, "input-name")

        input_name.clear()

        input_name.send_keys("Change for formation line for testing")

        input_description = self.driver.find_element(By.ID, "input-description")

        input_description.clear()
        input_description.send_keys(
            "Change for description for formation line for testing"
        )

        self.driver.find_element(By.ID, "button-submit").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-formation-line-mutation-')]",
                )
            )
        )

        self.assertEqual(
            "Cambios guardados",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-formation-line-mutation-')]",
            ).text,
        )

        self.get_and_maximize_window("http://localhost:5173/explore/formation-lines")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'formation-line-card-')]")
            )
        )

        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/formationlines"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-disable-formation-line-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "button-disable-formation-line-confirm")
            )
        )

        self.driver.find_element(By.ID, "button-disable-formation-line-confirm").click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-disable-formation-line-')]",
                )
            )
        )

        self.get_and_maximize_window("http://localhost:5173/explore/formation-lines")

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@id, 'formation-line-card-')]")
            )
        )

        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/formationlines"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-enable-formation-line-')]",
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-enable-formation-line-')]",
                )
            )
        )

    def test_09_try_deleting_used_course(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Edited Test Course 1')]//td//button[starts-with(@id, 'delete-course-button-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'button-delete-course-confirm')]",
                )
            )
        )

        self.driver.find_element(By.ID, "button-delete-course-confirm").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'toast-delete-used-course-error-')]",
                )
            )
        )

        self.assertEqual(
            "El curso está asociado a una línea de formación",
            self.driver.find_element(
                By.XPATH,
                "//div[contains(@id, 'toast-delete-used-course-error-')]",
            ).text,
        )

    def test_10_delete_formation_line(self):
        self.login_as_admin()
        self.get_and_maximize_window(
            "http://localhost:5173/controlpanel/formationlines"
        )

        self.wait.until(EC.visibility_of_element_located((By.ID, "table-body")))
        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-delete-formation-line-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'button-delete-formation-line-confirm')]",
                )
            )
        )

        self.driver.find_element(By.ID, "button-delete-formation-line-confirm").click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    f"//tr[contains(., 'Change for formation line for testing')]//td//button[starts-with(@id, 'button-delete-formation-line-')]",
                )
            )
        )

    def test_11_delete_course(self):
        self.login_as_admin()
        self.get_and_maximize_window("http://localhost:5173/controlpanel/courses")

        self.wait.until(EC.visibility_of_element_located((By.ID, "button-add-item")))

        self.driver.find_element(By.ID, "button-add-item").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "form-course")))
        self.driver.find_element(By.ID, "input-name").send_keys("Test Course 2")
        self.driver.find_element(By.ID, "input-description").send_keys(
            "Description of test course 2"
        )

        self.driver.find_element(By.ID, "submit-button").click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@id, 'toast-course-mutation-success-')]")
            )
        )

        self.assertEqual(
            "Curso creado",
            self.driver.find_element(
                By.XPATH, "//div[contains(@id, 'toast-course-mutation-success-')]"
            ).text,
        )

        table_body = self.driver.find_element(By.ID, "table-body")
        table_body.find_element(
            By.XPATH,
            f"//tr[contains(., 'Test Course 2')]//td//button[starts-with(@id, 'delete-course-button-')]",
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@id, 'button-delete-course-confirm')]",
                )
            )
        )

        self.driver.find_element(By.ID, "button-delete-course-confirm").click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(., 'Test Course 2')]",
                )
            )
        )


if __name__ == "__main__":

    unittest.main(verbosity=2)
