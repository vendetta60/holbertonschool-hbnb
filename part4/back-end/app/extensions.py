#!/usr/bin/python3
"""Helps with circulating error when creating a user"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
jwt = JWTManager()