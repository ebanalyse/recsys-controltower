from typing import List
import requests

#######################
#  EngageLists class  #
#######################


class EngageLists(object):
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
        pass

    def get_lists(self) -> List[str]:
        try:
            endpoint = f"{self._endpoint}/lists"
            res = requests.request(method="GET",
                                   url=self._endpoint,
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
                                   url=self._endpoint,
                                   params={"name": list_id},
                                   headers={"Authorization": self._auth_token})
            json_res = res.json()
            return json_res["Articles"]
        except requests.HTTPError as e:
            print(e)
            return []
