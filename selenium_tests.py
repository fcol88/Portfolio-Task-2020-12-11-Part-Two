from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import unittest

class Test_List_View(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    # When viewing the list page, the page title is Task list
    def test_list_view_title_is_correct_when_visiting_list_page(self):
        
        self.driver.get("http://127.0.0.1:5000")

        self.assertIn("Task list", self.driver.title)

        self.driver.get("http://127.0.0.1:5000/tasklist")

        self.assertIn("Task list", self.driver.title)

    # When clicking the add task button from the list page, 
    # the browser redirects to the add task form
    def test_list_view_add_task_redirects_to_task_form(self):

        self.driver.get("http://127.0.0.1:5000")
        addTaskButton = self.driver.find_element_by_id('addTask')
        addTaskButton.click()

        self.assertIn("Add task", self.driver.title)


    # When submitting the add task form without any data,
    # the user sees some feedback on how to fix the problem
    def test_add_task_form_redirects_to_task_form_with_message_when_invalid(self):

        self.driver.get("http://127.0.0.1:5000/addtask")
        saveTaskButton = self.driver.find_element_by_id("saveTask")
        saveTaskButton.click()

        errorPaneExists = True

        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            errorPaneExists = False

        self.assertTrue(errorPaneExists)

    # When the user saves a task with all the correct information,
    # they're redirected to the task list and the new task is shown
    def test_add_task_form_saves_task_when_user_enters_correct_info(self):

        self.driver.get("http://127.0.0.1:5000/")
        
        taskCount = len(self.driver.find_elements_by_xpath("//table[@id='taskList']/tbody/tr"))

        self.driver.get("http://127.0.0.1:5000/addtask")
        description = self.driver.find_element_by_id("description")
        description.send_keys("A description")
        user = Select(self.driver.find_element_by_id("user"))
        user.select_by_value("1")
        pin = self.driver.find_element_by_id("pin")
        pin.send_keys("1234")
        saveTaskButton = self.driver.find_element_by_id("saveTask")
        saveTaskButton.click()
        newTaskCount = len(self.driver.find_elements_by_xpath("//table[@id='taskList']/tbody/tr"))

        self.assertIn("Task list", self.driver.title)
        self.assertEqual(taskCount + 1, newTaskCount)

    # When the user clicks the add user button, 
    # the browser redirects to the user form
    def test_list_view_add_task_redirects_to_user_form(self):

        self.driver.get("http://127.0.0.1:5000/")
        addUserButton = self.driver.find_element_by_id("addUser")
        addUserButton.click()

        self.assertIn("Add user", self.driver.title)

    # When submitting the add user form without any data,
    # the user sees some feedback on how to fix the problem
    def test_add_user_form_redirects_to_user_form_with_message_when_invalid(self):

        self.driver.get("http://127.0.0.1:5000/adduser")
        saveUserButton = self.driver.find_element_by_id("saveUser")
        saveUserButton.click()

        errorPaneExists = True

        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            errorPaneExists = False

        self.assertTrue(errorPaneExists)

    # When submitting the add user form with all the correct info,
    # they're redirected to the task list
    def test_add_user_form_saves_task_when_user_enters_correct_info(self):

        self.driver.get("http://127.0.0.1:5000/adduser")
        firstName = self.driver.find_element_by_id("firstName")
        firstName.send_keys("First")
        lastName = self.driver.find_element_by_id("lastName")
        lastName.send_keys("Last")
        pin = self.driver.find_element_by_id("pin")
        pin.send_keys("1234")
        saveUserButton = self.driver.find_element_by_id("saveUser")
        saveUserButton.click()

        self.assertIn("Task list", self.driver.title)

    # When a user marks a task as complete, 
    # they're redirected to the task list and
    # it's not shown on the task list anymore
    def test_complete_task_completes_task(self):

        self.test_add_task_form_saves_task_when_user_enters_correct_info()
        taskCount = len(self.driver.find_elements_by_xpath("//table[@id='taskList']/tbody/tr"))
        completeTaskButton = self.driver.find_element_by_id("completeLink" + str(taskCount))
        completeTaskButton.click()
        newTaskCount = len(self.driver.find_elements_by_xpath("//table[@id='taskList']/tbody/tr"))

        self.assertIn("Task list", self.driver.title)
        self.assertEqual(taskCount - 1, newTaskCount)


if __name__ == "__main__":
    unittest.main()