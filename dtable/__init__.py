"""
DESCRIPTION:
    Tools for getting SeaTable of Nanjing University
PACKAGES:
    NjuTableAuth
"""
import requests
import re
import json

ROOT_URL = 'https://table.nju.edu.cn'
LOGIN_URL = ROOT_URL+'/accounts/login/'


class NjuTableAuth:
    """
    DESCRIPTION:
        Designed for passing SeaTable of Nanjing University.
    """

    def __init__(self, token) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
        })
        r = self.session.get(LOGIN_URL)
        self.cookies = r.cookies.get_dict()
        self.table_token = token
        self.csrfmiddlewaretoken = re.search(
            r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*)">', r.text).group(1)

    def login(self, username, password, next='/'):
        """
        DESCRIPTION:
            Post a request for logging in.
            Return true if login success, false otherwise
        ATTRIBUTES:
            username(str)
            password(str)
            next(str): redirect to dtable page, otherwise to ROOT_URL. e.g. f'/dtable/forms/{your_table_token}/'
        """
        data = {
            'login': username,
            'password': password,
            'csrfmiddlewaretoken': self.csrfmiddlewaretoken,
            'next': next,
        }
        r = self.session.post(LOGIN_URL, data=data,
                              allow_redirects=False)
        return r.status_code == 302

    def getUploadLinkViaFormToken(self, token):
        """
        DESCRIPTION:
            Api refer to npm module 'dtable-web-api'
        ATTRIBUTES:
            token(str): table token
        RETURN_VALUE:
            link_info(dict str), keys and format as :
            {
                'file_relative_path': "files/2022-04",
                'img_relative_path': "forms",
                'parent_path': "/asset/xxxx",
                'public_path': "public",
                'upload_link': "xxx"
            }
        """
        url = f'{ROOT_URL}/api/v2.1/forms/{token}/upload-link/'
        r = self.session.get(url)
        assert r.status_code == 200, f'Request Error,{r.status_code}'
        return r.text

    def uploadPic(self, upload_link, dir, relative_path, file, file_name="my_pic.jpg"):
        """
        DESCRIPTION:
            Upload based on upload_link and position 
        ATTRIBUTES:
            upload_link(str): link_info['upload_link']
            dir(str): link_info['parent_path']
            relative_path(str): link_info['img_relative_path']
            file(binary)
        RETURN_VALUE:
            Uploaded image name(str)
            You can submit image in form as:
            [f'{ROOT_URL}/dtable/forms/{TABLE_TOKEN}/asset/{image_name}']

        """
        url = upload_link+'?ret-json=1'
        """
        You can use a tuple for the files mapping value, with between 2 and 4 elements, 
        if you need more control. The first element is the filename, followed by the contents, 
        and an optional content-type header value and an optional mapping of additional headers:
        files = {'upload_file': ('foobar.txt', open('file.txt','rb'), 'text/x-spam')}
        """
        files = {'file': (file_name, file)}
        data = {
            'parent_dir': dir,
            'relative_path': relative_path,
        }
        r = self.session.post(url, files=files, data=data)
        assert r.status_code == 200, f'uploadPic Error,{r.status_code}'
        return dict(eval(r.text)[0])['name']

    def submit_form(self, token, data):
        """
        DESCRIPTION:
            Submit form data
        ATTRIBUTES:
            token(str): table token
            data(dict): form data. You can submit image in form as:
            [f'{ROOT_URL}/dtable/forms/{TABLE_TOKEN}/asset/{image_name}']
        """
        # get table_id
        table_url = f'{ROOT_URL}/dtable/forms/{token}/'
        r = self.session.get(table_url)
        # TODO：optimize searching method
        table_id = re.search(
            r'table_id\\u0022\:\\u0022(.*)\\u0022\,\\u0022logo_url', r.text).group(1)
        form_data = {
            'table_id': table_id,
            'row_data': json.dumps(data)
        }
        headers = {
            'x-csrftoken': self.cookies['dtable_csrftoken']
        }
        submit_url = f'{ROOT_URL}/api/v2.1/form-submit/{token}/'
        r = self.session.post(submit_url, data=form_data, headers=headers)
        return r.status_code == 200
