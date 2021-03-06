import datetime
from http import HTTPStatus
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class RatingListResource(Resource) :
    @jwt_required()
    def post(self) :

        # 1. 클라이언트로부터 데이터를 받아온다.
        # {
        #     "movie_id": 32,
        #     "rating": 4
        # }

        data = request.get_json()
        user_id = get_jwt_identity()

        # 2. 디비에 insert
        try :
            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into rating
                    (userId, movieId, rating)
                    values
                    (%s, %s , %s);'''
            
            record = (user_id, data['movieId'], 
                        data['rating'] )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503

        return {'result' : 'success'}, 200

    @jwt_required()
    def get(self) :

        # 1. 클라이언트로부터 데이터 받아온다.
        # ?offset=0&limit=25

        offset = request.args['offset']
        limit = request.args['limit']
        user_id = get_jwt_identity()

        # 2. 내 리뷰리스트를 디비에서 가져온다.
        try :
            connection = get_connection()

            query = '''select m.title, r.rating
                    from rating r 
                    join movie m 
                    on r.movieId = m.id and r.userId = %s                    
                    limit '''+offset+''' , '''+limit+''';'''
            
            record = (user_id,)

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)     

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return {'result' : 'success' ,
                'count' : len(result_list) , 
                'items' : result_list} , 200


    
class MovieRatingResourse(Resource):
    def get(self,movie_id):
        
        # 1.클라이언트로 부터 데이터를 받아온다.
        # ?offset=0&limit=25
        offset = request.args['offset']
        limit = request.args['limit']
        
        try :
            connection = get_connection()

            query = '''select m.title,r.rating,u.gender,u.name
                    from rating r
                    join movie m
                    on r.movieId = m.id and m.id = %s
                    join user u 
                    on r.userId = u.id
                    limit 0,25;                  
                    limit '''+offset+''' , '''+limit+''';'''
            
            record = (movie_id,)

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)     

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return {'result' : 'success' ,
                'count' : len(result_list) , 
                'items' : result_list} , 200

        
class MovieSearchResource(Resource):
    def get(self):
        
        # 1. 클라이언트가 보낸 데이터를 받는다.
        # ?keyword=hello&offset=0&limit=25
        keyword = request.args['keyword']
        offset = request.args['offset']
        limit = request.args['limit']
        
        try :
            connection = get_connection()

            query = '''select m.title ,count(r.movieId) as cunt, ifnull(avg(r.rating),0) as avg
                    from movie m 
                    join rating r
                    on m.id = r.movieId
                    where m.title like '%'''+keyword+'''%'
                    group by m.id                  
                    limit '''+offset+''' , '''+limit+''';'''
            
            # record = (movie_id,)

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)   

            i = 0
            for record in result_list :
                result_list[i]['avg'] = float(record['avg'])
                i = i + 1             

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return {'result' : 'success' ,
                'count' : len(result_list) , 
                'items' : result_list} , 200
            
        
        
