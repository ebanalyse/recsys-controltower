from typing import List
import requests
import boto3
from botocore.exceptions import ClientError
import json
from requests.auth import HTTPBasicAuth
# from math import ceil

#################################
#  Class for fetching articles  #
#################################


class MimisbrunrrAPI(object):
    # Get multiple
    # https://prod.mimisbrunrr.com/api/escenic/article/?id__in=8090973,8091036

    def __init__(self):
        self._base_endpoint = "https://prod.mimisbrunrr.com/api/"

        # Being set from _load_credentials()
        self._username = None
        self._password = None
        self._auth = None
        self._load_credentials()

    def _get_auth(self):
        if self._auth is None:
            self._auth = HTTPBasicAuth(
                username=self._username, password=self._password)
        return self._auth

    def _load_credentials(self):
        secret_name = "MimisbrunrrAdmin-prod"
        region_name = "eu-west-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']
        try:
            j = json.loads(secret)
            self._username = j.get('user', None)
            self._password = j.get('password', None)
        except Exception as e:
            raise e

    def get_articles(self, ids):
        url = "https://prod.mimisbrunrr.com/api/escenic/article/"
        auth = self._get_auth()

        # In order to not exceed the max request line 4092 chunk the ids
        max_ids_per_request = 400
        id_bins = [ids[i:i+max_ids_per_request]
                   for i in range(0, len(ids), max_ids_per_request)]
        ids_strs = [",".join([str(x) for x in id_bin]) for id_bin in id_bins]

        articles = []
        for ids_str in ids_strs:
            resp = requests.request(method="GET",
                                    url=url,
                                    params={
                                        "id__in": ids_str,
                                        "page_size": 400,
                                    },
                                    auth=auth)

            print(resp.status_code)

            def fetch_until_no_more(next_url):
                if next_url is None:
                    return []

                # print(f"GET: {next_url}")
                resp = requests.request(method="GET",
                                        url=next_url,
                                        auth=auth)
                print(resp.status_code)
                if resp.status_code == 200:
                    json_res = resp.json()
                    return json_res["results"] + fetch_until_no_more(json_res['next'])
                return []

            if resp.status_code == 200:
                # TODO HANDLE PAGINATION
                json_res = resp.json()
                articles += json_res["results"]
                if json_res['next']:
                    articles += fetch_until_no_more(json_res['next'])

        return articles

####################################
#  Class for fetching engagelists  #
####################################


class EngageListsAPI(object):
    """
    Available engage lists:
      - name: "most popular"
        type: "engage"
        id: "most_read_last_24_hours"
      - name: "most popular 24 hours"
        type: "engage"
        id: "most_read_last_24_hours"
      - name: "latest published politik samfund"
        type: "engage"
        id: "latest_published_politik_samfund"
      - name: "latest published fodbold"
        type: "engage"
        id: "latest_published_fodbold"
      - name: "latest published plus"
        type: "engage"
        id: "latest_published_premium"
      - name: "latest published all"
        type: "engage"
        id: "latest_published_all_sections"
    """

    def __init__(self):
        self._endpoint = "https://91f2powxgh.execute-api.eu-west-1.amazonaws.com/art-seg-prod-deploy"
        self._auth_token = "1413249utdfije9sdifd9324"

    def get_lists(self) -> List[str]:
        try:
            endpoint = f"{self._endpoint}/lists"
            res = requests.request(method="GET",
                                   url=endpoint,
                                   headers={"Authorization": self._auth_token})
            json_res = res.json()
            return sorted(json_res["Lists"])
        except requests.HTTPError as e:
            print(e)
            return []

    def get_list(self, list_id: str) -> List[int]:
        try:
            endpoint = f"{self._endpoint}/list"
            res = requests.request(method="GET",
                                   url=endpoint,
                                   params={"name": list_id},
                                   headers={"Authorization": self._auth_token})
            json_res = res.json()
            return json_res["Articles"]
        except requests.HTTPError as e:
            print(e)
            return []


if __name__ == "__main__":
    article_ids = [8090973, 8091036]
    EngageListsAPI().get_lists()
    article_ids = EngageListsAPI().get_list("sport_15_days")
    len(article_ids)
    r = MimisbrunrrAPI().get_articles(article_ids)
