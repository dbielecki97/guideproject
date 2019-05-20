from django.test import TestCase

# Create your tests here.


from guide.models import Category


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name')

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))

    def test_object_label_plural(self):
        category = Category.objects.get(id=1)
        object_label_plural = category._meta.verbose_name_plural
        self.assertEquals(object_label_plural, 'categories')
