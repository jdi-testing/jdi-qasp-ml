import pytest

from app.tasks import task_schedule_xpath_generation

mock_html_page_code = """
<head jdn-hash="4361097403863276612912310134">
         <meta charset="utf-8" jdn-hash="7913640661863276615714707459">
         <title jdn-hash="8598800324863276613727735360">Комбинации блоков с глубиной 3</title>
    <style jdn-hash="5293904565863276612580899721">
            div {
                    background-color: #7695FE;
                    border: thin #336699 solid;
                    padding: 10px;
                    margin: 10px;
                    text-align: center;

            }
            header {
                    border-color: #008a77;
                    border-style: solid;
                    padding: 10px;
                    margin: 10px;
            }
            footer {
                    border-color: #008a77;
                    border-style: solid;
                    padding: 10px;
                    margin: 10px;
            }
    </style>
     </head>
     <body jdn-hash="9524922623863276614194392984">
         <header id="main1" jdn-hash="4710303396863276617714104459">
            <h1 jdn-hash="7531002150863276618099465122">Header с уникальным ID = main1</h1>
            <div id="main2" jdn-hash="6898340876863276615063008062">
                Блок с уникальным ID = main2
                <div id="main3" jdn-hash="4996518264863276625559601113">Блок с уникальным ID = main3</div>
                <div jdn-hash="6945997776863276627355514186">Блок без ID</div>
            </div>
            <div jdn-hash="6411933497863276626564883815">
                Блок без ID
                <div id="main4" jdn-hash="9370885956863276621257946974">Блок с уникальным ID = main4</div>
                <div jdn-hash="8269088400863276622331733443">Блок без ID</div>
            </div>

    </header>
    <div class="Content" jdn-hash="2275563265863276624921676498">
            <h2 jdn-hash="7398993944863276624470456479">Просто заголовок</h2>
            <p jdn-hash="5450933298863276620235133171">Какой-то контент</p>
            <h2 jdn-hash="6060767279863276627461426417">Еще один</h2>
            <p jdn-hash="5073860463863276623690656873">И снова</p>
    </div>
         <footer jdn-hash="0329819731863276629881374440">
            <h1 jdn-hash="2169648125863276623834615542">Footer без ID</h1>
            <div id="main5" jdn-hash="7899801282863276627096681733">
                Блок с уникальным ID = main5
                <div id="mai6" jdn-hash="5103493915863276622439799353">Блок с уникальным ID = main6</div>
                <div jdn-hash="6083500568863276626995812760">Блок без ID</div>
            </div>
            <div jdn-hash="9781601218863276623154685617">
                Блок без ID
                <div id="main7" jdn-hash="7486900188863276629399402290">Блок с уникальным ID = main7</div>
                <div jdn-hash="5736619075863276627151919404">Блок без ID</div>
            </div>
    </footer>

 <div id="7531002150863276618099465122" class="jdn-highlight jdn-secondary" 
 jdn-highlight="true" jdn-status="undefined" style="left: 30.4px; top: 43.8375px; 
 height: 75.2px; width: 472px;"><div><span class="jdn-label"><span 
 class="jdn-class">100%, uielementH1</span></span></div></div><div 
 id="7398993944863276624470456479" class="jdn-highlight jdn-secondary" 
 jdn-highlight="true" jdn-status="undefined" style="left: 29px; top: 516.188px; 
 height: 27.2px; width: 474.8px;"><div><span class="jdn-label"><span 
 class="jdn-class">100%, uielementH23</span></span></div></div><div 
 id="5450933298863276620235133171" class="jdn-highlight jdn-secondary" 
 jdn-highlight="true" jdn-status="undefined" style="left: 29px; top: 563.3px; 
 height: 18.4px; width: 474.8px;"><div><span class="jdn-label"><span 
 class="jdn-class">100%, uielementP5</span></span></div></div><div 
 id="6060767279863276627461426417" class="jdn-highlight jdn-secondary" 
 jdn-highlight="true" jdn-status="undefined" style="left: 29px; top: 601.612px; 
 height: 27.2px; width: 474.8px;"><div><span class="jdn-label"><span 
 class="jdn-class">100%, uielementH2</span></span></div></div><div 
 id="5073860463863276623690656873" class="jdn-highlight jdn-secondary" 
 jdn-highlight="true" jdn-status="undefined" style="left: 29px; top: 648.725px;
  height: 18.4px; width: 474.8px;"><div><span class="jdn-label"><span 
  class="jdn-class">100%, uielementP</span></span></div></div><div 
  id="2169648125863276623834615542" class="jdn-highlight jdn-secondary" 
  jdn-highlight="true" jdn-status="undefined" style="left: 30.4px; 
  top: 737.963px; height: 37.6px; width: 472px;"><div><span class="jdn-label">
  <span class="jdn-class">100%, uielementH11</span></span></div></div></body>

"""


def test_task_schedule_xpath_generation_positive_case():
    element_id = "//*[@jdn-hash='5450933298863276620235133171']"
    config = {
        "maximum_generation_time": 10,
        "allow_indexes_at_the_beginning": False,
        "allow_indexes_in_the_middle": False,
        "allow_indexes_at_the_end": False,
    }
    result = task_schedule_xpath_generation(
        element_id=element_id, document=mock_html_page_code, config=config
    )
    assert result == "//*[contains(text(), 'Какой-то контент')]"


def test_task_schedule_xpath_generation_element_not_found():
    element_id = "//*[@jdn-hash='1234567890987654321']"
    config = {
        "maximum_generation_time": 10,
        "allow_indexes_at_the_beginning": False,
        "allow_indexes_in_the_middle": False,
        "allow_indexes_at_the_end": False,
    }

    from utils.robula import XPathDocumentDoesntContainElement

    with pytest.raises(XPathDocumentDoesntContainElement):
        task_schedule_xpath_generation(
            element_id=element_id, document=mock_html_page_code, config=config
        )
