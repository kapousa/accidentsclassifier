import requests
from flask import Flask, render_template, request

app = Flask(__name__)

URL = 'https://bmapiproject.azurewebsites.net/api/v1/30908139127022/classifydata'

resources_available_mapper = {
    "Rear-end collisions": "1 Responders,2 Supplies,0 Boats",
    "Head-on collisions": "8 Responders, 6 Supplies,3 Boats",
    "Side-impact collisions": "4 Responders,9 Supplies,2 Boats",
    "T-bone collisions": "8 Responders,1 Supplies,4 Boats",
    "Multi-car pileups": "3 Responders,5 Supplies,0 Boats",
    "Single-car accidents": "7 Responders,0 Supplies,7 Boats",
    "Hit and run accidents": "8 Responders,3 Supplies,8 Boats",
    "Pedestrian accidents": "3 Responders,2 Supplies,7 Boats"
}

distribution_of_aid_mapper = {
    "Rear-end collisions": "Food, Shelter",
    "Head-on collisions": "Water",
    "Side-impact collisions": "Food, Water, Shelter",
    "T-bone collisions": " Shelter",
    "Multi-car pileups": " Water, Shelter",
    "Single-car accidents": "Food, Water",
    "Hit and run accidents": "Water, Shelter",
    "Pedestrian accidents": "Food, Water, Shelter"
}

response_time_mapper = {
    "Rear-end collisions": "2",
    "Head-on collisions": "3",
    "Side-impact collisions": "5",
    "T-bone collisions": "6",
    "Multi-car pileups": "1",
    "Single-car accidents": "0.5",
    "Hit and run accidents": "2",
    "Pedestrian accidents": "4"
}

rescue_plan_mapper = {
    "Rear-end collisions": "https://www.youtube.com/embed/ChL6bmz7m7M",
    "Head-on collisions": "https://www.youtube.com/embed/oEAKHmsA3Z0",
    "Side-impact collisions": "https://www.youtube.com/embed/--kRpkSwv9w",
    "T-bone collisions": "https://www.youtube.com/embed/stdZoiFOuM0",
    "Multi-car pileups": "https://www.youtube.com/embed/aLOObx8H7DA",
    "Single-car accidents": "https://www.youtube.com/embed/SmGgZ-jpmNc",
    "Hit and run accidents": "https://www.youtube.com/embed/vvTnUAfkC40",
    "Pedestrian accidents": "https://www.youtube.com/embed/jTQ1JWK3XCM"
}


@app.route('/')
def index():
    desc = request.form.get("desc")
    return render_template('index.html', action_plan="None", desc="")


@app.route('/generateactionplan', methods=['POST'])
def generateactionplan():
    desc = request.form.get("desc")

    if desc != None:
        # sending get request and saving the response as response object
        PARAMS = {'data': desc}
        r = requests.post(url=URL, json=PARAMS)
        categories = []
        if r.status_code == 200:
            return_data = r.json()
            for k, v in return_data.items():
                categories.append(v)

        # Build action plan
        for i in range(len(categories)):
            resources_avilable = resources_available_mapper[categories[i]]
            resources_avilable = resources_avilable.split(',')
            distribution_of_aid = distribution_of_aid_mapper[categories[i]]
            distribution_of_aid = distribution_of_aid.split(',')
            response_time = response_time_mapper[categories[i]]
            plan_name = categories[i]
            plan_video = rescue_plan_mapper[plan_name]

        resouce_number = []
        resource_name = []
        for i in range(len(resources_avilable)):
            resouce_number.append(resources_avilable[i][:1])
            resource_name.append(resources_avilable[i][2:])

    return render_template('plan.html', action_plan="exist", desc=desc, resources_avilable=resources_avilable,
                           distribution_of_aid=distribution_of_aid, response_time=response_time, plan_name=plan_name, plan_video=plan_video, clock_image= "static/images/icon/Clock.png", resource_name= resource_name, resouce_number=resouce_number)


if __name__ == '__main__':
    app.run()
