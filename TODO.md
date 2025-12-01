# TODO for Creating Test for Notifications App

- [x] Import necessary modules in notifications/tests.py (TestCase, mail, send_purchase_notification, Order, OrderItem, Product, User)
- [x] Create a test method test_send_purchase_notification in TestCase class
- [x] In the test method, create a User instance
- [x] Create a Product instance
- [x] Create an Order instance linked to the user
- [x] Create an OrderItem instance linked to the order and product
- [x] Call send_purchase_notification(order)
- [x] Assert that one email was sent (len(mail.outbox) == 1)
- [x] Assert the email subject, body contains expected content, and recipient is 'admin@gmail.com'
