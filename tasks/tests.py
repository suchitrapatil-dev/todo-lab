from django.test import TestCase
from django.urls import reverse

from .models import Todo


class TodoCrudTests(TestCase):
    def setUp(self):
        self.task = Todo.objects.create(title="Buy milk", description="2 litres")

    def test_list_page_shows_task(self):
        r = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Buy milk")

    def test_empty_list_message(self):
        Todo.objects.all().delete()
        r = self.client.get(reverse("tasks:task_list"))
        self.assertContains(r, "No tasks yet")

    def test_create_valid_task(self):
        r = self.client.post(reverse("tasks:task_create"), {"title": "Read notes", "description": ""})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Todo.objects.filter(title="Read notes").exists())

    def test_reject_whitespace_title(self):
        r = self.client.post(reverse("tasks:task_create"), {"title": "   ", "description": "x"})
        self.assertEqual(r.status_code, 200)  # form redisplayed
        self.assertEqual(Todo.objects.count(), 1)

    def test_reject_long_title(self):
        r = self.client.post(reverse("tasks:task_create"), {"title": "a" * 151})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Todo.objects.count(), 1)

    def test_update_keeps_same_pk(self):
        pk = self.task.pk
        self.client.post(reverse("tasks:task_update", args=[pk]),
                         {"title": "Buy oat milk", "description": "1 litre", "completed": "on"})
        self.task.refresh_from_db()
        self.assertEqual(self.task.pk, pk)
        self.assertEqual(self.task.title, "Buy oat milk")
        self.assertTrue(self.task.completed)
        self.assertEqual(Todo.objects.count(), 1)  # no duplicate

    def test_get_delete_does_not_delete(self):
        self.client.get(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertTrue(Todo.objects.filter(pk=self.task.pk).exists())

    def test_post_delete_then_404(self):
        pk = self.task.pk
        self.client.post(reverse("tasks:task_delete", args=[pk]))
        self.assertFalse(Todo.objects.filter(pk=pk).exists())
        r = self.client.get(reverse("tasks:task_detail", args=[pk]))
        self.assertEqual(r.status_code, 404)
