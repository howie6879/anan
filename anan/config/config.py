#!/usr/bin/env python
"""
 Created by howie.hu at 2019/2/24.
"""
import os


class Config:
    # Basic config
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # MongoDB config
    mongo_dict = dict(
        host=os.getenv('MONGO_HOST', ""),
        port=int(os.getenv('MONGO_PORT', 27017)),
        username=os.getenv('MONGO_USERNAME', ""),
        password=os.getenv('MONGO_PASSWORD', ""),
        db='anan',
    )
