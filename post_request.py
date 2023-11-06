#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import cv2

import post_status as ps


class PostRequest():
    def __init__(self, retry_count, con_timeout, req_timeout):
        self.__retry_count = retry_count
        self.__con_timeout = con_timeout
        self.__req_timeout = req_timeout

    # JSONをPOSTリクエストする
    def request_json(self, url, req_id, json):
        return self.__try_post(url, req_id, 'application/json', json)

    # 画像をPOSTリクエストする
    def request_image(self, url, req_id, img):
        # print(data)
        return self.__try_post(url, req_id, 'image/jpeg', img)

    # ビデオをPOSTリクエストする
    def request_video(self, url, req_id, video_path):
        return self.__try_post(url, req_id, 'video/mp4', self.__read_data(video_path))

    def __read_data(self, path):
        with open(path, mode='rb') as f:
            return f.read()

    def __try_post(self, url, req_id, content_type, data):
        post_ret = False
        retry_count = 0
        res = ""
        while(retry_count <= self.__retry_count):
            if retry_count > 0:
                print("リトライ回数: ", retry_count)

            try:
                res, err = self.__run_request(url, req_id, content_type, data)
                print(res, err)
            except requests.exceptions.Timeout as timeout_err:
                print("TIMEOUT: ", timeout_err)
                err = "timeout"
            except:
                err = "error"
                print("error:", res)

            ret = self.__check_post(res, err)
            if ret is ps.PostStatus.OK:
                post_ret = True
                break
            elif ret is ps.PostStatus.RETRY:
                retry_count += 1
                continue
            else:
                break
        return post_ret

    def __run_request(self, url, req_id, content_type, req_data):
        headers = {
            'authorization': "Bearer 539cbd1d-b111-4a9e-833f-5fcb29ce2e94",
            'x-event-id': req_id,
            'x-event-type': 'object',
            'Content-Type': content_type
        }
        return requests.post(url, headers=headers, data=req_data, timeout=(self.__con_timeout, self.__req_timeout)), None

    def __check_post(self, res, err):
        ret = ps.PostStatus.ERROR
        # エラー処理
        if err == "timeout":
            return ps.PostStatus.OK
        elif err == "error":
            return ps.PostStatus.RETRY
        print("Response of request: ", res.status_code)
        if res.status_code == 200:
            ret = ps.PostStatus.OK
        # レスポンス処理
        # リクエストエラー: リトライは行わずスキップ
        elif res.status_code == 400:
            ret = ps.PostStatus.ERROR
            print("response error")
        # サーバエラー: リトライは行わずスキップ
        elif res.status_code == 500:
            print("サーバエラー.")
            ret = ps.PostStatus.ERROR
        # 高負荷/外部接続エラー/サーバ接続エラー: リトライを行う
        elif res.status_code == 503:
            print("高負荷/外部接続エラー/サーバ接続エラー. re-request.")
            ret = ps.PostStatus.RETRY
        else:
            print("Error occured")
            print("status code:", res.status_code)
            ret = ps.PostStatus.RETRY
        return ret
