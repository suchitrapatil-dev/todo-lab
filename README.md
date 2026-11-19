# Lab Worksheet I – Todo Application (Django + PostgreSQL)

A simple Todo app where you can **C**reate, **R**ead, **U**pdate and **D**elete tasks through your own web pages.

---

## 🧸 The big picture (explained simply)

Think of the app like a **restaurant**:

| Restaurant | Django | File |
|---|---|---|
| The menu (which page = which address) | **URLs** | `tasks/urls.py` |
| The waiter (takes your order, brings food) | **Views** | `tasks/views.py` |
| The order slip you fill in | **Form** | `tasks/forms.py` |
| The recipe for what a "dish" looks like | **Model** | `tasks/models.py` |
| The fridge where food is stored | **PostgreSQL database** | (set up in `settings.py`) |
| The plate the food is served on | **Templates (HTML)** | `tasks/templates/tasks/` |

So when you visit `/tasks/5/`:
1. **URL** says "that's the task detail page"
2. **View** asks the **Model** "give me task #5 from the fridge (database)"
3. If task #5 doesn't exist → **404 Not Found**
4. Otherwise the **Template** shows it nicely on the screen

---

## 📁 Project structure

```
todo_lab/
├── manage.py
├── requirements.txt
├── todo_project/          ← the PROJECT (settings, main URLs)
│   ├── settings.py
│   └── urls.py
└── tasks/                 ← the APP (our Todo stuff)
    ├── models.py          ← Todo model (Activity 2)
    ├── forms.py           ← TodoForm (Activity 4)
    ├── views.py           ← list/detail/create/update/delete
    ├── urls.py            ← named routes (Activity 3)
    ├── admin.py
    ├── tests.py           ← automatic checks
    ├── migrations/0001_initial.py
    └── templates/tasks/
        ├── base.html                 ← shared navigation
        ├── task_list.html
        ├── task_detail.html
        ├── task_form.html            ← used for BOTH create and edit
        └── task_confirm_delete.html
```

---

## Activity 1 – Set up the environment

### 1. Create the PostgreSQL database and user
Open **psql** (or pgAdmin's Query Tool) as the `postgres` user and run:

```sql
CREATE DATABASE todo_db;
CREATE USER todo_user WITH PASSWORD 'todo_pass';
ALTER DATABASE todo_db OWNER TO todo_user;
GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
```
> 💡 Making `todo_user` the **owner** gives it permission to create tables (needed on PostgreSQL 15+).

If you use a different name/password, change them in `todo_project/settings.py` under `DATABASES`.

### 2. Create and activate a virtual environment
Go into the `todo_lab` folder, then:

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Django and the PostgreSQL adapter
```bash
pip install -r requirements.txt
```

> 📝 If you're building it from scratch instead of using these files, the commands are:
> `django-admin startproject todo_project .` then `python manage.py startapp tasks`,
> and add `"tasks"` to `INSTALLED_APPS` in settings.py (already done here).

### 4. Run migrations and start the server
```bash
python manage.py migrate
python manage.py runserver
```
Open **http://127.0.0.1:8000/tasks/** — you should see "No tasks yet!" ✅

---

## Activity 2 – The Todo model

In `tasks/models.py`:

| Field | Django field | Why |
|---|---|---|
| `title` | `CharField(max_length=150)` | required, max 150 chars |
| `description` | `TextField(blank=True)` | `blank=True` = optional |
| `completed` | `BooleanField(default=False)` | new tasks start "not done" |
| `created_at` | `DateTimeField(auto_now_add=True)` | filled in automatically once |

- `__str__` gives a readable name, e.g. `Buy milk (not done)`.
- **Ordering decision:** `ordering = ["-created_at"]` → **newest tasks first**, everywhere.

Migrations (the migration file is already included, but this is the command):
```bash
python manage.py makemigrations tasks
python manage.py migrate
```

**Inspect the table** (pick one):
```bash
python manage.py dbshell
\d tasks_todo
SELECT * FROM tasks_todo;
\q
```
or
```bash
python manage.py shell
>>> from tasks.models import Todo
>>> Todo.objects.all()
```

---

## Activity 3 – URLs + Read pages

| Page | URL | Name |
|---|---|---|
| Task list | `/tasks/` | `tasks:task_list` |
| Task detail | `/tasks/<pk>/` | `tasks:task_detail` |
| Create | `/tasks/new/` | `tasks:task_create` |
| Update | `/tasks/<pk>/edit/` | `tasks:task_update` |
| Delete | `/tasks/<pk>/delete/` | `tasks:task_delete` |

- `todo_project/urls.py` uses `include("tasks.urls")`.
- Templates use `{% url 'tasks:...' %}` – **never hard-coded links**.
- `get_object_or_404()` → wrong id gives **HTTP 404**.
- Empty list shows a friendly "No tasks yet!" message.
- `base.html` gives every page the same navigation bar.

---

## Activity 4 – Create

- `TodoForm` is a **ModelForm** with `fields = ["title", "description", "completed"]` → `created_at` is **not** editable.
- `clean_title()` rejects empty/whitespace titles and anything over 150 chars **on the server**.
- **GET** → empty form. **POST** → validate → save → redirect to detail page.
- Invalid → form shown again **with error messages and what you typed**.
- Form has labels, **Save** button, **Cancel** link and `{% csrf_token %}`.

👉 **To do:** create at least 3 tasks, one **without** a description.

---

## Activity 5 – Update

- `TodoForm(request.POST, instance=task)` → `instance=` is the magic word that means
  "**update this existing row**", not "make a new one".
- Form opens pre-filled with current values.

👉 **To do:**
1. Edit one task's title and description.
2. Tick "Completed" on another task → Save. Then untick → Save.
3. Check the task number (`Task #…` on the detail page) didn't change and no duplicates appeared.

---

## Activity 6 – Delete

- **GET** `/tasks/<pk>/delete/` → only shows "Are you sure?" (nothing deleted!)
- **POST** (pressing the red Delete button) → deletes, then goes to the list.
- Cancel → back to the detail page, nothing deleted.
- Form has `{% csrf_token %}`.

👉 **To do:** delete one task, then visit `/tasks/<that number>/` → you should see **404 Not Found**.

---

## ✅ Run the automatic tests (optional but impressive)
```bash
python manage.py test tasks
```
These check: list page, empty message, create, whitespace/long title rejected,
update keeps same id, GET-delete doesn't delete, POST-delete then 404.

> The test runner creates a temporary database, so `todo_user` needs permission:
> `ALTER USER todo_user CREATEDB;`

---

## 🚀 Push to GitHub and submit

1. Create a **new empty repository** on github.com (e.g. `todo-lab`). Don't add a README there.
2. In the `todo_lab` folder:
```bash
git init
git add .
git commit -m "Lab Worksheet I - Todo app with Django and PostgreSQL"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/todo-lab.git
git push -u origin main
```
3. Email the repository URL to **phillip.gajadhar@uog.edu.gy**.
