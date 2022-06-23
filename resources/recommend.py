import datetime
from http import HTTPStatus
from os import access
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
import pandas as pd
import numpy as np

class MovieRecomResource(Resource):
    @jwt_required()
    def get(self):
        
        # 1. 클라이언트로 부터 데이터를 받아온다
        user_id = get_jwt_identity()
        # 2. 추천을 위한 상관계수 데이터 프레임을 읽어온다.
        df = pd.read_csv('data/movie_movie_correlations.csv',index_col='title')
        # print(df)
        # 3. 이 유저의 별점 정보를 디비에서 가져온다.


    
        
        return

