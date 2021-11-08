from flask import Flask, request
from app.exceptions.exceptions import InvalidIdError, InvalidUpdateDataError, MissingKeyError
from app.models.models import Post

def init_app(app: Flask):

    @app.post('/posts')
    def create_post():
        data = request.json
        requested_args = set(["title", "author", "tags", "content"])

        try:
            if set(data.keys()) - requested_args != set():
                raise MissingKeyError
            post = Post(**data)
            return post.new_post()
        except MissingKeyError:
            return {"message": "Requisição incompleta"}, 400
     

    @app.delete('/posts/<int:id>')
    def delete_post(id):
        try:
            return Post.remove_post(id)
        except InvalidIdError:
            return {"message": "Post não encontrado"}, 404

    @app.get('/posts/<int:id>')
    def read_post_by_id(id):
        try:
            return Post.get_specific_post(id)
        except InvalidIdError:
            return {"message": "Post não encontrado"}, 404

    @app.get('/posts')
    def read_posts():
        return Post.get_all_posts()
    
    @app.patch('/posts/<int:id>')
    def update_post(id):
        data = request.json
        try:
            return Post.update_specific_post(id, **data)
        except InvalidUpdateDataError:
            return {"message":"Dados para atualização inválidos."}, 400
        except InvalidIdError:
            return {"message":"Post não encontrado"}, 404