#!/usr/bin/python3
"""Defines environment-specific settings"""
import os

class Config:
    SECRET_KEY = 'hbnb-project-pt3'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db' # URI, Uniform Source Identifier for SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'development'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
