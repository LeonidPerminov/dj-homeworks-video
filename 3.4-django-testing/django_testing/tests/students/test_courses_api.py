import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)
    return factory

@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    response = api_client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    target_id = courses[1].id
    response = api_client.get('/api/v1/courses/', data={'id': target_id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course_factory(name='Python Basics')
    course_factory(name='Advanced Django')
    response = api_client.get('/api/v1/courses/', data={'name': 'Python Basics'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Python Basics'

@pytest.mark.django_db
def test_create_course(api_client):
    data = {'name': 'New Course'}
    response = api_client.post('/api/v1/courses/', data=data)
    assert response.status_code == 201
    assert Course.objects.filter(name='New Course').exists()

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name='Old Name')
    data = {'name': 'Updated Name'}
    response = api_client.put(f'/api/v1/courses/{course.id}/', data=data)
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Updated Name'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    response = api_client.delete(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()
def test_example():
    assert False, "Just test example"
