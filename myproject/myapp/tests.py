# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee

class EmployeeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create(name='John Doe', age=30,gender='M',department='devops',salary=50000)

    def test_create_employee(self):
        url = reverse('employee-list-create')
        data = {'name': 'Jane Smith', 'age': 25,'gender':'M','department':'devops','salary':50000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_list_employees(self):
        url = reverse('employee-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_employee(self):
        url = reverse('employee-retrieve-update-destroy', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)

    def test_update_employee(self):
        url = reverse('employee-retrieve-update-destroy', args=[self.employee.id])
        data = {'name': 'Updated Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.get(id=self.employee.id).name, 'Updated Name')

    def test_delete_employee(self):
        url = reverse('employee-retrieve-update-destroy', args=[self.employee.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
