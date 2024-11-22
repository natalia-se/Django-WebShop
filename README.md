# Django-WebShop

Team Django project

A full-featured webshop built using Django, designed to provide a seamless shopping experience.
This project includes features like product management, user authentication, a shopping cart.

## Installation and Setup

Follow these steps to set up the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/natalia-se/Django-WebShop.git
   cd Django-WebShop
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt

   ```

4. Set up the Django project:
   Apply migrations

   ```
   python manage.py makemigrations
   python manage.py migrate

   ```

5. Start the development server:

   ```
   python manage.py runserver

   ```

6. Access the application at http://127.0.0.1:8000/.

## Contributing

1. Create a new branch for your feature:

   ```bash
   git checkout -b feature/new-feature
   ```

2. Commit your changes.
3. Push your branch.
4. Open a pull request on GitHub.
