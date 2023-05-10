import random
import string

from main import app
import json
import unittest


class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """
    def test_register(self):
        username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = "pw" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        body = {"username": username, "password": password}

        headers = {
            "content-type": "application/json"
        }

        request, response = app.test_client.post('/auth/register', json = body, headers = headers)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('status'), "success")
        token = data.get('token')
        return token

    def test_login(self):
        body = {
            "username": "user8zbb93qj",
            "password": "pwZ4VKR6DZ"
        }
        headers = {
            "content-type": "application/json"
        }

        request, response = app.test_client.post('/auth/login', json = body, headers = headers)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('status'), "success")
        token = data.get('token')
        return token

    def test_get_all_books(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    # TODO: unittest for another apis



    def test_create_book(self):

        token =self.test_login()
        body = {
            "title": "The Great Gatsby4",
            "authors": ["F. Scott Fitzgerald"],
            "publisher": "Charles Scribner's Sons_auth",
            "description": "The story of the mysterious Jay Gatsby and his love for the beautiful Daisy Buchanan, set amidst the glittering excess of the Roaring Twenties."
        }
        headers = {
            "Authorization": token,
            "content-type": "application/json"
        }

        request, response = app.test_client.post('/books', json = body, headers = headers)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('status'), "success")

    def test_get_book_by_id(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        number = data.get('n_books')
        id = data.get('books')[number-1]['_id']
        url = '/books/' + id
        request, response = app.test_client.get(url)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    def test_update_book(self):
        token =self.test_login()
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        number = data.get('n_books')
        id = data.get('books')[number - 1]['_id']
        body = {
            "_id": id,
            "title": "The Great Gatsby 1 da update da auth1 cua user1",
            "authors": [
                "F. Scott Fitzgerald"
            ],
            "publisher": "Charles Scribner's Sons",
            "description": "The story of the mysterious Jay Gatsby and his love for the beautiful Daisy Buchanan, set amidst the glittering excess of the Roaring Twenties.",
            "owner": "null",
            "createdAt": 1683533525,
            "lastUpdatedAt": 1683533525
        }
        headers = {
            "Authorization": token,
            "content-type": "application/json"
        }
        url = '/books/' + id
        request, response = app.test_client.put(url, json=body, headers=headers)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('status'), "success")

    # def test_delete_book(self):
    #     token = self.test_login()
    #     request, response = app.test_client.get('/books')
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     number = data.get('n_books')
    #     _id = data.get('books')[number - 1]['_id']
    #
    #     headers = {
    #         "Authorization": token,
    #         "content-type": "application/json"
    #     }
    #     url = '/books/' + _id
    #     request, response = app.test_client.delete(url, headers=headers)
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     self.assertEqual(data.get('status'), "success")
    # Em chua biet cach viet unitest o ham nay vi neu cho xoa phan tu sach moi nhat thi se khong thuc hien duoc ham test_update_book










if __name__ == '__main__':
    unittest.main()
