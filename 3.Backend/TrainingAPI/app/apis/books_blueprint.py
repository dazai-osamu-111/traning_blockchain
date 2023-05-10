import uuid

from sanic import Blueprint
from sanic.response import json

from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.auth import protected
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError
# from app.hooks.error import ApiInternalError
from app.models.book import create_book_json_schema, Book

books_bp = Blueprint('books_blueprint', url_prefix='/books')

_db = MongoDB()


@books_bp.route('/')
async def get_all_books(request):
    # # TODO: use cache to optimize api
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is None:
            book_objs = _db.get_books()
            books = [book.to_dict() for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)

    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
@protected
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # # TODO: Save book to database
    inserted = _db.add_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'status': 'success'})


# TODO: write api get, update, delete book
@books_bp.route('/<book_id>', methods={'GET'})
async def get_book_by_id(request,book_id):
    filter_ = {'_id': book_id}
    book_objs = _db.get_books(filter_, projection=None)
    books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/<book_id>', methods=['PUT'])
@protected
async def update_book(request, book_id, username = None):
    updated_data = request.json

    # Check if book exists
    book_obj = _db.get_books({'_id': book_id})
    book = book_obj[0].to_dict()
    if not book:
        return json({'error': 'Book not found'}, status=404)

    #check if is owner
    if book["owner"] != username:
        raise ApiInternalError('is not owner')



    # Update the book to database
    success = _db.update_book(book_id, updated_data)
    if not success:
        raise ApiInternalError('Fail to update book')

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'status': 'success'})


@books_bp.route('/<book_id>', methods=['DELETE'])
@protected
async def delete_book(request, book_id, username = None):
    # Check if book exists
    book_obj = _db.get_books({'_id': book_id})


    if not book_obj:
        return json({'error': 'Book not found'}, status=404)

    book = book_obj[0].to_dict()

    #check if is owner
    if book["owner"] != username:
        raise ApiInternalError('is not owner')

    # Delete the book from the database
    success = _db.delete_book(book_id)
    if not success:
        raise ApiInternalError('Fail to delete book')

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'status': 'success'})

