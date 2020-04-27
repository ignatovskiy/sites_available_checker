import unittest
import script as target_script


class ScriptTests(unittest.TestCase):
    def test_getting_urls(self):
        test = target_script.get_url_categories({"test": ["test"]})
        self.assertEqual(len(test), 1)

    def test_adding_new_category(self):
        test = target_script.add_new_category({"test": ["test"]}, "test")
        self.assertEqual(test, False)

    def test_deleting_new_category(self):
        test = target_script.delete_category({"test": ["test"]}, "not")
        self.assertEqual(test, False)

    def test_adding_new_url(self):
        test = target_script.add_new_url({"test": ["test"]}, "test", "lol.ru")
        self.assertEqual(test, True)

    def test_deleting_url(self):
        test = target_script.\
            add_new_category({"test": ["test", "lol.ru"]}, "lol.ru")
        self.assertEqual(test, True)

    def test_getting_result(self):
        test = target_script.check(["google.ru"])
        self.assertEqual(len(test), 1)

    def test_getting_emodji(self):
        test = target_script.get_country_ip()
        self.assertEqual(isinstance(test, str), 1)

    def test_printing_func(self):
        test = target_script.print_menu()
        self.assertEqual(test, None)

    def test_saving_dict(self):
        test = target_script.save_urls(["lol"])
        self.assertEqual(test, False)

    def test_handling_menu(self):
        test = target_script.handle_menu(7)
        self.assertEqual(test, False)


if __name__ == "__main__":
    unittest.main()
