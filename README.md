# Finance Dashboard for the Management of Expenses and Income

CSC 302 System Analysis and Design, Group A51. Case study: Computer Science and AI Department, University of Ibadan.

A web system that gives the department its own current view of what it has received and spent. An Officer records transactions, a Head of Department approves large expenses, and an Administrator manages accounts.

## 1. What is in this folder

| Item | What it is |
|---|---|
| The Django project folder (manage.py, core/, financedash/) | The working system |
| requirements.txt | The Python packages needed |
| db.sqlite3 | The SQLite database with preloaded demo and test records |
| .gitignore | Keeps junk files out of GitHub |
| README.md | This file |

## 2. Technology and why we chose it

| Tool | Why |
|---|---|
| Python | One language for the whole system; readable for a group project |
| Django | Already provides login, user roles, and an admin page (covers NFR3, NFR4, FR9, FR10) |
| SQLite | A database in one file; no server to install |
| HTML and CSS templates | One base template and one style sheet give every screen the same look (NFR8) |
| VS Code | Editor used to write the code |

## 3. How the requirements map to the system

| Requirement | Where it lives |
|---|---|
| FR1, FR2, FR3, FR8: record income and expenses with category and receipt reference | Transaction entry screen (core/forms.py, core/views.py) |
| FR4: set a budget per category per month | Budgets screen |
| FR5: flag expenses above the limit for approval | Approval check in core/views.py; Pending approvals screen |
| FR6: monthly report | Monthly report screen |
| FR7: dashboard totals and budget usage | Dashboard screen |
| FR9, FR10: users, roles, categories | Django admin (core/admin.py) |
| NFR3, NFR4: login and role limits | Login screen and role checks in core/views.py |
| NFR9: amounts in Naira | All screens |

## 4. Roles

| Role | Can do |
|---|---|
| Officer | Record transactions, set budgets, view the dashboard and reports |
| Head of Department | View the dashboard and reports; approve or reject large expenses |
| Administrator | Manage users, roles, categories, and the approval limit |

Each role is blocked from the others' actions (tested in TC16 to TC18).

## 5. Rules the code enforces

- BR4: an amount must be greater than zero (core/forms.py).
- BR5: the category type must match the transaction type (core/forms.py).
- BR8: only one budget per month and category (unique pair in core/models.py).
- Approval limit: an expense above the limit is saved as pending, not final. In test TC8, an expense of 80,000 against a limit of 50,000 became a pending approval.
- Passwords are stored hashed, never as typed (fixed in core/admin.py).

## 6. How to run it

Windows:

1. Open a terminal in the project folder (the one with manage.py).
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver
7. Open http://127.0.0.1:8000/

Mac or Linux: use source venv/bin/activate for step 3.

## 7. Accounts for testing

| Role | Username | Notes |
|---|---|---|
| Officer | officer_test | Preloaded in `db.sqlite3` (or create via Django admin) |
| Head of Department | hod_test | Preloaded in `db.sqlite3` (or create via Django admin) |
| Administrator | admin | Superuser account (`python manage.py createsuperuser` if needed) |

Passwords are not stored in plain text in this repository. Use the preloaded test accounts in `db.sqlite3` or create a new superuser via `python manage.py createsuperuser` to log into `/admin/`.

## 8. Testing

18 black-box test cases (TC1 to TC18), all passed. Two real faults were found and fixed:

1. Missing role check: a logged-in user could open screens meant for another role. Fixed in core/views.py.
2. Plain-text password: accounts made in the admin page stored the password as typed. Fixed in core/admin.py.

Screenshots of every screen and every test are in the folder Screenshots & Pictures.

## 9. Limits we state honestly

- Speed and uptime (NFR1, NFR2, NFR6) were not measured under load.
- The system was tested by the group, not by real department staff.
- There is no password reset, audit log, or email notification yet.

## 10. GitHub

1. Create an empty repository on GitHub, for example finance-dashboard-a51.
2. In the project folder, run:
   - git init
   - git add .
   - git commit -m "Finance dashboard"
   - git branch -M main
   - git remote add origin PASTE-REPOSITORY-LINK-HERE
   - git push -u origin main
3. Paste the link here.

GitHub link: [https://github.com/EMMANUELWB/finance-dashboard-a51](https://github.com/EMMANUELWB/finance-dashboard-a51)

## 11. Hosting (optional)

Vercel is built for JavaScript sites and handles Django poorly, and it cannot keep a SQLite file between visits. If you want a live link, use a Python host with a Neon or Supabase Postgres database. For the submission, a GitHub link plus the screenshots shows the working system.

## 12. Group

Group A51: Emmanuel Idoko Agbo (Group Leader), Agunloye Marvellous Abimbola, Orumgbe Samuel Ifeanyichukwu, Adeleke Faruq Adeniji, Agbebi Oluwatobi Temitayo. Implementation by Emmanuel Idoko Agbo (Tasks 8 and 9).
