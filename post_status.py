#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class PostStatus(Enum):
    ERROR = 0
    RETRY = 1
    OK = 2
