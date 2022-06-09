import pytest
from fastapi.testclient import TestClient

import app.robula_api
from app.main import api


def test_websocket_invalid_message(monkeypatch):

    monkeypatch.setattr(app.robula_api, "END_LOOP_FOR_TESTING", True)
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"msg": "Hello"})
        data = websocket.receive_json()
        assert data == {"error": "Invalid message format."}


def test_websocket_positive_case(monkeypatch):

    monkeypatch.setattr(app.robula_api, "END_LOOP_FOR_TESTING", True)
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        mock_message = {
            "action": "schedule_xpath_generation",
            "payload": {
                "document": '"<head jdn-hash=\\"7437302889559760668635644354\\'
                '">\\n        <meta charset=\\"utf-8\\" jdn-hash=\\'
                '"0804855189559760662416741793\\">\\n        '
                '<title jdn-hash=\\"5214925616559760665036205317\\">'
                "Комбинации блоков с глубиной 3</title>\\n\\t<style "
                'jdn-hash=\\"3982843610559760669157146287\\">\\n\\'
                "t\\tdiv {\\n  \\t\\t\\tbackground-color: #7695FE;"
                "\\n  \\t\\t\\tborder: thin #336699 solid;\\n  "
                "\\t\\t\\tpadding: 10px;\\n  \\t\\t\\tmargin: 10px;"
                "\\n  \\t\\t\\ttext-align: center;\\n\\n\\t\\t}\\"
                "n\\t\\theader {\\n\\t\\t\\tborder-color: #008a77;"
                "\\n\\t\\t\\tborder-style: solid;\\n\\t\\t\\"
                "tpadding: 10px;\\n\\t\\t\\tmargin: 10px;\\n\\t\\"
                "t}\\n\\t\\tfooter {\\n\\t\\t\\tborder-color: #008a77;"
                "\\n\\t\\t\\tborder-style: solid;\\n\\t\\t\\"
                "tpadding: 10px;\\n\\t\\t\\tmargin: 10px;\\n\\t\\"
                "t}\\n\\t</style>\\n    </head>\\n    "
                '<body jdn-hash=\\"9365965576559760663932210658\\"'
                '>\\n        <header id=\\"main1\\" '
                'jdn-hash=\\"3913738650559760668611004189\\">\\'
                'n\\t\\t<h1 jdn-hash=\\"9418105228559760663122499447\\">'
                "Header с уникальным ID = main1</h1>\\n\\t        "
                '<div id=\\"main2\\" '
                'jdn-hash=\\"9854853464559760668730991390\\">\\n\\'
                "t\\t    Блок с уникальным ID = main2\\n\\t       "
                '     <div id=\\"main3\\" '
                'jdn-hash=\\"6862050948559760666430680549\\">'
                "Блок с уникальным ID = main3</div>\\n\\t         "
                '   <div jdn-hash=\\"9493188821559760669875391327\\'
                '">Блок без ID</div>\\n\\t        </div>\\n\\t    '
                '    <div jdn-hash=\\"7520781528559760661906321107\\"'
                ">\\n\\t\\t    Блок без ID\\n\\t            "
                '<div id=\\"main4\\" '
                'jdn-hash=\\"3189676561559760661294561923\\">'
                "Блок с уникальным ID = main4</div>\\n\\t          "
                '  <div jdn-hash=\\"5389137237559760664282471861\\'
                '">Блок без ID</div>\\n\\t        </div>\\n\\n\\t'
                '</header>\\n\\t<div class=\\"Content\\" '
                'jdn-hash=\\"0496233594559760661051207166\\">\\'
                'n\\t\\t<h2 jdn-hash=\\"0112389422559760667916905668\\"'
                ">Просто заголовок</h2>\\n\\t\\t<p "
                'jdn-hash=\\"0486422498559760669553972716\\">'
                "Какой-то контент</p>\\n\\t\\t<h2 "
                'jdn-hash=\\"3463068754559760667310543167\\">'
                "Еще один</h2>\\n\\t\\t<p "
                'jdn-hash=\\"2767519528559760664880308513\\">'
                "И снова</p>\\n\\t</div>\\n        "
                '<footer jdn-hash=\\"8261998788559760660161999069\\"'
                '>\\n\\t\\t<h1 jdn-hash=\\"2315847784559760661500578043\\"'
                '>Footer без ID</h1>\\n\\t        <div id=\\"main5\\"'
                ' jdn-hash=\\"1054128445559760663700144748\\">\\n\\t\\t'
                "    Блок с уникальным ID = main5\\n\\t            "
                '<div id=\\"mai6\\" jdn-hash=\\"2879953449559760660783129944\\"'
                ">Блок с уникальным ID = main6</div>\\n\\t            "
                '<div jdn-hash=\\"6921880154559760671177462018\\">'
                "Блок без ID</div>\\n\\t        </div>\\n\\t        "
                '<div jdn-hash=\\"0011994463559760676429491913\\">'
                "\\n\\t\\t    Блок без ID\\n\\t            "
                '<div id=\\"main7\\" '
                'jdn-hash=\\"6654392548559760678563476605\\">'
                "Блок с уникальным ID = main7</div>\\n\\t            "
                '<div jdn-hash=\\"6905471988559760672625853013\\">'
                "Блок без ID</div>\\n\\t        </div>\\n\\"
                "t</footer>\\n    \\n<div "
                'id=\\"9418105228559760663122499447\\" '
                'class=\\"jdn-highlight jdn-secondary\\" '
                'jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 30.4px; top: 43.8375px; '
                'height: 37.6px; width: 1458.4px;\\"><div>'
                '<span class=\\"jdn-label\\"><span class=\\'
                '"jdn-class\\">100%, uielementH11</span></span></div>'
                '</div><div id=\\"0112389422559760667916905668\\" '
                'class=\\"jdn-highlight jdn-secondary\\" '
                'jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 29px; top: 478.587px; height: 27.2px;'
                ' width: 1461.2px;\\"><div><span class=\\"jdn-label\\"'
                '><span class=\\"jdn-class\\">100%, uielementH2</span>'
                "</span></div></div><div "
                'id=\\"0486422498559760669553972716\\" '
                'class=\\"jdn-highlight jdn-secondary\\" '
                'jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 29px; top: 525.7px; height: 18.4px;'
                ' width: 1461.2px;\\"><div><span class=\\"jdn-label\\"'
                '><span class=\\"jdn-class\\">100%, uielementP</span>'
                '</span></div></div><div id=\\"3463068754559760667310543167\\"'
                ' class=\\"jdn-highlight jdn-secondary\\" '
                'jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 29px; top: 564.013px; height: 27.2px;'
                ' width: 1461.2px;\\"><div><span class=\\"jdn-label\\">'
                '<span class=\\"jdn-class\\">100%, uielementH23</span>'
                '</span></div></div><div id=\\"2767519528559760664880308513\\"'
                ' class=\\"jdn-highlight jdn-secondary\\"'
                ' jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 29px; top: 611.125px; height: 18.4px;'
                ' width: 1461.2px;\\"><div><span class=\\"jdn-label\\"'
                '><span class=\\"jdn-class\\">100%, uielementP5</span>'
                '</span></div></div><div id=\\"2315847784559760661500578043\\"'
                ' class=\\"jdn-highlight jdn-secondary\\"'
                ' jdn-highlight=\\"true\\" jdn-status=\\"undefined\\"'
                ' style=\\"left: 30.4px; top: 700.362px;'
                ' height: 37.6px; width: 1458.4px;\\"><div><span'
                ' class=\\"jdn-label\\"><span class=\\"jdn-class\\">'
                '100%, uielementH1</span></span></div></div></body>"',
                "id": "2315847784559760661500578043",
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(mock_message)
        data0 = websocket.receive_json()
        assert data0["action"] == "tasks_scheduled"
        data1 = websocket.receive_json()
        assert data1["action"] == "status_changed"
        data2 = websocket.receive_json()
        assert data2["action"] == "status_changed"
        data3 = websocket.receive_json()
        assert data3["action"] == "result_ready"
        assert data3["payload"]["result"]
