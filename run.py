from dtable import NjuTableAuth
from dotenv import load_dotenv
from pytz import timezone
import logging
import os
import datetime
from screenshot import get_skm_img, get_xcm_img

ROOT_URL = 'https://table.nju.edu.cn'
TABLE_TOKEN = 'acb58836-10ae-4ec0-a2bf-8cce3245a373'

auth = NjuTableAuth(TABLE_TOKEN)


if __name__ == "__main__":
    load_dotenv(verbose=True)
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    log = logging.getLogger()

    username = os.getenv('NJU_USERNAME')
    password = os.getenv('NJU_PASSWORD')
    name = os.getenv('NAME')
    phone = os.getenv('PHONE')
    skm_token = os.getenv('SKM_TOKEN')

    if username is None or password is None:
        log.error('账户或密码信息为空！请检查是否正确地设置了 SECRET 项（GitHub Action）。')
        os._exit(1)

    if name is None or phone is None or skm_token is None:
        log.error('人员信息、苏康码或行程码信息为空！请检查是否正确地设置了 SECRET 项（GitHub Action）。')
        os._exit(1)
    try:
        log.info('获取苏康码截图...')
        skm_pic = get_skm_img(skm_token)
        log.info('苏康码截图获取成功！获取行程码截图...')
        xcm_pic = get_xcm_img(phone)
        log.info('行程码截图获取成功！')
    except Exception as e:
        log.error('苏康码、行程码截图错误！出现"网络繁忙，请稍后重试"表示苏康码token有误')
        log.error(e)
        os._exit(1)

    ok = auth.login(username, password)
    if not ok:
        log.error('登陆失败')
        os._exit(1)
    log.info('登录成功！')

    try:
        current_time = datetime.datetime.now(
            timezone('Asia/Shanghai')).strftime("%Y%m%d%H%M%S")
        # upload skm_pic
        upload_info = auth.getUploadLinkViaFormToken(TABLE_TOKEN)
        assert upload_info is not None and upload_info != "", f'getUploadLink Error,{upload_info}'
        upload_info = dict(eval(upload_info))
        skm_name = auth.uploadPic(upload_info['upload_link'], upload_info['parent_path'],
                                  upload_info['img_relative_path'], skm_pic, f'screenshot_01_{current_time}.jpg')
        # upload xcm_pic
        upload_info = auth.getUploadLinkViaFormToken(TABLE_TOKEN)
        assert upload_info is not None and upload_info != "", f'getUploadLink Error,{upload_info}'
        upload_info = dict(eval(upload_info))
        xcm_name = auth.uploadPic(upload_info['upload_link'], upload_info['parent_path'],
                                  upload_info['img_relative_path'], xcm_pic, f'screenshot_02_{current_time}.jpg')

        # TODO：变更项
        submit_data = {
            '人员': name,
            '学号': username,
            '苏康码截图': [f'{ROOT_URL}/dtable/forms/{TABLE_TOKEN}/asset/{skm_name}'],
            '行程码截图': [f'{ROOT_URL}/dtable/forms/{TABLE_TOKEN}/asset/{xcm_name}']
        }
        ok = auth.submit_form(TABLE_TOKEN, submit_data)
        if not ok:
            log.error("申报失败，请手动申报")
            os._exit(1)
        else:
            log.info("申报成功！")
    except Exception as e:
        log.error("申报失败，可能是超出申报时间")
        log.error(e)
        os._exit(1)
