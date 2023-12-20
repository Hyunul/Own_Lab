import pymysql
import os
from flask import request
from flask_restx import Api, Namespace, Resource, fields
from config import DB
from werkzeug.utils import secure_filename

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

cursor = conn.cursor(pymysql.cursors.DictCursor)

Post_api = Namespace(
    name="Post",
    description="게시글 관련 API",
)

post_fields = Post_api.model('Post', {  # Model 객체 생성
    'title': fields.String(required=True),
    'content': fields.String(required=True),
    'email': fields.String(required=True)
})

@Post_api.route('/add_post', methods = ['POST'])
class add_post(Resource):
    @Post_api.doc(description='게시글 추가')
    @Post_api.expect(post_fields)
    def post(self): 
        title = request.json['title']
        content = request.json['content']
        email = request.json['email']
        
        cursor.execute("SELECT * FROM post where title = %s", title)
        posts = cursor.fetchone()

        if posts:
            if posts['title'] == title:
                return "fail"
        else:
            cursor.execute(f"INSERT INTO post (title, content, email) VALUES ('{title}', '{content}', '{email}')")
            conn.commit()
            return "success"
        
@Post_api.route('/get_post', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 조회')
    def get(self):
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        return posts
    
@Post_api.route('/get_post/<int:post_id>', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 확인')
    def get(self, post_id):
        cursor.execute(f"SELECT * FROM post WHERE post_id = {post_id}")
        posts = cursor.fetchall()
        return posts
    
@Post_api.route('/delete_post/<int:post_id>', methods = ['DELETE'])
class delete_post(Resource):
    @Post_api.doc(description='게시글 삭제')
    def delete(self, post_id):
        cursor.execute(f"SELECT * FROM post WHERE post_id = {post_id}")
        exist = cursor.fetchone()

        if exist is None:
            return "fail"
        else:
            cursor.execute(f"DELETE FROM post WHERE post_id = {post_id}")
            conn.commit()
            return "success"

@Post_api.route('/update_post/<int:post_id>', methods = ['PUT'])
class update_post(Resource):
    @Post_api.doc(description='게시글 수정')
    def put(self, post_id):
        title = request.json['title']
        content = request.json['content']
        cursor.execute(f"UPDATE post SET title = '{title}', content = '{content}' WHERE post_id = {post_id}")
        conn.commit()
        return "success"