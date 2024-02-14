import pytest


@pytest.fixture
def mock_simple_page():
    mock_simple_page = (
        '"<head jdn-hash=\\"5199181866842394674406282593'
        '\\">\\n<title '
        'jdn-hash=\\"5990732221842394679796959251\\">A very '
        'simple webpage</title>\\n<basefont size=\\"4\\" '
        'jdn-hash=\\"7422534067842394675342522617\\">\\n'
        '</head>\\n\\n<body bgcolor=\\"FFFFFF\\" '
        'jdn-hash=\\"7863048312842394674327019673\\">\\n\\n'
        '<h1 jdn-hash=\\"9772922236842394671549553513\\">A '
        'very simple webpage. This is an \\"h1\\" level '
        "header.</h1>\\n\\n<h2 "
        'jdn-hash=\\"4193993466842394678988767466\\">This is '
        "a level h2 header.</h2>\\n\\n<h6 "
        'jdn-hash=\\"7583721053842394674210958853\\">This is '
        "a level h6 header.  Pretty small!</h6>\\n\\n<p "
        'jdn-hash=\\"5572629157842394676934206880\\">This is '
        'a standard paragraph.</p>\\n\\n<p align=\\"center\\" '
        'jdn-hash=\\"3363615764842394670921018049\\">Now '
        "I've aligned it in the center of the "
        'screen.</p>\\n\\n<p align=\\"right\\" '
        'jdn-hash=\\"5721291098842394672262179535\\">Now '
        "aligned to the right</p>\\n\\n<p "
        'jdn-hash=\\"6141640202842394676845507677\\"><b '
        'jdn-hash=\\"3480383656842394673342086838\\">Bold '
        "text</b></p>\\n\\n<p "
        'jdn-hash=\\"6509829360842394679374579325\\"><strong '
        'jdn-hash=\\"6686340432842394672915867634\\">Strongly '
        "emphasized text</strong>  Can you tell the "
        "difference vs. bold?</p>\\n\\n<p "
        'jdn-hash=\\"9552011587842394678546958439\\"><i '
        'jdn-hash=\\"8540635057842394672033697611\\">Italics'
        "</i></p>\\n\\n<p "
        'jdn-hash=\\"2124540623842394679666778990\\"><em '
        'jdn-hash=\\"7733525060842394670953927239'
        '\\">Emphasized text</em>  Just like '
        "Italics!</p>\\n\\n<p "
        'jdn-hash=\\"3454558281842394677212548221\\">Here is '
        "a pretty picture: <img "
        'src=\\"example/prettypicture.jpg\\" alt=\\"Pretty '
        'Picture\\" '
        'jdn-hash=\\"4888107319842394676938962285\\"></p>\\n'
        "\\n<p "
        'jdn-hash=\\"6491321822842394671263543627\\">Same '
        "thing, aligned differently to the paragraph: <img "
        'align=\\"top\\" src=\\"example/prettypicture.jpg\\" '
        'alt=\\"Pretty Picture\\" '
        'jdn-hash=\\"0141316083842394670777635798\\"></p>\\n'
        "\\n<hr "
        'jdn-hash=\\"0308362355842394677786454946\\">\\n\\n'
        '<h2 jdn-hash=\\"5806303415842394670029439121\\">How '
        "about a nice ordered list!</h2>\\n<ol "
        'jdn-hash=\\"4715235143842394682994661577\\">\\n  <li '
        'jdn-hash=\\"1603135005842394685658036421\\">This '
        "little piggy went to market\\n  </li><li "
        'jdn-hash=\\"9061192712842394685798659191\\">This '
        "little piggy went to SB228 class\\n  </li><li "
        'jdn-hash=\\"6528603828842394685044449206\\">This '
        "little piggy went to an expensive restaurant in "
        "Downtown Palo Alto\\n  </li><li "
        'jdn-hash=\\"3037655855842394687195730753\\">This '
        "little piggy ate too much at Indian Buffet.\\n  "
        "</li><li "
        'jdn-hash=\\"9171755459842394681247470737\\">This '
        "little piggy got lost\\n</li></ol>\\n\\n<h2 "
        'jdn-hash=\\"5610175704842394682912827557'
        '\\">Unordered list</h2>\\n<ul '
        'jdn-hash=\\"7057344733842394681094842113\\">\\n  <li '
        'jdn-hash=\\"3428834674842394689067147541\\">First '
        "element\\n  </li><li "
        'jdn-hash=\\"0344208139842394689703406210\\">Second '
        "element\\n  </li><li "
        'jdn-hash=\\"8875563235842394680818663908\\">Third '
        "element\\n</li></ul>\\n\\n<hr "
        'jdn-hash=\\"9304002644842394682625207574\\">\\n\\n'
        "<h2 "
        'jdn-hash=\\"9693930545842394683885892445\\">Nested '
        "Lists!</h2>\\n<ul "
        'jdn-hash=\\"5136859532842394689920587674\\">\\n  <li '
        'jdn-hash=\\"6565663620842394682507536512\\">Things '
        "to to today:\\n    <ol "
        'jdn-hash=\\"2410924237842394686818276434\\">\\n      '
        '<li jdn-hash=\\"6543257481842394684131309244\\">Walk '
        "the dog\\n      </li><li "
        'jdn-hash=\\"4628343248842394680808454803\\">Feed the '
        "cat\\n      </li><li "
        'jdn-hash=\\"0336109894842394681125551466\\">Mow the '
        "lawn\\n    </li></ol>\\n  </li><li "
        'jdn-hash=\\"1760244636842394686659416685\\">Things '
        "to do tomorrow:\\n    <ol "
        'jdn-hash=\\"6831289723842394688837035776\\">\\n      '
        "<li "
        'jdn-hash=\\"6925947654842394689957978341\\">Lunch '
        "with mom\\n      </li><li "
        'jdn-hash=\\"8485642180842394688346973594\\">Feed the '
        "hamster\\n      </li><li "
        'jdn-hash=\\"0977617602842394684696910030\\">Clean '
        "kitchen\\n    </li></ol>\\n</li></ul>\\n\\n<p "
        'jdn-hash=\\"2062873048842394684036507809\\">And '
        "finally, how about some <a "
        'href=\\"http://www.yahoo.com/\\" '
        'jdn-hash=\\"0103848358842394684976681594\\">Links'
        "?</a></p>\\n\\n<p "
        'jdn-hash=\\"6034232264842394689263545313\\">Or '
        'let\'s just link to <a href=\\"../../index.html\\" '
        'jdn-hash=\\"3027183088842394682894924777\\">another '
        "page on this server</a></p>\\n\\n<p "
        'jdn-hash=\\"4056348058842394686575005676'
        '\\">Remember, you can view the HTMl code from this '
        'or any other page by using the \\"View Page '
        'Source\\" command of your '
        "browser.</p>\\n\\n\\n\\n\\n<div "
        'id=\\"9772922236842394671549553513\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 8px; height: 37.6px; width: '
        '1503.2px;\\"><div><span class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "titleH1</span></span></div></div><div "
        'id=\\"4193993466842394678988767466\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 67.0375px; height: 27.2px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "titleH25</span></span></div></div><div "
        'id=\\"7583721053842394674210958853\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 119.213px; height: 12.8px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "titleH6</span></span></div></div><div "
        'id=\\"5572629157842394676934206880\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 156.988px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP13</span></span></div></div><div "
        'id=\\"3363615764842394670921018049\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 191.387px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP15</span></span></div></div><div "
        'id=\\"5721291098842394672262179535\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 225.788px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP11</span></span></div></div><div "
        'id=\\"6141640202842394676845507677\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 260.188px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP9</span></span></div></div><div "
        'id=\\"6509829360842394679374579325\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 294.587px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP8</span></span></div></div><div "
        'id=\\"9552011587842394678546958439\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 328.988px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP7</span></span></div></div><div "
        'id=\\"2124540623842394679666778990\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 363.388px; height: 18.4px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP16</span></span></div></div><div "
        'id=\\"3454558281842394677212548221\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 397.788px; height: 266px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        "textP</span></span></div></div><div "
        'id=\\"6491321822842394671263543627\\" '
        'class=\\"jdn-highlight jdn-secondary\\" '
        'jdn-highlight=\\"true\\" jdn-status=\\"PENDING\\" '
        'style=\\"left: 8px; top: 679.788px; height: 262px; '
        'width: 1503.2px;\\"><div><span '
        'class=\\"jdn-label\\"><span '
        'class=\\"jdn-class\\">100%, '
        'textP1</span></span></div></div></body>" '
    )
    return mock_simple_page


@pytest.fixture
def mock_predict_html_request_body():
    mock_predict_html_request_body = [
        {
            "tag_name": "HTML",
            "element_id": "7220984636029324676365471567",
            "parent_id": None,
            "x": 0,
            "y": 0,
            "width": 532.7999877929688,
            "height": 1141.800048828125,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "7220984636029324676365471567"},
            "text": "Header \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0"
            "\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main1\\n\xd0\x91\xd0"
            "\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba"
            "\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main2\\n"
            "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba\xd1\x81 \xd1\x83\xd0\xbd\xd0\
                xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main3\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\
                xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\
                xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \
                xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\
                xbd\xd1\x8b\xd0\xbc ID = main4\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0"
            "\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x9f\xd1\x80\xd0\xbe\
                xd1\x81\xd1\x82\xd0\xbe\xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\xd0\
                xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba\\n\\n\xd0\x9a\xd0\xb0\xd0"
            "\xba\xd0\xbe\xd0\xb9-\xd1\x82\xd0\xbe \xd0\xba\xd0\xbe\xd0\
                xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82\\n\\n\xd0\x95\xd1\x89\xd0\
                xb5\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbd\\n\\n\xd0\x98 \xd1\x81\xd0"
            "\xbd\xd0\xbe\xd0\xb2\xd0\xb0\\n\\nFooter \xd0\xb1\xd0\xb5\xd0"
            "\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81\xd1\x83\
                xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\
                x8b\xd0\xbc ID = main5\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \
                xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\
                x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main6\\n\xd0\x91\xd0\xbb\xd0"
            "\xbe\xd0\xba\xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\
                xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\
                xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\
                xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main7\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0"
            "\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "HEAD",
            "element_id": "8511898237029324670140028561",
            "parent_id": "7220984636029324676365471567",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "8511898237029324670140028561"},
            "text": "\\n        \\n        \xd0\x9a\xd0\xbe\xd0\xbc\xd0\xb1\xd0"
            "\xb8\xd0\xbd\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8 \xd0\xb1\xd0\
                xbb\xd0\xbe\xd0\xba\xd0\xbe\xd0\xb2 \xd1\x81 \xd0\xb3\xd0\
                xbb\xd1\x83\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xbe\xd0\xb9 3\\n\\"
            "t\\n\\t\\tdiv {\\n  \\t\\t\\tbackground-color: #7695FE;\\"
            "n  \\t\\t\\tborder: thin #336699 solid;\\n  \\t\\t\\"
            "tpadding: 10px;\\n  \\t\\t\\tmargin: 10px;\\n  \\t\\t\\"
            "ttext-align: center;\\n\\n\\t\\t}\\n\\t\\theader {\\n\\t\\t\\"
            "tborder-color: #008a77;\\n\\t\\t\\tborder-style: solid;\\n\\"
            "t\\t\\tpadding: 10px;\\n\\t\\t\\tmargin: 10px;\\n\\t\\t}\\n\
                \t\\tfooter {\\n\\t\\t\\tborder-color: #008a77;\\n\\t\\t\\"
            "tborder-style: solid;\\n\\t\\t\\tpadding: 10px;\\n\\t\\t\\"
            "tmargin: 10px;\\n\\t\\t}\\n\\t\\n    ",
        },
        {
            "tag_name": "META",
            "element_id": "8238579074029324678311820056",
            "parent_id": "8511898237029324670140028561",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "charset": "utf-8",
                "jdn-hash": "8238579074029324678311820056",
            },
            "text": "",
        },
        {
            "tag_name": "TITLE",
            "element_id": "9185149581029324670117322490",
            "parent_id": "8511898237029324670140028561",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "9185149581029324670117322490"},
            "text": "\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xb1\xd0\xb8\xd0\xbd\xd0\xb0\xd1"
            "\x86\xd0\xb8\xd0\xb8 \xd0\xb1\xd0\xbb\xd0\xbe\xd0\xba\xd0\xbe"
            "\xd0\xb2 \xd1\x81 \xd0\xb3\xd0\xbb\xd1\x83\xd0\xb1\xd0\xb8\
                xd0\xbd\xd0\xbe\xd0\xb9 3",
        },
        {
            "tag_name": "STYLE",
            "element_id": "0018850454029324670599463042",
            "parent_id": "8511898237029324670140028561",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0018850454029324670599463042"},
            "text": "\\n\\t\\tdiv {\\n \\t\\t\\tbackground-color: #7695FE;\\n  "
            "\\t\\t\\tborder: thin #336699 solid;\\n  \\t\\t\\tpadding: "
            "10px;\\n  \\t\\t\\tmargin: 10px;\\n  \\t\\t\\ttext-align:"
            "center;\\n\\n\\t\\t}\\n\\t\\theader {\\n\\t\\t\\tborder-color:"
            " #008a77;\\n\\t\\t\\tborder-style: solid;\\n\\t\\t\\tpadding:"
            "10px;\\n\\t\\t\\tmargin: 10px;\\n\\t\\t}\\n\\t\\tfooter {\\n\
                \t\\t\\tborder-color: #008a77;\\n\\t\\t\\tborder-style: solid;"
            "\\n\\t\\t\\tpadding: 10px;\\n\\t\\t\\tmargin: 10px;\\n\\t\\t}"
            "\\n\\t",
        },
        {
            "tag_name": "BODY",
            "element_id": "0082007708029324670636177198",
            "parent_id": "7220984636029324676365471567",
            "x": 8,
            "y": 10,
            "width": 516.7999877929688,
            "height": 1121.800048828125,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0082007708029324670636177198"},
            "text": "Header \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0"
            "\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main1\\n\xd0\x91\
                xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0"
            "\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main2\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba\xd1\x81 \xd1\
                x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\
                xd1\x8b\xd0\xbc ID = main3\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba "
            "\xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba "
            "\xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba "
            "\xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\
                x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main4\\n\xd0\x91\xd0\xbb\xd0\
                xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x9f\xd1\x80\xd0"
            "\xbe\xd1\x81\xd1\x82\xd0\xbe \xd0\xb7\xd0\xb0\xd0\xb3\xd0\xbe\
                xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba\\n\\n\xd0\x9a\xd0\xb0\
                xd0\xba\xd0\xbe\xd0\xb9-\xd1\x82\xd0\xbe \xd0\xba\xd0\xbe\xd0\
                xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82\\n\\n\xd0\x95\xd1\x89\xd0\
                xb5 \xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbd\\n\\n\xd0\x98\xd1\x81\xd0"
            "\xbd\xd0\xbe\xd0\xb2\xd0\xb0\\n\\nFooter \xd0\xb1\xd0\xb5\xd0"
            "\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\
                xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b"
            "\xd0\xbc ID = main5\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\
                x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\
                xd0\xbd\xd1\x8b\xd0\xbc ID = main6\\n\xd0\x91\xd0\xbb\xd0\xbe"
            "\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\
                xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\
                xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0"
            "\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main7\\n\
                xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "HEADER",
            "element_id": "4640212527029324674660482489",
            "parent_id": "0082007708029324670636177198",
            "x": 18,
            "y": 10,
            "width": 496.8000183105469,
            "height": 465.2749938964844,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main1", "jdn-hash": "4640212527029324674660482489"},
            "text": "Header \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\
        xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main1\\n\xd0\x91\xd0\xbb\xd0\
        xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\
        xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main2\\n\xd0\x91\xd0\xbb\xd0\xbe\
        xd0\xba\xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\
        x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main3\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\
        xba \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \
        xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81"
            " \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0"
            "\xbd\xd1\x8b\xd0\xbc ID = main4\\n\xd0\x91\xd0\xbb\xd0\xbe\
                xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "H1",
            "element_id": "6125528352029324678033982693",
            "parent_id": "4640212527029324674660482489",
            "x": 30.399999618530273,
            "y": 43.837501525878906,
            "width": 472,
            "height": 75.20000457763672,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "6125528352029324678033982693"},
            "text": "Header \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0"
            "\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main1",
        },
        {
            "tag_name": "DIV",
            "element_id": "3573727654029324675421326291",
            "parent_id": "4640212527029324674660482489",
            "x": 40.400001525878906,
            "y": 140.47500610351562,
            "width": 452,
            "height": 151.1999969482422,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main2", "jdn-hash": "3573727654029324675421326291"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main2\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\
                x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1"
            "\x8b\xd0\xbc ID = main3\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \
                xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "0389530473029324687995154036",
            "parent_id": "3573727654029324675421326291",
            "x": 61.400001525878906,
            "y": 179.875,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main3", "jdn-hash": "0389530473029324687995154036"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main3",
        },
        {
            "tag_name": "DIV",
            "element_id": "5383966325029324680589610684",
            "parent_id": "3573727654029324675421326291",
            "x": 61.400001525878906,
            "y": 230.27500915527344,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "5383966325029324680589610684"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "5391590654029324684395137976",
            "parent_id": "4640212527029324674660482489",
            "x": 40.400001525878906,
            "y": 301.6750183105469,
            "width": 452,
            "height": 151.1999969482422,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "5391590654029324684395137976"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 "
            "ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\
                xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\
                xd0\xbc ID = main4\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\
                xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "8897113917029324682951093729",
            "parent_id": "5391590654029324684395137976",
            "x": 61.400001525878906,
            "y": 341.07501220703125,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main4", "jdn-hash": "8897113917029324682951093729"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main4",
        },
        {
            "tag_name": "DIV",
            "element_id": "8845167505029324686758415721",
            "parent_id": "5391590654029324684395137976",
            "x": 61.400001525878906,
            "y": 391.4750061035156,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "8845167505029324686758415721"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "9459882663029324684189471250",
            "parent_id": "0082007708029324670636177198",
            "x": 18,
            "y": 485.2749938964844,
            "width": 496.8000183105469,
            "height": 208.85000610351562,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "class": "Content",
                "jdn-hash": "9459882663029324684189471250",
            },
            "text": "\xd0\x9f\xd1\x80\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe \xd0\xb7\xd0\
        xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba\\n\\n\xd0"
            "\x9a\xd0\xb0\xd0\xba\xd0\xbe\xd0\xb9-\xd1\x82\xd0\xbe \xd0\
                xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82\\n\\n\xd0\
                x95\xd1\x89\xd0\xb5 \xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbd\\n\\n\xd0"
            "\x98 \xd1\x81\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0",
        },
        {
            "tag_name": "H2",
            "element_id": "0845270812029324688456919969",
            "parent_id": "9459882663029324684189471250",
            "x": 29,
            "y": 516.1875,
            "width": 474.8000183105469,
            "height": 27.200000762939453,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0845270812029324688456919969"},
            "text": "\xd0\x9f\xd1\x80\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe \xd0\xb7\xd0"
            "\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba",
        },
        {
            "tag_name": "P",
            "element_id": "7054485647029324682871973688",
            "parent_id": "9459882663029324684189471250",
            "x": 29,
            "y": 563.2999877929688,
            "width": 474.8000183105469,
            "height": 18.399999618530273,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "7054485647029324682871973688"},
            "text": "\xd0\x9a\xd0\xb0\xd0\xba\xd0\xbe\xd0\xb9-\xd1\x82\xd0\xbe \
        xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82",
        },
        {
            "tag_name": "H2",
            "element_id": "8570141971029324682751918828",
            "parent_id": "9459882663029324684189471250",
            "x": 29,
            "y": 601.6124877929688,
            "width": 474.8000183105469,
            "height": 27.200000762939453,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "8570141971029324682751918828"},
            "text": "\xd0\x95\xd1\x89\xd0\xb5 \xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbd",
        },
        {
            "tag_name": "P",
            "element_id": "0560335606029324680223883751",
            "parent_id": "9459882663029324684189471250",
            "x": 29,
            "y": 648.7250366210938,
            "width": 474.8000183105469,
            "height": 18.399999618530273,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0560335606029324680223883751"},
            "text": "\xd0\x98 \xd1\x81\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0",
        },
        {
            "tag_name": "FOOTER",
            "element_id": "2647726871029324686979223437",
            "parent_id": "0082007708029324670636177198",
            "x": 18,
            "y": 704.125,
            "width": 496.8000183105469,
            "height": 427.6750183105469,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "2647726871029324686979223437"},
            "text": "Footer \xd0\xb1\xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe"
            "\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0"
            "\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc ID = main5\\n\xd0\x91\xd0"
            "\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0\xb8\xd0\xba"
            "\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main6\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\
                xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\
                xd0\xb5\xd0\xb7 ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 "
            "\xd1\x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\
                xbd\xd1\x8b\xd0\xbc ID = main7\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\
                xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "H1",
            "element_id": "0395444610029324683635685321",
            "parent_id": "2647726871029324686979223437",
            "x": 30.399999618530273,
            "y": 737.9625244140625,
            "width": 472,
            "height": 37.60000228881836,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0395444610029324683635685321"},
            "text": "Footer \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "9769906611029324684314988597",
            "parent_id": "2647726871029324686979223437",
            "x": 40.400001525878906,
            "y": 797,
            "width": 452,
            "height": 151.1999969482422,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main5", "jdn-hash": "9769906611029324684314988597"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main5\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\
                x83\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1"
            "\x8b\xd0\xbc ID = main6\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \
                xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "3698429813029324680150065659",
            "parent_id": "9769906611029324684314988597",
            "x": 61.400001525878906,
            "y": 836.4000244140625,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "mai6", "jdn-hash": "3698429813029324680150065659"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main6",
        },
        {
            "tag_name": "DIV",
            "element_id": "1915326623029324681970384124",
            "parent_id": "9769906611029324684314988597",
            "x": 61.400001525878906,
            "y": 886.7999877929688,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "1915326623029324681970384124"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "3870010824029324682543162184",
            "parent_id": "2647726871029324686979223437",
            "x": 40.400001525878906,
            "y": 958.2000122070312,
            "width": 452,
            "height": 151.1999969482422,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "3870010824029324682543162184"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 "
            "ID\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\
                xbd\xd0\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\
                xd0\xbc ID = main7\\n\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1"
            "\xd0\xb5\xd0\xb7 ID",
        },
        {
            "tag_name": "DIV",
            "element_id": "2587789745029324682289738923",
            "parent_id": "3870010824029324682543162184",
            "x": 61.400001525878906,
            "y": 997.6000366210938,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"id": "main7", "jdn-hash": "2587789745029324682289738923"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd1\x81 \xd1\x83\xd0\xbd\xd0"
            "\xb8\xd0\xba\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc "
            "ID = main7",
        },
        {
            "tag_name": "DIV",
            "element_id": "2272339177029324688461115174",
            "parent_id": "3870010824029324682543162184",
            "x": 61.400001525878906,
            "y": 1048,
            "width": 410,
            "height": 40.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "2272339177029324688461115174"},
            "text": "\xd0\x91\xd0\xbb\xd0\xbe\xd0\xba \xd0\xb1\xd0\xb5\xd0\xb7 ID",
        },
    ]

    return mock_predict_html_request_body


@pytest.fixture
def mock_predict_mui_request_body():
    mock_predict_mui_request_body = [
        {
            "tag_name": "HTML",
            "element_id": "3336566090148511111989974563",
            "parent_id": None,
            "x": 0,
            "y": 0,
            "width": 549.6000366210938,
            "height": 267.6750183105469,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "3336566090148511111989974563"},
            "text": "Example Domain\\n\\nThis domain is for use in illustrative "
            "examples in documents. You may use this domain in literature "
            "without prior coordination or asking for permission.\\n\\n"
            "More information...",
        },
        {
            "tag_name": "HEAD",
            "element_id": "0764730516148511114916431143",
            "parent_id": "3336566090148511111989974563",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "0764730516148511114916431143"},
            "text": "\\n    Example Domain\\n\\n    \\n    \\n    \\n    \\n    "
            "body {\\n        background-color: #f0f0f2;\\n        margin: "
            "0;\\n        padding: 0;\\n        font-family: -apple-system, "
            'system-ui, BlinkMacSystemFont, \\"Segoe UI\\", \\"Open Sans\\", '
            '\\"Helvetica Neue\\", Helvetica, Arial, sans-serif;\\n        '
            "\\n    }\\n    div {\\n        width: 600px;\\n        "
            "margin: 5em auto;\\n        padding: 2em;\\n       "
            "background-color: #fdfdff;\\n        border-radius: 0.5em;\\"
            "n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\\n    }"
            "\\n    a:link, a:visited {\\n        color: #38488f;\\n       "
            " text-decoration: none;\\n    }\\n    @media (max-width: 700px)"
            " {\\n        div {\\n            margin: 0 auto;\\n           "
            " width: auto;\\n        }\\n    }\\n        \\n",
        },
        {
            "tag_name": "TITLE",
            "element_id": "3391378189148511114730185652",
            "parent_id": "0764730516148511114916431143",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "3391378189148511114730185652"},
            "text": "Example Domain",
        },
        {
            "tag_name": "META",
            "element_id": "1669087435148511113481565763",
            "parent_id": "0764730516148511114916431143",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "charset": "utf-8",
                "jdn-hash": "1669087435148511113481565763",
            },
            "text": "",
        },
        {
            "tag_name": "META",
            "element_id": "5031259000148511118782402543",
            "parent_id": "0764730516148511114916431143",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "http-equiv": "Content-type",
                "content": "text/html; charset=utf-8",
                "jdn-hash": "5031259000148511118782402543",
            },
            "text": "",
        },
        {
            "tag_name": "META",
            "element_id": "7325185367148511118397557202",
            "parent_id": "0764730516148511114916431143",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1",
                "jdn-hash": "7325185367148511118397557202",
            },
            "text": "",
        },
        {
            "tag_name": "STYLE",
            "element_id": "5934169267148511119135331701",
            "parent_id": "0764730516148511114916431143",
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0,
            "displayed": False,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "type": "text/css",
                "jdn-hash": "5934169267148511119135331701",
            },
            "text": "\\n    body {\\n        background-color: #f0f0f2;\\n        "
            "margin: 0;\\n        padding: 0;\\n        font-family: "
            '-apple-system, system-ui, BlinkMacSystemFont, \\"Segoe UI\\", '
            '\\"Open Sans\\", \\"Helvetica Neue\\", Helvetica, Arial, '
            "sans-serif;\\n        \\n    }\\n    div {\\n        "
            "width: 600px;\\n        margin: 5em auto;\\n        "
            "padding: 2em;\\n        background-color: #fdfdff;\\n        "
            "border-radius: 0.5em;\\n        box-shadow: 2px 3px 7px 2px "
            "rgba(0,0,0,0.02);\\n    }\\n    a:link, a:visited {\\n        "
            "color: #38488f;\\n        text-decoration: none;\\n    }\\n  "
            "  @media (max-width: 700px) {\\n        div {\\n            "
            "margin: 0 auto;\\n            width: auto;\\n        }\\n    "
            "}\\n    ",
        },
        {
            "tag_name": "BODY",
            "element_id": "5171222660148511114907651022",
            "parent_id": "3336566090148511111989974563",
            "x": 0,
            "y": 0,
            "width": 549.6000366210938,
            "height": 267.6750183105469,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "5171222660148511114907651022"},
            "text": "Example Domain\\n\\nThis domain is for use in illustrative "
            "examples in documents. You may use this domain in literature "
            "without prior coordination or asking for permission.\\n\\n"
            "More information...",
        },
        {
            "tag_name": "DIV",
            "element_id": "6200000529148511111274513917",
            "parent_id": "5171222660148511114907651022",
            "x": 0,
            "y": 0,
            "width": 549.6000366210938,
            "height": 267.6750183105469,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "6200000529148511111274513917"},
            "text": "Example Domain\\n\\nThis domain is for use in illustrative "
            "examples in documents. You may use this domain in literature "
            "without prior coordination or asking for permission.\\n\\n"
            "More information...",
        },
        {
            "tag_name": "H1",
            "element_id": "7988753852148511119026682429",
            "parent_id": "6200000529148511111274513917",
            "x": 32,
            "y": 53.4375,
            "width": 485.6000061035156,
            "height": 42.400001525878906,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "7988753852148511119026682429"},
            "text": "Example Domain",
        },
        {
            "tag_name": "P",
            "element_id": "1339472578148511110315514566",
            "parent_id": "6200000529148511111274513917",
            "x": 32,
            "y": 117.2750015258789,
            "width": 485.6000061035156,
            "height": 64.80000305175781,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "1339472578148511110315514566"},
            "text": "This domain is for use in illustrative examples in documents. "
            "You may use this domain in literature without prior "
            "coordination or asking for permission.",
        },
        {
            "tag_name": "P",
            "element_id": "5358765886148511115211341401",
            "parent_id": "6200000529148511111274513917",
            "x": 32,
            "y": 198.0749969482422,
            "width": 485.6000061035156,
            "height": 21.600000381469727,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {"jdn-hash": "5358765886148511115211341401"},
            "text": "More information...",
        },
        {
            "tag_name": "A",
            "element_id": "1809317032148511112403159843",
            "parent_id": "5358765886148511115211341401",
            "x": 32,
            "y": 198.0749969482422,
            "width": 134.9875030517578,
            "height": 21.600000381469727,
            "displayed": True,
            "onmouseover": None,
            "onmouseenter": None,
            "attributes": {
                "href": "https://www.iana.org/domains/example",
                "jdn-hash": "1809317032148511112403159843",
            },
            "text": "More information...",
        },
    ]
    return mock_predict_mui_request_body
