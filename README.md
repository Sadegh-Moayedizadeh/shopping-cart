# Shopping Cart Application

This is a sample shopping cart application written as a part of an assessment
procedure from **NoviraTech** company.

The source code is developed in a type-safe manner following the best
practices in the field. As an example a use of generic typing can be seen
in the classes developed under ``crud`` directory.

The development of this project has been mostly test-driven following the
**red-green-refactor** pattern. The framework employed to develop the tests
is ``pytest`` and the structure of the tests follow the **xUnit** patterns.


## Models

The technology chosen as the orm is ``SQLAlchemy`` alongside ``Alembic`` for
the migration scripts.

Three database models have been developed:
* ``User`` that stores information of client of the website. Each user is
  associated with a shopping cart.
* ``Cart`` which denotes a shopping cart that can hold the products.
* ``Product`` That represents each product.

The relationship between ``User`` and ``Cart`` is one to one and the
relationship between ``Cart`` and ``Product`` is one to many.

There is also a script to populate the **Product** model with some fake data
gathered from the `fake store api`<https://fakestoreapi.com>.

The CRUD functionalities are implemented in a separate directory to have a
more modular design. A class named ``CRUDBase`` extracted all the common
behaviors to avoid duplications and decrease the coupling between entities.


## APIs

The restful APIs in this project fall into three categories:
* **Users** to create, read, and update users.
* **Login** to login to the application. This process is handled employing JWT
  tokens.
* **Products** to view the products and add to or remove from user's cart.


## Further development

Because of the shortage of time, the source code can be described as anything
but perfect. If there was unlimited time, there could have been more APIs
providing more thorough functionalities. A user could be able to purchase the
cart and we could have a model to store those purchases. Having some
super-user functionalities could also be nice. We could also have a pg-admin
interface for super-users who are not necessarily familiar with the code. We
could manage the dependencies with ``poetry``, we could have a ``config.py``
file, we could have used some kind of message queue, and so on.
